import psycopg2
from project.settings import config
from init_db import create_tables, create_engine

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}".format(**config['postgres'])
try:
    conn = psycopg2.connect(DSN)
    conn.close()
    try:
        db_url = DSN.format(**config['postgres'])
        engine = create_engine(db_url)
        create_tables(engine)
    except:
        pass
except psycopg2.OperationalError:
    raise