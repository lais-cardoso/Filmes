from datetime import date, timedelta


def calculate_expired_date(current_date: date):
    '''
        Calculates a deadline of 30 days.

            Parameters:
                current_date (date): A current date.

            Returns:
                expired_date (date): A date referring to the sum of the current date plus 30 days.
    '''

    free_sample = timedelta(30)
    unsubscribe_date = current_date + free_sample
    expired_date = unsubscribe_date.strftime('%d/%m/%Y')

    return expired_date


def calculate_difference_day(today_date: date, oscar_date: date):
    """ Subtract two dates

    :args:
        today_date (date): A current date.
        oscar_date (date): Oscar celebration date. 

    :returns The subtraction between the Oscar celebration date and the current date.

    """
    difference = oscar_date - today_date
    difference_day = difference.days

    return difference_day
