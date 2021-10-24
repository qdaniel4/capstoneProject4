""" Depending on a given country-code , month, and year of travel,
the app will display holidays observed in that country during that month. """

import time
import ui
import valid

#TODO fix validation/exception issue
#TODO testing cont.. fix reqhttp res


def main():
    country_location = get_country()
    travel_year,travel_month = get_travel_date()
        
    t1 = time.perf_counter()
    holiday = get_holiday(country_location,travel_year,travel_month )
    

    if holiday is None:
        print ('There is no national holiday for this month')
    else:
        display_holiday(holiday)
        t2 = time.perf_counter()
        print(f'Finished in {t2-t1} seconds')


def get_country():
    """ ask user the country's country_code,validate the input and pass it to api req country_code handler
    :returns: the country_code (ISO format)"""
    while True:
        country = valid.valid_country_code_input()
        country_code = ui.country_code_handler(country.upper())
        if country_code == None:
            continue
        else:
            break
    return country_code

      
def get_travel_date():
    """ :return the year and month of travel. """
    year = valid.valid_year()
    month = valid.valid_month()
    return year, month
            
     
def get_holiday(country,year,month):
    """ request holiday data from calendarificAPI.
    :params: country year and month are data the user provided.
    :returns: the national holidays   """
    return ui.get_holiday_data(country,year,month)

    
def display_holiday(holiday):
    """ display the holiday data. """
    ui.display_holiday(holiday)
      

if __name__ == '__main__':
    main()