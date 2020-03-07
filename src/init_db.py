from sqlalchemy import create_engine, MetaData

from project.settings import config
from project.db import employee, car, spares


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"

tables = (
    employee,
    car,
    spares
)

def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=tables)


def sample_data(engine):
    conn = engine.connect()
    for table in tables:
        query = conn.execute("SELECT COUNT(id) FROM {}".format(table))
        count = query.fetchone()
        if count[0]:
            return
    conn.execute(employee.insert(), [
        {
            'name': 'John',
            'surname': 'Doe',
            'patronymic': 'Sam son',
            'sex': 'male'
        },
        {
            'name': 'Jane',
            'surname': 'Doe',
            'patronymic': 'Sam daughter',
            'sex': 'female'
        },
        {
            'name': 'Some',
            'surname': 'Person',
            'patronymic': 'Undefined',
            'sex': 'undefined'
        },
    ])
    conn.execute(car.insert(), [
        {
            'model': 'Ford Mustang',
            'year': 2020,
        },
        {
            'model': 'Chevrolet Camaro',
            'year': 2010,
        },
        {
            'model': 'Chevrolet Impala',
            'year': 1967,
        },
        {
            'model': 'VAZ 2101',
            'year': 1970,
        },
    ])
    conn.execute(spares.insert(), [
        {
            'name': 'Wheel 15" x 7"',
            'country': 'USA',
            'car_id': 3
        },
        {
            'name': 'Front brake rotor',
            'country': 'Japan',
            'car_id': 3
        },
        {
            'name': 'Engine 1.2',
            'country': 'USSR',
            'car_id': 4
        },
    ])
    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)