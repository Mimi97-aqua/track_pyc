from dotenv import load_dotenv
import psycopg2
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'heic'}

load_dotenv()


def allowed_file(filename):
    """
    Checks if the uploaded profile photo has an allowed extension.

    Args:
        filename (string): The name of the file to check.

    Returns:
        bool: True if the uploaded profile photo has an allowed extension, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db_connection():
    """
    Establishes a database connection to the PostgreSQL database using credentials from the environment variables.
    """
    db_params = {
        'db_name': os.getenv('db_name'),
        'db_user': os.getenv('db_user'),
        'db_password': os.getenv('db_password'),
        'db_host': os.getenv('db_host'),
        'port': os.getenv('db_port'),
    }
    return psycopg2.connect(**db_params)


def close_db_connection():
    """
    Closes the database again at the end of execution.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    conn.commit()
    cursor.close()
    conn.close()