from sqlalchemy import create_engine, MetaData

from project.settings import config
from project.db import employee, car, spares


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[employee, car, spares])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(employee.insert(), [
        {
            'name': 'John',
            'surname': 'Doe',
            'patronymic': 'Ivanovich',
            'sex': 'mail'
        }
    ])
    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)