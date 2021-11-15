from re import X
from models.models import db
from flask import request


def insert(table='', feilds=[], values=[], where=''):
    values = list(map(lambda v: f'"{v}"', values))
    query = f'INSERT INTO {table} ({",".join(feilds)}) VALUES ({",".join(values)})'
    if where:
        query += f'WHERE {where}'
    db.session.execute(query)
    db.session.commit()


def insert_many(table='', feilds=[], values=[], where=''):
    query = f'INSERT INTO {table} ({",".join(feilds)}) VALUES '

    def object_to_str(obj):
        return ",".join(list(map(lambda v: f'"{v}"', list(obj.values()))))

    str_list = list(map(object_to_str, values))
    for index, text in enumerate(str_list):
        if index != 0:
            query += ", "
        query += f'({text})'
    db.session.execute(query)
    db.session.commit()


def delete(table='', where=''):
    query = f'delete from {table} '
    if where:
        query += f'WHERE {where}'
    db.session.execute(query)
    db.session.commit()


def update(table='', feilds=[], values=[], where=''):
    values = list(map(lambda v, f: f'{f}="{v}"', values, feilds))
    query = f'update {table} set {",".join(values)}'
    if where:
        query += f'WHERE {where}'
    db.session.execute(query)
    db.session.commit()


def select(table='', feilds=[], where='', as_list=False, limit=[]):

    if not feilds:
        feilds = '*'
    else:
        feilds = ','.join(feilds)
        limit = ','.join(limit)
    query = f'SELECT {feilds} FROM {table}'

    if where:
        query += f' WHERE {where}'
    if limit:
        query += f' LIMIT {limit};'
    result = db.session.execute(query)
    if as_list:
        result = result.mappings().all()
    return result


def select_with_join(tables=[], feilds=[], joins=[], where='', as_list=False, limit=[]):
    if not feilds:
        feilds = '*'
    else:
        feilds = ','.join(feilds)
        limit = ','.join(limit)
    query = f'SELECT {feilds} FROM {tables[0]} '
    for i in range(len(joins)):
        query += f'INNER JOIN {tables[i+1]} ON {joins[i]} '
    if where:
        query += f' WHERE {where}'
    if limit:
        query += f' LIMIT {limit};'
    # print(query)
    result = db.session.execute(query)
    if as_list:
        result = result.mappings().all()
    return result
