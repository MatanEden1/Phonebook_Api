from dotenv import load_dotenv
from flask import Flask
from flask_caching import Cache
from logging.handlers import RotatingFileHandler
from app.routes import init_routes
from app.models import db
import os
import logging
import sqlite3

# Load environment variables from .env file
load_dotenv()

# Configure cache
cache = Cache()

def setup_logging(app):
    if not os.path.exists('logs'):
        os.makedirs('logs')

    handler = RotatingFileHandler('logs/app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add handler to app logger
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)


def create_database_if_not_exists(db_uri):
    db_path = db_uri.replace('sqlite:///', '')

    if not os.path.exists(db_path):
        try:
            # Create the database file by establishing a connection
            conn = sqlite3.connect(db_path)
            conn.close()
            logging.info(f"Database '{db_path}' created")
        except Exception as e:
            logging.error(f"Error creating database: {e}")
    else:
        logging.info(f"Database '{db_path}' already exists")

def create_app(config_name='production'):
    app = Flask(__name__)

    db_name = os.getenv('DB_NAME')

    # Set the database name based on the environment
    if config_name == 'testing':
        db_name = 'test' + db_name

    db_uri = f'sqlite:///{db_name}'


    # Ensure the database exists before connecting
    create_database_if_not_exists(db_uri)

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize cache with configuration
    app.config['CACHE_TYPE'] = 'simple'
    app.config['CACHE_DEFAULT_TIMEOUT'] = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))  # Default to 300s if not set
    cache.init_app(app)

    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    init_routes(app)

    setup_logging(app)
    app.logger.info('Flask application started')

    return app
