import pandas as pd
import datetime

from chinese_calendar import is_workday
def interval_date(base_date,start_date,end_date):
    if start_date > end_date:
        return None
    start_date = datetime.datetime.strptime(start_date,"%Y%m%d").date()
    end_date = datetime.datetime.strptime(end_date,"%Y%m%d").date()
    base_date = datetime.datetime.strptime(base_date,"%Y%m%d").date()
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        p_date = datetime.datetime.strftime(current_date,'%Y%m%d')
        date_diff = current_date - base_date
        id = date_diff.days + 1
        year = current_date.year
        month = current_date.month
        day = current_date.day
        week_number_u = int(datetime.datetime.strftime(current_date,"%W")) + 1
        week = '7' if datetime.datetime.strftime(current_date,"%w") == '0' else datetime.datetime.strftime(current_date,"%w")
        is_holiday = '0' if is_workday(current_date) else '1'
        current_date += datetime.timedelta(days=1)
        value = f"({id},{p_date},{year},{month},{day},{week},{week_number_u},{is_holiday})"
        date_list.append(value)
    values = ','.join(date_list)
    return values
    # for date in date_list:
    #     print(date)
    # print(','.join(f"{date_list[0]}"))

# 输出DataFrame




