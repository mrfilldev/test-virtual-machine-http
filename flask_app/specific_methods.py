import re


def is_valid_guid(guid_string):
    print(guid_string)
    pattern = r'^\b[A-Fa-f0-9]{8}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{12}\b$'
    return bool(re.match(pattern, guid_string))


def method_of_filters(request):
    result = {}
    if request.form['search_field'] != '':
        if is_valid_guid(request.form['search_field']):
            # искать среди order.Status
            # искать среди order.Date
            # искать среди order.Id
            print('TRUE')
            result = {
                'Id': request.form['search_field'],
                # 'DateCreate': {'$gt': start_time.isoformat()}
            }

        else:
            print('FALSE')
            # искать среди order.CarWashId
            # искать среди order.Status
            # искать среди order.Date
            result = {
                'CarWashId': request.form['search_field'],
                # 'DateCreate': {'$gt': start_time.isoformat()}
            }
    else:
        result = {
            # 'DateCreate': {'$gt': start_time.isoformat()}
        }

    return result
