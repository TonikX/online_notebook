from .fetcher import fetch
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from rest_framework.exceptions import APIException


def execute_solution(db_name, sql_solution):
    print('db_name - на этапе запуска сервера мускула', db_name)
    sql = 'use {};'.format(db_name)
    #print('на этом этапе используем базу данных', sql)
    sql += sql_solution + ';'
    #print('на этом этапе проверяем запрос целиком', sql)
    success, data, error = fetch(sql)
    #print('на этом этапе проверяем сработал ли запрос на использование бд', success, data, error)

    if success:
        return data
        #print ('данные из базы вренулись')
    else:
        raise APIException({'stacktrace': error})
        #print ('апиэксепшн сработал')
        #esponse = exception_handler(exc, context)

        # return Response({
        #     #'status': 'error',
        #     'error_text': 'sdsd',
        # })
