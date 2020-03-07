import psycopg2
from project.settings import config
from init_db import create_tables, create_engine, sample_data

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}".format(**config['postgres'])
try:
    conn = psycopg2.connect(DSN)
    conn.close()
    try:
        engine = create_engine(DSN)
        create_tables(engine)
        sample_data(engine)
    except:
        pass
except psycopg2.OperationalError:
    raise