# Phonebook API

A simple phonebook API built with Python, Flask, and Sqlite.

This API allows users to manage their contacts with operations such as creating, 

retrieving, updating, and deleting contact information.

## Features

- **Create**: Add new contacts to the phonebook.
- **Retrieve**: Get a list of contacts with pagination and search functionality.
- **Update**: Edit existing contacts.
- **Delete**: Remove contacts from the phonebook.
- **Logging**: Application logs for tracking events and errors.

## Technologies

- **Backend**: Flask
- **Database**: Sqlite3
- **ORM**: SQLAlchemy
- **Data Validation**: Pydantic
- **Logging**: RotatingFileHandler
- **Containerization**: Docker
- **Testing**: Pytest

## Getting Started

### Prerequisites

- Python 3.12.5
- Sqlite3
- Docker and Docker Compose (for containerized setup)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/phonebook-api.git
   cd phonebook-api

2. **Set up the virtual environment and install dependencies**
      ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt

3. **Run the application**
      ```bash 
   flask --app run_app run --host=0.0.0.0

## API Endpoints

### Get Contacts

- **Method**: `GET`
- **URL**: `/contacts`
- **Query Parameters**:
  - `page`: Page number for pagination (default: 1)
- **Response**: JSON array of contacts
- **Example**: For page = 2 (http://127.0.0.1:5000/contacts?page=2)

### Search Contacts

- **Method**: `GET`
- **URL**: `/contacts/search`
- **Query Parameters**:
  - `q`: Search query (first name or last name)
- **Response**: JSON array of matching contacts
- **Example**: To search for contact which include 'ma' (http://127.0.0.1:5000/contacts/search?q=ma)
### Add Contact

- **Method**: `POST`
- **URL**: `/contacts`
- **Body**: JSON object with contact details
- **Response**: JSON object with the added contact
- **Body Example**: [
    {
        "first_name": "matan",
        "last_name": "matan",
        "phone_number": 123,
        "address": "123"}]

### Update Contact

- **Method**: `PUT`
- **URL**: `/contacts/phone/<phone_number>`
- **Body**: JSON object with updated contact details
- **Response**: JSON object with the updated contact
- **Example**: (PUT REQUEST) http://localhost:5000/contacts/phone/054

### Delete Contact

- **Method**: `DELETE`
- **URL**: `/contacts/phone/<phone_number>`
- **Response**: JSON object with a confirmation message
- **Example**: (DELETE REQUEST) http://localhost:5000/contacts/phone/054

### Docker Setup
  To run the application using Docker, ensure Docker and Docker Compose are installed.
  
  Then, run:
  
    - **docker build -t mataneden/phone_book_api .**                    
    - **docker container run -d -p 5000:5000  mataneden/phone_book_api**


### Comments
For scaleable API:
- Async API (fastAPI framework)
- For Cache better to use Redis (with LFU)
- load balancer
- k8
