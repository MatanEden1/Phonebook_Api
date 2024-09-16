import pytest
from app.models import Contact
from sqlalchemy.exc import IntegrityError

def test_contact_model_creation(db):
    contact = Contact(first_name='Alice', last_name='Smith', phone_number='22', address='123 Test St')
    db.session.add(contact)
    db.session.commit()

    assert contact.id is not None
    assert contact.first_name == 'Alice'
    assert contact.last_name == 'Smith'
    assert contact.phone_number == '22'
    assert contact.address == '123 Test St'

def test_contact_model_unique_phone_number(db):
    contact1 = Contact(first_name='Alice', last_name='Smith', phone_number='22', address='123 Test St')
    contact2 = Contact(first_name='Bob', last_name='Brown', phone_number='22', address='456 Another St')
    db.session.add(contact1)
    db.session.commit()

    db.session.add(contact2)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()

def test_contact_model_default_values(db):
    contact = Contact(first_name='Charlie', last_name='Brown', phone_number='5555555555')
    db.session.add(contact)
    db.session.commit()

    assert contact.address is None  # Assuming address is optional and defaults to None
