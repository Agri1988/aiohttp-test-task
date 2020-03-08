import json

from aiohttp import web
from aiopg.sa.result import ResultProxy
from multidict import MultiDictProxy
from aiohttp.web_request import Request
import aiohttp_jinja2
import db


@aiohttp_jinja2.template('index.html')
async def index(request):
    pass


# ABSTRACT GET LIST OBJECT
async def list_object(request, object_name, raw_query: str=None):
    async with request.app['db'].acquire() as conn:
        query = getattr(db, object_name).select()
        if raw_query is not None:
            query = raw_query
        cursor = await conn.execute(query)
        records = await cursor.fetchall()
        objects = [dict(q) for q in records]
        return web.json_response(status=200, data=objects)


# FILTER OBJECTS BY FIELD
async def filter_object_by_field(request: Request, object_name: str, object_field: str,
                                 search_data: str, raw_query: str=None):
    async with request.app['db'].acquire() as conn:
        try:
            model = getattr(db, object_name)
            field = getattr(model.c, object_field)
            query = model.select().where(field == search_data)
            if raw_query is not None:
                query = raw_query + f'WHERE {object_name}.{field}={search_data}'
            cursor: ResultProxy = await conn.execute(query)
            records = await cursor.fetchall()
            objects = [dict(q) for q in records]
            return web.json_response(status=200, data=objects)
        except AttributeError:
            return web.json_response(status=412, text='ObjectDoesNotContainsRequestField')


# HANDLER SELECTOR BASED ON QUERY CONTENT
async def handler_selector(request, object_name: str, raw_query: str=None):
    params: MultiDictProxy = request.query
    field = params.get('field')
    search_data = params.get('search_data')
    if all((field, search_data)):
        return await filter_object_by_field(
            request,
            object_name=object_name,
            object_field=field,
            search_data=search_data
        )
    else:
        return await list_object(request, object_name=object_name, raw_query=raw_query)


# ABSTRACT GET OBJECT BY ID
async def get_object(request, object_name):
    object_id: str = request.match_info['id']
    if object_id.isdigit():
        async with request.app['db'].acquire() as conn:
            model = getattr(db, object_name)
            cursor = await conn.execute(model.select().where(model.c.id == object_id))
            record = await cursor.fetchall()
            if len(record) == 1:
                return web.json_response(status=200, data=dict(record[0]))
            elif len(record) > 1:
                return web.Response(status=406, text='MultipleObjectsReturned')
            else:
                return web.Response(status=406, text='ObjectDoesNotExist')
    else:
        return web.Response(status=412, text='WrongRequestParam')


# CREATE ABSTRACT OBJECT BY ID
async def create_object(request, object_name):
    async with request.app['db'].acquire() as conn:
        new_object: dict = await request.json()
        cursor = await conn.execute(getattr(db, object_name).insert().values(**new_object))
        record = await cursor.fetchone()
        if record:
            new_object: dict = dict(new_object.items())
            new_object['id'] = record[0]
            return web.json_response(status=201, data=new_object)
        else:
            return web.Response(status=400, text='ObjectSaveError')


# UPDATE ABSTRACT OBJECT BY ID
async def update_object(request: Request, object_name: str):
    object_id: str = request.match_info['id']
    if object_id.isdigit():
        async with request.app['db'].acquire() as conn:
            update_object: dict = await request.json()
            cursor: ResultProxy = await conn.execute(getattr(db, object_name).update().
                                        values(**update_object).
                                        where(getattr(db, object_name).c.id == object_id))

            if cursor.rowcount == 1:
                return web.json_response(status=200, data=update_object)
            else:
                return web.Response(status=400, text='ObjectUpdateError')
    else:
        return web.Response(status=412, text='WrongRequestParam')


# Employee API
# GET EMPLOYEE LIST
async def list_employee(request):
    return await handler_selector(request, 'employee')


# GET EMPLOYEE INSTANCE
async def get_employee(request):
    return await get_object(request, object_name='employee')


# CREATE EMPLOYEE INSTANCE
async def create_employee(request):
    return await create_object(request, object_name='employee')


# UPDATE EMPLOYEE INSTANCE
async def update_employee(request):
    return await update_object(request, object_name='employee')


# Car API
# GET CAR LIST
async def list_car(request):
    return await handler_selector(request, object_name='car')


# GET CAR INSTANCE
async def get_car(request):
    return await get_object(request, object_name='car')


# CREATE CAR INSTANCE
async def create_car(request):
    return await create_object(request, object_name='car')


# UPDATE CAR INSTANCE
async def update_car(request):
    return await update_object(request, object_name='car')


# SPARES API
# GET SPARES LIST
async def list_spares(request):
    return await handler_selector(request, object_name='spares')


# GET SPARES LIST WITH CAR
async def list_spares_with_car(request):
    raw_query = """
SELECT spares.id, spares.name, spares.car_id, spares.country, (car.model || ' ' || car.year) as car_model FROM spares 
  LEFT JOIN car on spares.car_id = car.id """
    return await handler_selector(request, 'spares', raw_query=raw_query)


# GET SPARES INSTANCE
async def get_spares(request):
    return await get_object(request, object_name='spares')


# CREATE SPARES INSTANCE
async def create_spares(request):
    return await create_object(request, object_name='spares')


# UPDATE SPARES INSTANCE
async def update_spares(request):
    return await update_object(request, object_name='spares')
