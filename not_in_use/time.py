from datetime import datetime, timedelta, date

start_time = datetime.now() - timedelta(minutes=15)
current_day = date.today()
print(current_day)
print(start_time)
print(start_time.time())
