# import time
# from time import gmtime
# from datetime import datetime, timedelta, date
# from dateutil import parser
#
# # format = '%Y-%m-%dT%H:%M:%S%Z'
# # date_now = datetime.strptime(time.strftime(format, time.localtime()), format)
# # print(date_now)
#
# """string = '2023-02-27T14:24:49.215Z'
#
# value = parser.parse(string)
# print(value)
# value = value.strftime("%m/%d/%y %H:%M:%S")
# print(value)
# """
#
# # # определение временного диапазона
# # start_time = datetime.now() - timedelta(minutes=15)
# # end_time = datetime.now()
# # print(start_time.strftime('%H:%M:%S'))
# # print(end_time.strftime('%H:%M:%S'))
# #
# # start_time = datetime.strftime(start_time, "%Y-%m-%dd %H:%M:%S")
# #
# #
#
#
# # result = string.replace('T', ' ')
# # print(result)
# # result = result.replace('Z', '')
# # print(result)
# #
# # start_time = datetime.now() - timedelta(minutes=15)
# #
# # print(start_time)
#
# #
# #
# #
# #
# # start_time = datetime.now() - timedelta(minutes=15)
# # current_day = date.today()
# # print(current_day)
# # print(start_time)
# # print(start_time.time())
#
#
# # extended_date = datetime.now().strftime("%d-%m-%YT%H:%M:%SZ")
# # extended_date = datetime.now().isoformat(timespec='microseconds')
# # print(extended_date)
# #
# # now = datetime.now()
# #
# # # Преобразуем время в формат ISO8601
# # iso_time = now.isoformat()
# #
# # print(iso_time)
#
#
# # date_str = '2023-05-04'
# # time_start = '17:01'
# # time_end = '18:01'
# # test = date_str + 'T' + time_start
# # d1 = datetime.strptime('2023-04-12T14:42:06.368', "%Y-%m-%dT%H:%M:%S.%f")
# # print(d1)
# # print(type(d1))
# #
# #
# # print(d1.isoformat())
#
# format = '%Y-%m-%dT%H:%M:%S%Z'
# date_now = datetime.strptime(time.strftime(format, time.localtime()), format)
# print(date_now)
# print(time.strftime(format, time.localtime()) + ' ' + " flv dfivjfv")
# print(time.localtime())
# print("попытка изменения тайм зоны")
# print("2023-06-27 14:05")
# print("2023-06-27 16:05")
#
# date_created = datetime.now().isoformat()
# print(date_created)
#
# dt_utcnow = datetime.utcnow().isoformat()
# print(dt_utcnow)
# date_start_iso = datetime.strptime("2023-06-27" + ' ' + "14:05", "%Y-%m-%d %H:%M").isoformat()
# print(date_start_iso, type(date_start_iso))
#
# print("\n################################\n")
# date_start = datetime.strptime("2023-06-27" + 'T' + "14:05", "%Y-%m-%dT%H:%M")
# print(type(date_start), date_start)
#
# own = parser.parse("2023-06-27T12:22:26+03:00")
# print(type(own), own)
# yaru = parser.parse("2023-06-27T12:22:26.809Z")
# print(type(yaru), yaru)
#
# '''
# OWN:   DateCreate='2023-06-23T12:54:03.722884', DateStart='2023-06-23T12:53:00', DateEnd='2023-06-23T13:53:00'
# YARU:  DateCreate='2023-06-27T12:22:26.809Z'
# '''
# print("\n################################\n")
# test_own = parser.parse("2023-06-23T12:54:03.722884Z")
# test_yaru = parser.parse("2023-06-27T12:22:26.809Z")
# utc_now = parser.parse(datetime.utcnow().isoformat() + "Z")
# print(type(utc_now), utc_now, utc_now.strftime('%H:%M'))
# print(type(test_own), test_own, test_own.strftime('%H:%M'))
# print(type(test_yaru), test_yaru, test_yaru.strftime('%H:%M'))
# print("\n################################\n")
#
# test_string = parser.parse("2023-06-27T12:31:31.968705")
# print(type(test_string), test_string, test_string.strftime('%H:%M'))
# test_string = parser.parse("2023-06-27T12:31:31.968705") + timedelta(hours=3)
# print(type(test_string), test_string, test_string.strftime('%H:%M'))
# print("\n################################\n")
#
# time_value = parser.parse("2023-06-27T12:31:31.968705") + timedelta(hours=3)
# print(time_value.isoformat())
#
# print("\n################################\n")
#
#
# def convert_string_to_utc(value, timezone=3):
#     time_value = parser.parse(value) - timedelta(hours=timezone)
#     return time_value.isoformat()
#
#
# def convert_string_to_timezone(value, timezone=3):
#     time_value = parser.parse(value) + timedelta(hours=timezone)
#     return time_value.isoformat()
#
#
# def checking():
#     date_start = datetime.strptime("2023-06-27" + 'T' + "18:12", "%Y-%m-%dT%H:%M")
#     print(type(date_start), date_start)
#     date_start = convert_string_to_utc(date_start.isoformat()) + "+03:00"
#     print(type(date_start), date_start)


def print_utc_time():
    from datetime import datetime, timezone
    print(datetime.now(timezone.utc))


print_utc_time()

