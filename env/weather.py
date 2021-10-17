import requests
import os
import re
from pprint import pprint

# location
# https://api.troposphere.io/place/name/[Search-String]?token=[API-KEY]

# weather 
# https://api.troposphere.io/forecast/[Latitude],[Longitude]?token=[API-KEY]

# climate
# https://api.troposphere.io/climate/[Latitude],[Longitude]?token=[API-KEY]
# https://api.troposphere.io/climate/48.5,11.123?token=[API-KEY]

key = os.environ.get('TROPOSPHERE_KEY')


def main():
    city_input = city_name()
    capitolized = capitolize_city(city_input)
    list_of_countries = check_if_found(capitolized)
    correct_city = pick_correct(list_of_countries)
    get_coordinates(correct_city)
    #month = get_month_name()
    #get_month_number(month)

    

def city_name():
    not_match = True
    while not_match:
        city = input('enter a city ')
        if city == '':
            print('you must enter a city')
        else:
        # from automate the boring stuff book
        # and from # from https://www.guru99.com/python-regular-expressions-complete-tutorial.html
            check = re.match(r'[\d\W]', city)
            if not check:
                not_match = False
                return city

def capitolize_city(city):
    city = city.lower()
    listWords = []
    split = city.split(' ')
    for word in split:
        length = len(word)
        x = word[0].upper()
        listWords.append(x + word[1:length])
    searched_city = "".join(listWords)
    return searched_city

def check_if_found(searched_city):
    url = f'https://api.troposphere.io/place/name/{searched_city}?token={key}'
    countries_list = []
    url_data = requests.get(url).json()
    for x in url_data['data']:
        if searched_city == x['name']:
            countries_list.append(x)
        if not countries_list:
            check_if_found(capitolize_city(city_name()))
    return countries_list



    






def pick_correct(countries_list):
    not_match = True
    x = 0
    while not_match:
        x = 0
        for country_in_list in countries_list:
            print( str(x) + ' ' + country_in_list['name'] + ' in ' + country_in_list['admin1'] +', ' + country_in_list['country'])
            x += 1
        num = input('enter the number of correct city ')
        if  not num.isnumeric():
            print('you must enter a number')

       
        elif num == '':
            print('you must enter a number')
        else:
            num = int(num)
            
            if num > int(len(countries_list)) :
                print('you must enter a lower number')
            elif  num < 0:
                print('you must enter a higher number')
            else:
                correct_city = countries_list[num]
                not_match = False
                return correct_city
    

        
        
            
def get_coordinates(correct_city):
    latitude = correct_city['latitude']
    longitude = correct_city['longitude']
    print(latitude)
    print(longitude)
    
     
             


    
        
        
    
        #print(url_data["data"][x]['name'])
    #latitude = url_data["data"][0]["latitude"]
    #longitude = url_data["data"][0]["longitude"]
    
    #return latitude, longitude 

def get_month_name():
    not_match = True
    while not_match:
        month = input('enter a month name ')
        if month == '':
            print('you must enter a month name')
        else:
            check = re.match(r'[\d\W]', month)
            if not check:
                month = month.lower()
                if month == 'january' or month == 'febuary' or month == 'march' or month == 'april' or month == 'may' or month == 'june' or month == 'july' or month == 'august' or month == 'september' or month == 'october' or month == 'november' or month == 'december':
                    not_match = False
                    return month

def get_month_number(month):
    number = 0
    if month == 'january':
        number = 0
    elif month == 'febuary':
        number = 1
    elif month == 'march':
        number = 2
    elif month == 'april':
        number = 3
    elif month == 'may':
        number = 4
    elif month == 'june':
        number = 5
    elif month == 'july':
        number = 6
    elif month == 'august':
        number = 7
    elif month == 'september':
        number = 8
    elif month == 'october':
        number = 9
    elif month == 'november':
        number == 10
    else:
        number == 11
    print(number)
    


                









if __name__ == '__main__':
    main()
