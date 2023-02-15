# print(json.loads(request.data, default=lambda x: x.__dict__))

# new_order = Order(data.I
# d)
# print(type(new_order.Status.name))
# print(new_order.Status.name)
# print(type(new_order.Status.value))
# print(data)


# url = URL_DEV + "/api/carwash/order/completed"
# data = {
#     "apikey": API_KEY,
#     "orderId": data.Id,
#     "sum": data.Sum,
#     "extendedOrderId": extended_order_id,
#     "extendedDate": extended_date
# }
# headers = {'content-type': 'application/json'}
# requests.post(url, data=data, headers=headers)

# print('data: ', data)
# response = urllib.request.urlopen(url)
# data = response.read()
# dict = json.loads(data)
# print('dict: ', dict)

#  response = urllib.request.urlopen(url)
# data = response.read()
# dict = json.loads(data)
# print('dict: ', dict)
# task2 = asyncio.create_task(send_completed_status(id, sum))

# print('data: ', data)

# task1 = asyncio.create_task(send_accept_status(data.Id, data.Sum))
# print('Task done?')

# self.Services = Services(services[0].Id, services[0].Description, services[0].Cost)
# data = json.loads(request.data, object_hook=lambda d: custom_decoder(**d))

# data = {
#     "apikey": API_KEY,
#     "orderId": data.Id,
# }
#
# headers = {'content-type': 'application/json'}
# requests.post(url, data=data, headers=headers)
