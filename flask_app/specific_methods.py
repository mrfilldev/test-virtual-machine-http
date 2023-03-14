import re


def is_valid_guid(guid_string):
    print(guid_string)
    #  pattern = r'^\b[A-Fa-f0-9]{8}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{12}\b$' не сработало?!
    # return bool(re.match(pattern, guid_string))

    if len(guid_string) == 32:
        return True
    else:
        return False


def method_of_filters(request):
    for i in request.form:
        print(i)
    result = {}
    if request.form['search_field'] != '' and request.form['status'] != '': #  1 1
        if is_valid_guid(request.form['search_field']):
            print('is_guid')
            print('search_field & status')
            result = {
                'Id': request.form['search_field'],
                'Status': request.form['status']
                # 'DateCreate': {'$gt': start_time.isoformat()}
            }

        else:
            print('not_guid')
            print('search_field & status')

            result = {
                'CarWashId': request.form['search_field'],
                'Status': request.form['status']
                # 'DateCreate': {'$gt': start_time.isoformat()}
            } #
    elif request.form['search_field'] == '' and request.form['status'] != '':
        print('only status')
        result = {
            'Status': request.form['status']
            # 'DateCreate': {'$gt': start_time.isoformat()}
        }
    elif request.form['search_field'] != '' and request.form['status'] == '':
        print('only search_field')
        result = {
            'CarWashId': request.form['search_field'],
            # 'DateCreate': {'$gt': start_time.isoformat()}
        }
    print('search_field', request.form['search_field'])
    print('status', request.form['status'])
    return result
