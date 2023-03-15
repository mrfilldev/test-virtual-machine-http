import json


def get_code(request):
    code = request.args.get('code')
    state = request.args.get('state')

    print(code, state)
