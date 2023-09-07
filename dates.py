#arquivo para colocar as funções
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
import os

oscar_environment_variable = f"{os.environ['OSCAR_DATE']}"

oscar_date = datetime.strptime(oscar_environment_variable, "%Y/%m/%d")

def calculate_expired_date(current_date):
    # index route calculation
    free_sample = timedelta(30)
    unsubscribe_date = current_date + free_sample
    expired_date = unsubscribe_date.strftime('%d/%m/%Y')

    return expired_date

def calculate_difference_day(current_date):
    # home route calculation
    difference = oscar_date - current_date
    difference_day = difference.days

    return difference_day