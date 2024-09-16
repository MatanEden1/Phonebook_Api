import os
from app.models import db, Contact
from app.schemas import ContactCreate, ContactUpdate

CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', 60))

def init_routes(app):
    from app import cache
    @app.route('/contacts', methods=['GET'])
    @cache.cached(timeout=CACHE_TIMEOUT, query_string=True)
    def get_contacts():
        app.logger.info('GET /contacts endpoint accessed')
        page = request.args.get('page', 1, type=int)
        try:
            contacts =  Contact.query.paginate(page=page, per_page=10).items
            response = jsonify([contact.to_dict() for contact in contacts])
            app.logger.info('Contacts retrieved successfully')
            response.status_code = 200
            return response
        except Exception as e:
            app.logger.error(f"Error retrieving contacts: {e}")
            response = jsonify({'error': 'An error occurred while retrieving contacts.'})
            response.status_code = 500
            return response

    @app.route('/contacts/search', methods=['GET'])
    @cache.cached(timeout=CACHE_TIMEOUT, query_string=True)  # Use timeout from .env
    def search_contacts():
        app.logger.info('GET /contacts/search endpoint accessed with query: %s', request.args.get('q'))
        query = request.args.get('q', '', type=str)
        try:
            contacts = Contact.query.filter(Contact.first_name.ilike(f'%{query}%') |
                                            Contact.last_name.ilike(f'%{query}%')).all()
            response = jsonify([contact.to_dict() for contact in contacts])
            app.logger.info('Contacts search completed')
            response.status_code = 200
            return response

        except Exception as e:
            app.logger.error(f"Error searching contacts: {e}")
            response = jsonify({'error': 'An error occurred while searching contacts.'})
            response.status_code = 500
            return response

    from flask import Flask, request, jsonify
    from sqlalchemy.exc import IntegrityError
    from pydantic import ValidationError
    import logging

    @app.route('/contacts', methods=['POST'])
    def add_contacts():
        app.logger.info('POST /contacts endpoint accessed')
        data = request.json

        if not isinstance(data, list):
            app.logger.error('Invalid input format')
            response = jsonify({'error': 'Invalid input format, expected a list of contacts'})
            response.status_code = 400
            return response

        responses = []
        for contact_data in data:
            try:
                contact_create = ContactCreate(**contact_data)
                exist_contact = Contact.query.filter_by(phone_number=contact_create.phone_number).first()

                if exist_contact:
                    app.logger.info(
                        f'Contact with phone number %s already exists in the database: {contact_create.phone_number}')
                    responses.append({
                        'status': 'error',
                        'contact': contact_data,
                        'message': 'A contact with this phone number already exists.'
                    })
                    continue  # Skip to the next contact

                contact = Contact(
                    first_name=contact_create.first_name,
                    last_name=contact_create.last_name,
                    phone_number=contact_create.phone_number,
                    address=contact_create.address
                )

                db.session.add(contact)
                db.session.commit()
                responses.append({'status': 'success', 'contact': contact.to_dict()})
                app.logger.info('Contact added successfully: %s', contact_data)

                # Clear cache after data modification
                cache.delete_memoized(get_contacts)
                cache.delete_memoized(search_contacts)

            except ValidationError as e:
                errors = e.errors()
                formatted_errors = {
                    'error': 'Validation failed',
                    'details': errors
                }
                responses.append({'status': 'error', 'contact': contact_data, 'message': formatted_errors})
                app.logger.error('Validation error: %s', errors)
            except IntegrityError as e:
                db.session.rollback()
                if 'unique' in str(e.orig):
                    responses.append({
                        'status': 'error',
                        'contact': contact_data,
                        'message': 'Phone number already exists'
                    })
                    app.logger.warning('Unique constraint violation: %s', e.orig)
                else:
                    responses.append({
                        'status': 'error',
                        'contact': contact_data,
                        'message': 'Integrity error occurred'
                    })
                    app.logger.error('Integrity error occurred: %s', e.orig)
            except Exception as e:
                db.session.rollback()
                responses.append({
                    'status': 'error',
                    'contact': contact_data,
                    'message': 'An unexpected error occurred.'
                })
                app.logger.error(f"Error adding contact: {e}")

        response = jsonify(responses)
        response.status_code = 200
        return response

    from sqlalchemy.exc import IntegrityError
    from pydantic import ValidationError

    @app.route('/contacts/phone/<string:phone_number>', methods=['PUT'])
    def edit_contact(phone_number):
        app.logger.info('PUT /contacts/phone/%s endpoint accessed', phone_number)
        data = request.json
        try:
            contact_update = ContactUpdate(**data)
            contact = Contact.query.filter_by(phone_number=phone_number).first()

            if not contact:
                app.logger.info('Contact with phone number %s not found', phone_number)
                response = jsonify({'message': 'The number does not exist'})
                response.status_code = 404
                return response

            contact.first_name = contact_update.first_name
            contact.last_name = contact_update.last_name
            contact.phone_number = contact_update.phone_number
            contact.address = contact_update.address

            db.session.commit()
            app.logger.info('Contact edited successfully: %s', data)

            # Clear cache after data modification
            cache.delete_memoized(get_contacts)
            cache.delete_memoized(search_contacts)

            response = jsonify(contact.to_dict())
            response.status_code = 200
            return response
        except ValidationError as e:
            errors = e.errors()
            response = jsonify({'error': 'Validation failed', 'details': errors})
            app.logger.error('Validation error: %s', errors)
            response.status_code = 400
            return response
        except IntegrityError:
            db.session.rollback()
            app.logger.warning('Integrity error while editing contact')
            response = jsonify(
                {'error': 'An error occurred while updating the contact. Please ensure the data is correct.'})
            response.status_code = 400
            return response
        except Exception as e:
            app.logger.error(f"Error editing contact: {e}")
            db.session.rollback()
            response = jsonify({'error': 'An unexpected error occurred while updating the contact.'})
            response.status_code = 500
            return response


    @app.route('/contacts/phone/<string:phone_number>', methods=['DELETE'])
    def delete_contact(phone_number):
        app.logger.info('DELETE /contacts/phone/%s endpoint accessed', phone_number)
        contact = Contact.query.filter_by(phone_number=phone_number).first()

        if not contact:
            app.logger.info('Contact with phone number %s does not exist', phone_number)
            response = jsonify({'message': 'The number does not exist'})
            response.status_code = 404  # Not Found
            return response

        try:
            db.session.delete(contact)
            db.session.commit()
            app.logger.info('Contact deleted successfully with phone number: %s', phone_number)

            # Clear cache after data modification
            cache.delete_memoized(get_contacts)
            cache.delete_memoized(search_contacts)

            response = jsonify({'message': f'Contact with phone number {phone_number} deleted'})
            response.status_code = 200
            return response
        except Exception as e:
            db.session.rollback()
            app.logger.error('Exception occurred while deleting contact: %s', str(e))
            response = jsonify({'error': 'An error occurred while deleting contact.'})
            response.status_code = 500
            return response

    @app.route('/', methods=['GET'])
    def home_page():
        return "Home Page"
