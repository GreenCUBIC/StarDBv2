import os
import dotenv
import psycopg2 as pg

dotenv.load_dotenv()


def get_db_connection(database):
    return pg.connect(
        f"dbname='{database}' user='{os.getenv('DB_USER')}' host='{os.getenv('DB_HOST')}' port='{os.getenv('DB_PORT')}' password='{os.getenv('DB_PASSWORD')}'"
    )

