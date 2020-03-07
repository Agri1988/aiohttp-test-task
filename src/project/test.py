import json

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from sqlalchemy import create_engine, MetaData

from aiohttp import web
from aiohttp.web_request import Request

from settings_test import config
from routes import setup_routes
from db import employee, car, spares, init_pg, close_pg


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[employee, car, spares])


def drop_tables(engine):
    meta = MetaData()
    meta.drop_all(bind=engine, tables=[employee, car, spares])


db_url = DSN.format(**config['postgres'])
engine = create_engine(db_url)


class EmployeeTestCase(AioHTTPTestCase):
    @classmethod
    def setUpClass(cls):
        pass

    async def get_application(self):
        create_tables(engine)

        app = web.Application()
        setup_routes(app)
        app['config'] = config
        app.on_startup.append(init_pg)
        app.on_cleanup.append(close_pg)
        return app

    @unittest_run_loop
    async def test_index(self):
        response = await self.client.request('GET', '/')
        assert 'Index' in await response.text()

    @unittest_run_loop
    async def test_employee_create(self):
        first_employee = json.dumps({
            'name': 'Vasili',
            'surname': 'Kukushkin',
            'patronymic': 'Vasilievich',
            'sex': 'mail'
        })
        second_employee = json.dumps({
            'name': 'Sergei',
            'surname': 'Semenov',
            'patronymic': 'Petrovich',
            'sex': 'mail'
        })
        third_employee = json.dumps({
            'name': 'Petr',
            'surname': 'Ivanov',
            'patronymic': 'Semenovich',
            'sex': 'mail'
        })
        await self.client.request('POST', '/employee/', data=first_employee)
        await self.client.request('POST', '/employee/', data=second_employee)
        response = await self.client.request('POST', '/employee/', data=third_employee)
        assert 201 == response.status

        response_data = await response.json()
        new_employee_id = response_data['id']
        async with self.app['db'].acquire() as conn:
            cursor = await conn.execute(employee.select().where(employee.c.id == new_employee_id))
            record = await cursor.fetchone()
            assert record[1] == 'Petr'

    @unittest_run_loop
    async def test_employee_update(self):
        new_employee = json.dumps({
            'name': 'Irina',
            'surname': 'Petrova',
            'patronymic': 'Vasilievna',
            'sex': 'female'
        })
        response = await self.client.request('PUT', '/employee/1/', data=new_employee)
        assert 200 == response.status

        response_data = await response.json()
        assert 'Irina' == response_data['name']
        assert 'Petrova' == response_data['surname']
        assert 'Vasilievna' == response_data['patronymic']
        assert 'female' == response_data['sex']

    @unittest_run_loop
    async def test_get_exist_employees(self):
        response = await self.client.request('GET', '/employee/1/')
        employee = await response.json()
        assert 200 == response.status
        assert 'Irina' == employee.get('name')

    @unittest_run_loop
    async def test_try_to_get_not_exist_employee(self):
        response = await self.client.request('GET', '/employee/111/')
        response_text = await response.text()
        assert 406 == response.status
        assert 'ObjectDoesNotExist' in response_text

    @unittest_run_loop
    async def test_get_all_employee(self):
        response = await self.client.request('GET', '/employee/')
        employee_list = await response.json()
        assert 200 == response.status
        assert 3 == len(employee_list)

    @unittest_run_loop
    async def test_get_filter_employees(self):
        response = await self.client.request('GET', '/employee/?field=sex&search_data=mail')
        employee_list = await response.json()
        assert 200 == response.status
        assert 2 == len(employee_list)

    @classmethod
    def tearDownClass(cls):
        drop_tables(engine)