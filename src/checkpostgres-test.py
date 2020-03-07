import psycopg2
from project.settings_test import config

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}".format(**config['postgres'])
try:
    conn = psycopg2.connect(DSN)
    conn.close()
except psycopg2.OperationalError:
    raise