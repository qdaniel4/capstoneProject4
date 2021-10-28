""" Depending on a given country-code , month, and year of travel,
the app will display holidays observed in that country during that month. """

import ui

def get_holiday_data(country,year,month):
    """ :params: the country_code(upperCase),year and month of travel.
    :returns holday name,description,date """
    holiday = get_holiday(country,year,month ) #str 
    if holiday is None:
        print ('There is no national holiday for this month')
    else:
        display_holiday(holiday)
             
def get_holiday(country,year,month):
    """ request holiday data from calendarificAPI.
    :params: country year and month are data the user provided.
    :returns: the national holidays   """
    return ui.get_holiday_data(country,year,month)
    
def display_holiday(holiday):
    """ display the holiday data. """
    ui.display_holiday(holiday)


# get_holiday_data('US','2039','2')