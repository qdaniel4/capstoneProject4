""" Depending on a given country-code , month, and year of travel,
the app will display holidays observed in that country during that month. """

import time
import pyinputplus as pyip
from datetime import datetime
from exceptions import ValueTooLarge,NoStateRegion
import ui


#TODO work on rendering the ISO supported state/region.return value too long
#TODO return location 'ALL' if no state/region is supported
#TODO fix validation/exception issue
#TODO REFACTOR CODE!! separate query from modifier
#TODO testing
#TODO update Slack


def main():
    country_location = get_country()
    travel_year,travel_month = get_travel_date()
  
        
    t1 = time.perf_counter()
    holiday = get_holiday(country_location,travel_year,travel_month )

    if holiday is None:
        print ('There is no national holiday for this month')
        t2 = time.perf_counter()#temp
    else:
        
        display_holiday(holiday)
        t2 = time.perf_counter()#temp, simply checking response time
        print(f'Finished in {t2-t1} seconds')


def get_country():
    #TODO include state/counties if available
    """ :return the country of travel in ISO format"""
    while True:
        try:
            country = input('Enter the 2-letter country code: ').strip()
            # region_state = input('Enter the 2-letter region code: ').strip()
            if len(country) != 2 or not country.isalpha():
                raise ValueTooLarge
            else:
                ui.valid_country_code(country.upper())
            break
        except ValueTooLarge:
            print("Country code must be in 2-letter format, try agin!\n")
        except NoStateRegion:
            print('error, No country with that country code,try agin!\n')
    return country
            
  
   

def get_travel_date():
    """ :return the year and month of travel """
    while True:
        today = str(datetime.today())
        curr_year = int(today[:4])

        year = pyip.inputNum('Enter the year you wish to travel eg,2021: ')
        if year < curr_year or year > 2049: #2049 is the maximum year API supports
            print('Not Valid: year of travel must be between CURRENT year(2021) to 2049')
            continue
        else:
            month = pyip.inputNum('Enter the month you wish to travel eg,1-12: ', min=1, max=12)
        return year, month
  
       
            
     
def get_holiday(country,year,month):
    """ request holiday data from calendarificAPI
    :param country year and month are the user input return
    :return the holiday data with the given country,year and month """
    
    try:
        query = {'country': country, 'year': year, 'month': month}
        response = ui.req_holiday(query)
        
        return response
    except Exception as err:
        print(err)
    
    
    

def display_holiday(holiday):
    """ display the holiday data"""
    try:
        ui.get_holiday_data(holiday)
        
    except Exception:
        print('This data is not in the format expected')
        return 'Unknown'
    

    
    

if __name__ == '__main__':
    main()

