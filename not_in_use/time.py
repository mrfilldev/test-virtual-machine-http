from datetime import datetime, timedelta, date
string = '2023-02-27T14:24:49.215Z'

result = string.replace('T', ' ')
print(result)
result = result.replace('Z', '')
print(result)

start_time = datetime.now() - timedelta(minutes=15)

print(start_time)

#
#
#
#
# start_time = datetime.now() - timedelta(minutes=15)
# current_day = date.today()
# print(current_day)
# print(start_time)
# print(start_time.time())
