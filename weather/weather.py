import requests
import os
import re
from pprint import pprint

key = os.environ.get('TROPOSPHERE_KEY')



    

# def city_name():
#     not_match = True
#     while not_match:
#         city = input('enter a city ')
#         if city == '':
#             print('you must enter a city')
#         else:
#         # from automate the boring stuff book
#         # and from # from https://www.guru99.com/python-regular-expressions-complete-tutorial.html
#             check = re.match(r'[\d\W]', city)
#             if not check:
#                 not_match = False
#                 return city

def capitolize_city(city):
    city = city.lower()
    to_return = ''
    list_words = []
    split = city.split(' ')
    for word in split:
        length = len(word)
        x = word[0].upper()
        list_words.append(x + word[1:length])
       
    if len(list_words)  > 1:
         # from https://www.geeksforgeeks.org/python-program-to-convert-a-list-to-string/
        to_return = ' '.join([elem for elem in list_words])
    else:
        to_return = list_words[0]
    return to_return

def check_if_found(searched_city):
    url = f'https://api.troposphere.io/place/name/{searched_city}?token={key}'
    countries_list = []
    url_data = requests.get(url).json()
    if len(url_data['data']) == 0:
       return None
    else:
        for x in url_data['data']:
            if searched_city == x['name']:
                countries_list.append(x)
        
        return countries_list  

def pick_correct(countries_list, country):
    cities_in_country = []
    for correct_country in countries_list:
        if country == correct_country['country']:
            cities_in_country.append(correct_country)
        if len(cities_in_country) == 0:
            return None
        else:
            print(cities_in_country[0])
            return cities_in_country[0]
       # if country == correct_country[]
    # not_match = True
    # x = 0
    # while not_match:
    #     x = 0
    #     for country_in_list in countries_list:
    #         print( str(x) + ' ' + country_in_list['name'] + ' in ' + country_in_list['admin1'] +', ' + country_in_list['country'])
    #         x += 1
    #     num = input('enter the number of correct city ')
    #     if  not num.isnumeric():
    #         print('you must enter a number')
    #     elif num == '':
    #         print('you must enter a number')
    #     else:
    #         num = int(num)
    #         if num > int(len(countries_list)) :
    #             print('you must enter a lower number')
    #         elif  num < 0:
    #             print('you must enter a higher number')
    #         else:
    #             correct_city = countries_list[num]
    #             not_match = False
    #             return correct_city
    
def get_coordinates(correct_city):
    latitude = correct_city['latitude']
    longitude = correct_city['longitude']
    return latitude, longitude
    
# def get_month_name():
#     not_match = True
#     while not_match:
#         month = input('enter a month name ')
#         if month == '':
#             print('you must enter a month name')
#         else:
#             check = re.match(r'[\d\W]', month)
#             if not check:
#                 month = month.lower()
#                 if month == 'january' or month == 'febuary' or month == 'march' or month == 'april' or month == 'may' or month == 'june' or month == 'july' or month == 'august' or month == 'september' or month == 'october' or month == 'november' or month == 'december':
#                     not_match = False
#                     return month

def get_month_number(month):
    number = 0
    if month == 1:
        number = 0
    elif month == 2:
        number = 1
    elif month == 3:
        number = 2
    elif month == 4:
        number = 3
    elif month == 5:
        number = 4
    elif month == 6:
        number = 5
    elif month == 7:
        number = 6
    elif month == 8:
        number = 7
    elif month == 9:
        number = 8
    elif month == 10:
        number = 9
    elif month == 11:
        number == 10
    else:
        number == 11
    return number

def get_climate(latitude, longitude, month):
    url =  f'https://api.troposphere.io/climate/{latitude},{longitude}?token={key}'
    url_data = requests.get(url).json()
    temp_max = url_data['data']['monthly'][month]['temperatureMax']
    temp_min = url_data['data']['monthly'][month]['temperatureMin']
    cloud_cover = url_data['data']['monthly'][month]['cloudCover']
    sunshine_hours = url_data['data']['monthly'][month]['sunshineHours']
    total_rain = url_data['data']['monthly'][month]['totalPrecipitation']
    high = (temp_max * 1.8) + 32
    low = (temp_min * 1.8) + 32
    rain = (total_rain * 2) / 25.4
    high_return =f' {high:.2f}F'
    low_return = f' {low:.2f}F'
    rain_return = f'{rain:.2f} inches per month'
    sunshine_return = f'{sunshine_hours:.2f}'
    temp_return = f'{high_return}F to {low_return}F'
    
    return rain_return, sunshine_return, temp_return






