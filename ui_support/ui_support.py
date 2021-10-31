import calendar

def get_list_of_countries(country_api_response):
    """Gets list of countries and country codes from the country_api in holiday_cal
    Pulls just the country names out, puts them in a list, then returns that list."""
    if not country_api_response:
        return None, 'No response from Calendarific API for country names.'

    country_name_list = []
    for country_name_and_code in country_api_response:
        country_name_list.append(country_name_and_code['country_name'])
    return country_name_list, None


def get_list_of_webcam_categories(webcam_api_response):
    """Checks if response is None or if it has data.
    If data, returns data, None.
    If None, returns None, error."""
    if not webcam_api_response:
        return None, 'No response from Windy API for webcam categories.'
    return webcam_api_response, None


def get_month_and_year_from_date(date):
    """Takes a date in the HTML datepicker format as param.
    Returns just the month and year from that date as tuple."""
    date_list = date.split('/')
    month = date_list[0]
    year = date_list[2]

    return month, year


def get_name_of_month_from_number(month):
    """Take number string month as param.
    Return name of month using calendar."""
    error = (None, 'Error: Month needs to be a whole number 1-12.')
    if month.isnumeric() == False:
        return error

    month_int = int(month)

    if (1 <= month_int <= 12) == False:
        return error

    month_name_to_return = calendar.month_name[month_int]
    return month_name_to_return, None



def create_result_dictionary(city, country, month, month_name, year, webcams, holidays, weather):
    """Return a dictionary from params."""
    result = {
        'city': city,
        'country': country,
        'month': month,
        'month_name': month_name,
        'year': year,
        'webcams': webcams,
        'holidays': holidays,
        'weather': weather
    }
    return result