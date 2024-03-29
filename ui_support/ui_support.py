import calendar
import json

def add_error_to_error_list(error, error_list):
    """Takes an error and error_list
    Appends error to error_list if it is not None
    Returns modified error list."""
    if error:
        error_list.append(error)
    return error_list


def check_if_coordinates(coordinates):
    """Return an error message if coordinates were not retrieved from the API."""
    if coordinates == None:
        return None, 'Error getting location information from API. Please double check city name and country and try again.'
    else:
        return coordinates, None


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
    if not date:
        return None, None, 'Error: No date was selected.'
    date_list = date.split('-')
    month = date_list[1]
    year = date_list[0]

    return month, year, None


def get_name_of_month_from_number(month_string):
    """Take number string month as param.
    Return name of month using calendar."""
    error = (None, 'Error: Month needs to be a whole number 1-12.')
    month = str(month_string)
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


# https://www.tutorialspoint.com/How-to-convert-a-string-to-dictionary-in-Python
def create_holidays_list_from_database_favorite(holidays_string):
    """Take the string from the holidays entry in database.
    Turn it into a usable format for result.html"""
    if not holidays_string:
        return None
    elif holidays_string == 'None':
        return None
    else:
        holidays_string_json_compatible = holidays_string.replace('\'', '\"') # json wants double quotes, not single quotes
        holidays_json = json.loads(holidays_string_json_compatible)
        return holidays_json



def create_weather_dict_from_database_favorite(weather_string): 
    """Take the string from the weather entry in database.
    Turn it into a usable format for result.html"""
    if not weather_string:
        return None
    elif weather_string == 'None':
        return None
    else:
        weather_string_json_compatible = weather_string.replace('\'', '\"')
        weather_json = json.loads(weather_string_json_compatible)
        return weather_json


def create_webcams_list_from_database_favorite(webcams_string):
    """Take the string from the webcam entry in database.
    Turn it into a usable list for result.html"""
    if not webcams_string:
        return None
    elif webcams_string == 'None':
        return None
    else:
        webcams_string_json_compatible = webcams_string.replace('\'', '\"')
        webcams_list = json.loads(webcams_string_json_compatible)
        return webcams_list
