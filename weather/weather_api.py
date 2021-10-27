import requests
import os
import re
from pprint import pprint

key = os.environ.get('TROPOSPHERE_KEY')
cache ={}

def main():
    x = check_if_found('Munich')
    
    y = check_if_in_cache(x)
    print(y)
 ### I left in validation in case we need it   

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

def capitalize_city(city):
    # capitalizing first letter of each word put in to search for it
    city = city.lower()
    to_return = ''
    list_words = []
    # splitting by word
    split = city.split(' ')
    for word in split:
        length = len(word)
        # upper casing first letter
        x = word[0].upper()
        # putting capital letter and rest of word together in a list
        list_words.append(x + word[1:length])
       
    if len(list_words)  > 1:
        # if more than 1 word it makes a string out of all the words
         # from https://www.geeksforgeeks.org/python-program-to-convert-a-list-to-string/
        to_return = ' '.join([elem for elem in list_words])
    else:
        to_return = list_words[0]
    # for a return value of 1 word
    return to_return

def check_if_found(searched_city):
    url = f'https://api.troposphere.io/place/name/{searched_city}?token={key}'
    countries_list = []
    url_data = requests.get(url).json()
    if len(url_data['data']) == 0:
       return None
    else:
        for x in url_data['data']:
            # if city put in is the same as city in list
            if searched_city == x['name']:
                countries_list.append(x)
        #returns the data of all cities with same name
        
        return countries_list

# from https://towardsdatascience.com/how-to-speed-up-your-python-code-with-caching-c1ea979d0276
def check_if_in_cache(searched_city):
    
    for x in searched_city:
        
        if x['country'] not in cache:
            city = check_if_found(x['name'])
            print(city)
            cache[searched_city] = city
        return cache[searched_city]

    


def pick_correct(countries_list, country):
    cities_in_country = []
    #loops through list put in from check_if_found
    #for correct_country in countries_List:
        # selects items with same country name as put in
    for k, v in countries_list.items():
       # if country == correct_country['country']:
        
        for x in v['data']:
            if x['country'] == country:
                cities_in_country.append(x)
          #  cities_in_country.append(correct_country)
        if len(cities_in_country) == 0:
            return None
        else:
            # returns first item in list 
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
    # gets latitude and longitude from pick_country
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
    # changes month to correct format for search
    return_month = 0
    if month == '01':
        return_month = 0
    if month == '02':
        return_month = 1
    if month == '03':
        return_month = 2
    if month == '04':
        return_month = 3
    if month == '05':
        return_month = 4
    if month == '06':
        return_month = 5
    if month == '07':
        return_month = 6
    if month == '08':
        return_month = 7
    if month == '09':
        return_month = 8
    if month == '10':
        return_month = 9
    if month == '11':
        return_month = 10
    else:
        return_month = 11
    return return_month
    

def get_climate(latitude, longitude, month):
    # new api request
    url =  f'https://api.troposphere.io/climate/{latitude},{longitude}?token={key}'
    url_data = requests.get(url).json()
    # gets temp data from latitude and longitude of city originally searched for thr month put in
    temp_max = url_data['data']['monthly'][month]['temperatureMax']
    temp_min = url_data['data']['monthly'][month]['temperatureMin']
    cloud_cover = url_data['data']['monthly'][month]['cloudCover']
    sunshine_hours = url_data['data']['monthly'][month]['sunshineHours']
    total_rain = url_data['data']['monthly'][month]['totalPrecipitation']
    # changing celsius to farenhight
    high = (temp_max * 1.8) + 32
    low = (temp_min * 1.8) + 32
    # changing metric to imperial
    rain = (total_rain * 2) / 25.4
    # puts results in a string to display
    high_for_dict =f' {high:.2f}F'
    low_for_dict = f' {low:.2f}F'
    rain_for_dict = f'{rain:.2f} inches per month'
    sunshine_for_dict = f'{sunshine_hours:.2f}'
    # a string of high and low
    temp_for_dict = f'{high_for_dict}F to {low_for_dict}F'
    # all weather info
    temp_dict = {'rain': rain_for_dict, 'sunshine': sunshine_for_dict, 'temp': temp_for_dict}
    return temp_dict

cache = {}



if __name__ == '__main__':
    main()