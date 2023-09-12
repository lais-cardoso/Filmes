from datetime import date, timedelta

def calculate_expired_date(current_date: date):
    # index route calculation
    free_sample = timedelta(30)
    unsubscribe_date = current_date + free_sample
    expired_date = unsubscribe_date.strftime('%d/%m/%Y')

    return expired_date

def calculate_difference_day(current_date: date, oscar_date: date):
    # home route calculation
    difference = oscar_date - current_date
    difference_day = difference.days

    return difference_day