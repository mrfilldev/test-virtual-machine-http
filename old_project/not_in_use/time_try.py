import time
from datetime import datetime, timedelta, date
from dateutil import parser

# format = '%Y-%m-%dT%H:%M:%S%Z'
# date_now = datetime.strptime(time.strftime(format, time.localtime()), format)
# print(date_now)

"""string = '2023-02-27T14:24:49.215Z'

value = parser.parse(string)
print(value)
value = value.strftime("%m/%d/%y %H:%M:%S")
print(value)
"""

# # определение временного диапазона
# start_time = datetime.now() - timedelta(minutes=15)
# end_time = datetime.now()
# print(start_time.strftime('%H:%M:%S'))
# print(end_time.strftime('%H:%M:%S'))
#
# start_time = datetime.strftime(start_time, "%Y-%m-%dd %H:%M:%S")
#
#


# result = string.replace('T', ' ')
# print(result)
# result = result.replace('Z', '')
# print(result)
#
# start_time = datetime.now() - timedelta(minutes=15)
#
# print(start_time)

#
#
#
#
# start_time = datetime.now() - timedelta(minutes=15)
# current_day = date.today()
# print(current_day)
# print(start_time)
# print(start_time.time())


# extended_date = datetime.now().strftime("%d-%m-%YT%H:%M:%SZ")
# extended_date = datetime.now().isoformat(timespec='microseconds')
# print(extended_date)
#
# now = datetime.now()
#
# # Преобразуем время в формат ISO8601
# iso_time = now.isoformat()
#
# print(iso_time)


# date_str = '2023-05-04'
# time_start = '17:01'
# time_end = '18:01'
# test = date_str + 'T' + time_start + 'Z'
# d1 = datetime.strptime(test, "%Y-%m-%dT%H:%MZ")
# print(d1)
# print(type(d1))
#
#
# print(d1.isoformat())
