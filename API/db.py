import os
import psycopg2

def create_db_connection():
    """Establishes a database connection using credentials from environment variables.
    :rtype: object
    """
    dbname = os.environ.get('DB_NAME')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    host = os.environ.get('DB_HOST')

    print("successful connection!")

    return psycopg2.connect(dbname=dbname, user=user, password=password, host=host)


