""" Depending on a given country-code , month, and year of travel,
the app will display holidays observed in that country during that month. """

import extract_holiday


def get_holiday(country,year,month):
    """ :params: the country_code(upperCase),year and month of travel.
    :returns holday name,description,date """
    check_country_code = country_code_handler(country)
    if check_country_code:
        holiday = get_travel_data(country,year,month ) #str 
    #if the api response returns holiday[] 
    if holiday is None:
        print ('There is no national holiday for this month')
    else:
        return show_holiday(holiday)


def country_code_handler(country_code):
    """  verifies if the provided country_code matches to any of the countries supported by the API.
    :param:  The country code to verify.
    :returns: True if a country exists with the provided country_code, else raises NoStateRegion. """
    country_list = extract_holiday.is_country_supported(country_code)
    return country_list
             
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



get_holiday('us','2025','2')


# t1 = time.time()
# print(country_code_handler())
# t2 = time.time()
# print(t2-t1)
# info = req_countries.cache_info()
#0.002855062484741211 when retrieved from cache
#0.2691211700439453 when retrieved from api
# total= 0.0021638870239257812