import os
import traceback
from flask import Blueprint, request, Response
from . import ping
from .carwash_list import carwash_list_main
from ..config import Config

api_bp = Blueprint(
    'api_blueprint', __name__,
)

API_KEY = Config.API_KEY


@api_bp.route('/carwash/ping')
async def return_carwash_ping():
    apiKey = request.args.get('apikey')
    print('try_apiKey: ' + apiKey)

    if apiKey in API_KEY:
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
    if try_apiKey in API_KEY:
        # result = carwash_list.main(request)
        result = carwash_list_main()
        status = 200
    else:
        result = 'Error, Something is wrong...'
        status = 401
    response = Response(result, status=status, mimetype="application/json")
    return response


@api_bp.route('/carwash/order', methods=['POST'])
@api_bp.route('/tanker/order', methods=['POST'])
async def make_carwash_order():
    try:
        # carwash_order.main(request)
        return Response(status=200)
    except Exception as e:
        # write to log
        traceback.print_exc()
        print(f'caught {type(e)}: e', e)  # добавить логгер
        return Response(status=400)
