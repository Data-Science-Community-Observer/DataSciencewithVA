# print start_date to till date, where till date is not define

from datetime import datetime, timedelta
start_date = "20230101"
format = "%Y%m%d"
def dates_till_now(start_date,format):
  current_date = datetime.strptime(start_date, format).date()
  today = datetime.now().date()
  while current_date <= today:
    print(current_date.strftime(format))
    current_date += timedelta(days=1)
    
dates_till_now(start_date,format)