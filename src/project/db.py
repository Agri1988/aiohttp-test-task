import aiopg
import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, ForeignKey
)
from sqlalchemy import ForeignKeyConstraint

meta = MetaData()

employee = Table(
    'employee', meta,

    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    Column('surname', String(100), nullable=False),
    Column('patronymic', String(100), nullable=False),
    Column('sex', String(100), nullable=False),
)

car = Table(
    'car', meta,

    Column('id', Integer, primary_key=True),
    Column('model', String(100), nullable=False),
    Column('year', Integer, nullable=False),
)

spares = Table(
    'spares', meta,

    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    Column('country', String(100), nullable=False),
    Column('car_id', Integer, ForeignKey('car.id', ondelete='CASCADE')),
)


async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port']
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()