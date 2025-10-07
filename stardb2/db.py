"""Connection to the database.
"""

import os
import dotenv
import psycopg2 as pg
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

dotenv.load_dotenv()

def get_db_connection(database: str) -> 'connection':
    """Returns a connection to the database, using the parameters specified by the environment
    variables to connect.
    
    The parameter database is the name of the database for which a connection is sought: `development` or `estrous_cycle`.
    """
    url_object = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=database
    )
    engine = create_engine(url_object)
    return engine