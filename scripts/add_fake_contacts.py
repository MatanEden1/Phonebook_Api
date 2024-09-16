from app import create_app
from app.models import db, Contact
from faker import Faker


def generate_fake_contacts(num_contacts):
    fake = Faker()

    contacts = []
    for _ in range(num_contacts):
        contact = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'phone_number': fake.phone_number()[:10],  # Ensure the length is no more than 15 characters
            'address': fake.address()
        }
        contacts.append(contact)

    return contacts


def populate_database(num_contacts):

    app = create_app()

    with app.app_context():
        fake_contacts = generate_fake_contacts(num_contacts)


        # Add each contact to the database
        for contact_data in fake_contacts:
            contact = Contact(
                first_name=contact_data['first_name'],
                last_name=contact_data['last_name'],
                phone_number=contact_data['phone_number'],
                address=contact_data['address']
            )
            db.session.add(contact)

        # Commit the changes to the database
        db.session.commit()

    print(f"Database populated with {num_contacts} contacts.")


if __name__ == '__main__':
    num_contacts = 50  # Specify the number of contacts you want to generate
    populate_database(num_contacts)

# db.session.query(Contact).delete()
