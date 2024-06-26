# 2. Create a python function which accept 1 argument (Start Date) and print all the dates till date (Till date should be today's date). Excluding Saturday and Sunday.
from datetime import datetime, timedelta
start_date = "20230101"
format = "%Y%m%d"
def dates_till_now(start_date,format):
  current_date = datetime.strptime(start_date, format).date()
  today = datetime.now().date()
  while current_date <= today:
    if current_date.weekday() != 5 and current_date.weekday() != 6:
      print(current_date.strftime(format))
    current_date += timedelta(days=1)

dates_till_now(start_date,format)