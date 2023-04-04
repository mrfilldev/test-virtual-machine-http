import os
import traceback
from flask import Blueprint, request, Response
from . import ping
from .carwash_list import carwash_list_main
from . import create_order
from configuration.config import Config

api_bp = Blueprint(
    'api_blueprint', __name__,
)



@api_bp.route('/carwash/ping')
async def return_carwash_ping():
    apiKey = request.args.get('apikey')
    print('try_apiKey: ' + apiKey)
    print(Config.API_KEY)
    if apiKey in Config.API_KEY:
        status = ping.main(request)
        response = Response(status=status, mimetype="application/json")

    else:
        result = 'Error, Something is wrong...'
        status = 401

        response = Response(result, status=status, mimetype="application/json")
    print(response)
    return response


@api_bp.route('/carwash/list')
async def return_carwash_list():
    try_apiKey = request.args.get('apikey')
    print('try_apiKey: ' + try_apiKey)
    if try_apiKey in Config.API_KEY:
        result = carwash_list_main()
        print(result)
        status = 200
    else:
        result = 'Error, Something is wrong...'
        status = 401
    response = Response(result, status=status, mimetype="application/json")
    return response


@api_bp.route('/carwash/order', methods=['POST'])
async def make_carwash_order():
    try:
        create_order.main(request)
        return Response(status=200)
    except Exception as e:
        # write to log
        traceback.print_exc()
        print(f'caught {type(e)}: e', e)  # добавить логгер
        return Response(status=400)
