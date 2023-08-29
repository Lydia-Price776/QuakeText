import psycopg2
from sqlalchemy import create_engine, URL
import time
from prepare_quaketext_data import read_data

from embeddings_retrevial import run

from configDB import config

start = time.time()

cursor = None
connection = None


def connect():
    params = config()
    url = create_url(params)
    print('Connecting to PostgreSQL Database')
    conn = psycopg2.connect(**params)
    return conn, conn.cursor(), url


# Creates a url from the config file parameters
def create_url(params):
    url_object = URL.create(
        "postgresql+psycopg2",
        username=params['user'],
        password=params['password'],
        host=params['host'],
        database=params['database'],
    )
    return url_object


try:
    connection, cursor, url = connect()
    engine = create_engine(url)
    conn_engine = engine.connect()
    connection.autocommit = True
    run(conn_engine)
    """ Code for prepare_quake_text.py
    data = read_data(conn_engine)
    data.reset_index(drop=True, inplace=True)
    data.to_csv("quake_text_for_eval.csv", index=False)
    """


except(Exception, psycopg2.DatabaseError) as error:
    print(error)

finally:
    if cursor is not None:
        cursor.close()
        print('Cursor connection Terminated')
    if connection is not None:
        connection.close()
    print('Database connection Terminated')
    end = time.time()
    total = end - start
    print("Total Time taken: ")
    print(total)