import json
from app.models import Contact

def test_get_contacts(client, db):
    # Add some contacts to the database
    contact1 = Contact(first_name='Alice', last_name='Smith', phone_number='1122355', address='456 Elm St')
    contact2 = Contact(first_name='Bob', last_name='Jones', phone_number='1122466', address='789 Oak St')
    db.session.add(contact1)
    db.session.add(contact2)
    db.session.commit()

    # Test getting contacts with pagination (page 1)
    response = client.get('/contacts')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['first_name'] == 'Alice'
    assert data[1]['first_name'] == 'Bob'


def test_add_contacts(client, db):
    # Define contact data
    contact_data = [
        {'first_name': 'Charlie', 'last_name': 'Brown', 'phone_number': '5555555555', 'address': '123 Maple St'},
        {'first_name': 'Lucy', 'last_name': 'Van Pelt', 'phone_number': '5555555556', 'address': '456 Oak St'}
    ]

    response = client.post('/contacts', json=contact_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['status'] == 'success'
    assert data[1]['status'] == 'success'


def test_add_contacts_invalid_format(client, db):
    # Test invalid input format
    contact_data = {'first_name': 'Invalid', 'last_name': 'Format'}

    response = client.post('/contacts', json=contact_data)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'Invalid input format, expected a list of contacts'


def test_edit_contact(client, db):
    # Add a contact
    contact = Contact(first_name='Daisy', last_name='Duck', phone_number='555888', address='789 Pine St')
    db.session.add(contact)
    db.session.commit()

    # Edit the contact
    update_data = {'first_name': 'Daisy', 'last_name': 'Duck', 'address': '123 Birch St'}
    response = client.put('/contacts/phone/555888', json=update_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['address'] == '123 Birch St'

    db.session.delete(contact)
    db.session.commit()


def test_delete_contact(client, db):
    # Add a contact to be deleted
    contact = Contact(first_name='Donald', last_name='Duck', phone_number='5555555558', address='1010 Maple St')
    db.session.add(contact)
    db.session.commit()

    # Delete the contact
    response = client.delete('/contacts/phone/5555555558')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Contact with phone number 5555555558 deleted'
