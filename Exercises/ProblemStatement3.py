# 3. Create a python function which accept 1 argument (Start Date) and print all the dates till date (Till date should be today's date). Excluding Saturday and Sunday. Generate URL from these dates. Save to an excel.

# import necessary library
from datetime import datetime, timedelta
import pandas as pd
from IPython.display import FileLink

# function to generate URL from the current date
def generate_url(current_date):
    # formatted url syncronized with the current date using concatenation
    url = f"https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_{current_date}_F_0000.csv.zip"
    return url


# initiate variable
start_date = "20230101"

# function to generate dates till now excluding weekdays
def dates_till_now(start_date):
    format = "%Y%m%d"
    # initilize URL list
    urls = []
    # generate current date initiate from 2023/01/01
    current_date = datetime.strptime(start_date, format).date()
    # present date
    today = datetime.now().date()
    # loop for printing URL for each date
    while current_date <= today:
        # excluding weekdays
        if current_date.weekday() != 5 and current_date.weekday() != 6:
            # current date updation in url
            url = generate_url(current_date.strftime(format))
            urls.append({"URL": url})
        # next current date  
        current_date += timedelta(days=1)
    # create url's dataframe 
    nse_data_urls = pd.DataFrame(urls)
    # create excel file name
    excel_file = "./Exercises/assets/nse_data_urls.xlsx"
    # convert dataframe to excel
    nse_data_urls.to_excel(excel_file, index=False)
    

dates_till_now(start_date)