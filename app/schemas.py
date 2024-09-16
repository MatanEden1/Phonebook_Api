from pydantic import BaseModel, conint

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    address: str

class ContactCreate(ContactBase):
    phone_number: conint(ge=0, le=9999999999)  # Max 10 digits

class ContactUpdate(ContactBase):
    phone_number: conint(ge=0, le=9999999999)  # Max 10 digits

class ContactResponse(ContactBase):
    id: int
    phone_number: conint(ge=0, le=9999999999)  # Max 10 digits
