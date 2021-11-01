""" Depending on a given country-code , month, and year of travel,
the app will display holidays observed in that country during that month. """

import extract_holiday

# method call for dropdown only 
def list_of_countries():
    country = extract_holiday.req_res_country()
    return None if country == None else country

def get_holiday(country_name,year,month):
    """ :params: the country_code(upperCase),year and month of travel.
    :returns holday name,description,date """
    country_code = country_code_handler(country_name)
    if country_code == None:
        return None
    else:
        holiday = get_travel_data(country_code,year,month ) #str
        return show_holiday(holiday) 
    

def country_code_handler(country_name):
    """  verifies if the provided country_name matches to any of the countries supported by the API.
    :param:  The country_name to verify.
    :returns: True if a country exists with the provided country_code, else raises NoStateRegion. """
    country_code = extract_holiday.is_country_supported(country_name)
    return country_code

             
def get_travel_data(country,year,month):
    """ request holiday data from calendarificAPI.
    :params: country year and month are data the user provided.
    :returns: the national holidays   """
    country_travel =  extract_holiday.get_holiday_data(country,year,month)
    return country_travel


def show_holiday(holiday):
    """ display the holiday data. """
    if holiday != None:
        hol = extract_holiday.display_holiday(holiday)
        print(hol)
    else:
        print('No data found')
        return None




