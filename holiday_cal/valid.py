import exceptions
from exceptions import NoStateRegion,ValueTooLarge
from datetime import datetime
import pyinputplus as pyip

""" All user inputs are queried and validated before passed to request parameters. """

def valid_country_code_input():
    """ Ask for country_code, validate to ensure user entered in the correct format.
    :returns: The country code. """
    while True:
        try:
            country_code = input('Enter the 2-letter country code: ').strip()
            if len(country_code) != 2 or not country_code.isalpha():
                raise ValueTooLarge
            break
        except ValueTooLarge:
            print("Err, Country code must be 2 letters, in (ISO-3166) format.eg US, try again!\n")
            continue
    return country_code


def valid_year():
    """ ask for the year user is planning to travel to the provided country, 
    validate to ensure user entered the righ data type(int) and in the correct format.
    :returns: the year in 4 digit format.eg,2021 """
    while True:
        today = str(datetime.today())
        curr_year = int(today[:4])
        year = pyip.inputNum('Enter the year you wish to travel eg,2021: ')
        if year < curr_year or year > 2049: #2049 is the maximum year API supports
            print('Not Valid: year of travel must be between CURRENT year(2021) to 2049')
            continue
        break
    return year
    

def valid_month():
    """ ask for the month planned to travel, 
    validate to ensure user entered the righ data type(int).
    :returns: the numeric value of the month. eg,[1-12]. """
    month = pyip.inputNum('Enter the month you wish to travel eg,1-12: ',min=1, max=12)
    return month