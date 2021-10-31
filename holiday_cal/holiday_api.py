""" Depending on a given country-code , month, and year of travel,
the app will display holidays observed in that country during that month. """

import extract_holiday

# method call for dropdown 
def list_of_countries():
    country = extract_holiday.req_res_country()
    return country

def get_holiday(country_name,year,month):
    """ :params: the country_code(upperCase),year and month of travel.
    :returns holday name,description,date """
    country_code = country_code_handler(country_name)
    
    holiday = get_travel_data(country_code,year,month ) #str 

    #if the api response returns holiday[] 
    if holiday is None:
        return 
    else:
        return show_holiday(holiday)


def country_code_handler(country_name):
    """  verifies if the provided country_name matches to any of the countries supported by the API.
    :param:  The country_name to verify.
    :returns: True if a country exists with the provided country_code, else raises NoStateRegion. """
    country_code, is_valid = extract_holiday.is_country_supported(country_name)
    error_message = ''
    if is_valid:
        error_message = 'Valid country'
        return country_code, error_message
    else:
        error_message = 'No country matches the provided country code'
        return None, error_message
             
def get_travel_data(country,year,month):
    """ request holiday data from calendarificAPI.
    :params: country year and month are data the user provided.
    :returns: the national holidays   """
    country_travel =  extract_holiday.get_holiday_data(country,year,month)
    return country_travel
    
def show_holiday(holiday):
    """ display the holiday data. """
    hol = extract_holiday.display_holiday(holiday)
    for key,value in hol.items():
        print(f'{key}: {value}')



get_holiday('united states','2022','12')


#0.002855062484741211 when retrieved from cache
#0.2691211700439453 when retrieved from api
# total= 0.0021638870239257812
