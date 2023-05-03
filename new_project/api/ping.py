def main(request):
    carwash_id = request.args.get('carwashId')
    box_number = request.args.get('boxNumber')
    print('carwash_id: ', carwash_id)
    print('box_number: ', box_number)

    return carwash_check(box_number)


def carwash_check(box_number):
    if box_number == '1':
        status = 200
        print('status_reply', status)
        return status
    elif box_number == '2':
        status = 200
        print('status_reply', status)
        return status
    elif box_number == '3':
        status = 200
        print('status_reply', status)
        return status
    else:
        status = 401
        print('status_reply', status)
        return status
