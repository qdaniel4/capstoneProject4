import requests
import os
import re
from pprint import pprint
import collections

key = '9048347e96d25c489043de49f6b92476b2184a595c86683051'  #'https://github.com/qdaniel4/capstoneProject4/tree/weather/weather' os.environ.get('TROPOSPHERE_KEY')


def main():
      #x = check_if_found('Munich')
#     print(x)
      y = check_if_in_cache('London')
     # x = pick_correct(y, 'Germany')
      

 # from https://www.quickprogrammingtips.com/python/how-to-create-lru-cache-in-python.html
class SimpleLRUCache:
  def __init__(self, size):
    self.size = size
    self.lru_cache = collections.OrderedDict()
 
  def get(self, key):
    try:
      value = self.lru_cache.pop(key)
      self.lru_cache[key] = value
      return value
    except KeyError:
      return -1
 
  def put(self, key, value):
    try:
      self.lru_cache.pop(key)
    except KeyError:
      if len(self.lru_cache) >= self.size:
        self.lru_cache.popitem(last=False)
    self.lru_cache[key] = value
 
  def show_entries(self):
    print(self.lru_cache)

cache_city_to_lat_long = SimpleLRUCache(999)
climate_for_month_cache = SimpleLRUCache(999)

 ## I left in validation in case we need it   

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
    return city.title()

    
def check_if_found(searched_city):
    url = f'https://api.troposphere.io/place/name/{searched_city}?token={key}'
    countries_list = []
    url_data = requests.get(url).json()
    pprint( url_data)
    if url_data['data'] == None:
        print('There were no results')
        return None
    else:
        for x in url_data['data']:
            # if city put in is the same as city in list
            if searched_city == x['name']:
                countries_list.append(x)
        #returns the data of all cities with same name
        print(countries_list)
        return countries_list


# @lru_cache(maxsize=999)
#from https://towardsdatascience.com/how-to-speed-up-your-python-code-with-caching-c1ea979d0276

# one function for flask to call 
def get_climate_data_for_city(city, country, month):


    # convert city and county into lat-long
    # check if the lat-long for city  in the cache 1 ?
    # if it is, use that
    # if not, make API request to get lat-long, store in cache for next time 


    # now we have the lat-long

    # is climate for city for month in cache 2? 
    # if it is, return data from cache 
    # if it not 
        # make the request for climate for lat long (for month)?

    
    # return climate 





def pick_correct(countries_list, country):
    cities_in_country = []
    #loops through list put in from check_if_found
    for correct_country in countries_list:
        # selects items with same country name as put in
    #for k, v in countries_list.items():
        if country == correct_country['country']:
        
        #for x in v['data']:
            #if x['country'] == country:
            #cities_in_country.append(x)
            cities_in_country.append(correct_country)
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


def convert_month_string_to_month_number(month):
    """ convert a month such as "06" for June to 5 (0-based months for API) """
    # EXCELLENT candidate for a test 
    if month.starts_with('0'):
        month = month[1:]   # remove leading 0
    return int(month) - 1

    

def get_climate(coordinates, month):
    # new api request
    url =  f'https://api.troposphere.io/climate/{coordinates}?token={key}'
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
    high_for_dict =f'{high:.2f}F'
    low_for_dict = f'{low:.2f}F'
    rain_for_dict = f'{rain:.2f} inches per month'
    sunshine_for_dict = f'{sunshine_hours:.2f}'
    # a string of high and low
    temp_for_dict = f'{high_for_dict}F to {low_for_dict}F'
    # all weather info
    temp_dict = {'rain': rain_for_dict, 'sunshine': sunshine_for_dict, 'temp': temp_for_dict}
    return temp_dict

if __name__ == "__main__":
     main()



