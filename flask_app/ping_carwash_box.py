def main(request):
    carwash_id = request.args.get('carwashId')
    box_number = request.args.get('boxNumber')
    print('carwash_id: ', carwash_id)
    print('box_number: ', box_number)
    if carwash_id == '1':
        return carwash_id_1(box_number)
    if carwash_id == '2':
        return carwash_id_2(box_number)


def carwash_id_1(box_number):
    if box_number == '1':
        status = 200
        print('status_reply',  status)
        return status
    elif box_number == '2':
        status = 404
        print('status_reply',  status)
        return status


def carwash_id_2(box_number):
    if box_number == '1':
        status = 200
        print('status_reply',  status)
        return status
    elif box_number == '2':
        status = 404
        print('status_reply',  status)
        return status
