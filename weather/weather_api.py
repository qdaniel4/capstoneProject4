import requests
import os
import collections

key = os.environ.get('TROPOSPHERE_KEY')



 

# # #     # call get like this
# def main():
#      coordinates = get_coordinates('munich', 'Germany')
# #     temp = get_climate(coordinates, '02')
#     print(temp)


#     temp = get_climate(lat,lon, '02')
#     print(temp)
   # returns something like {'rain': '4.61 inches per month', 'sunshine': '9.90 hours', 'temp': ' 56.63F to  41.42F'} 
      
  # from https://www.quickprogrammingtips.com/python/how-to-create-lru-cache-in-python.html
""" creates a cache when instantiated"""

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

cache = SimpleLRUCache(999)
lat_long_cache = SimpleLRUCache
  

def capitalize_city(city):
    """capitalizing first letter of each word put in to search for it"""
    if city:
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
    else:
        return None


def check_if_found(city):
    """ checks api json for all dictionaries with the city in the dictionary being the same as the one put in and returning dictionaries"""
    if city:
        searched_city = capitalize_city(city)
        url = f'https://api.troposphere.io/place/name/{searched_city}?token={key}'
        countries_list = []
        url_data = requests.get(url).json()
        if url_data['data'] == None:
            return None
        else:
            for x in url_data['data']:
                # if city put in is the same as city in list
                if searched_city == x['name']:
                    countries_list.append(x)
            #returns the data of all cities with same name
            return countries_list
    else:
        return None

#from https://towardsdatascience.com/how-to-speed-up-your-python-code-with-caching-c1ea979d0276

""" checks cache for the searched for city for a key """
def check_if_in_cache(searched_city):
    if searched_city:
        in_cache = cache.get(searched_city)
        if in_cache == -1:
            content = check_if_found(searched_city)
            cache.put(searched_city, content)
            return content
        # returns from cache
        return cache.get(searched_city)
    else:
        return None    

def pick_country(city, country):
    """checks list of dictionaies for the ones that have the same country as the one put in"""
    if city and country:
        countries_list = check_if_in_cache(city)
        cities_in_country = []
        #loops through list put in from check_if_found
        for correct_country in countries_list:
            # selects items with same country name as put in
            if country == correct_country['country']:
                cities_in_country.append(correct_country)
            if len(cities_in_country) == 0:
                return None
            else:
                # returns first item in list
                print(cities_in_country, 0)
                print(country)
                return cities_in_country[0], country
    else:
        return None    
        
        
    
    
def get_coordinates(city, country):
    """ gets coordinates from city and country put in"""
    if city and country:
        city = capitalize_city(city)
        country = capitalize_city(country)
        correct_city = pick_country(city, country)
        if correct_city == None:
            return None
        # gets latitude and longitude from pick_country
        lat = correct_city[0]['latitude']
        lon = correct_city[0]['longitude']
        return f'{lat},{lon}'
    else:
        return None

    

def get_month_number(month):
    """ turns month string put in to the correct number for searching a list"""
    if month:
    
        # changes month to correct format for search
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
        if month == '12':
            return_month = 11
        return return_month
    else:
        return None
    
    

def get_climate(coordinates, month):
    """ gets a list of climate data for the coordinates put in and searches list for data with the correct month"""
    if coordinates and month:
        month = get_month_number(month)
        # new api request
        url =  f'https://api.troposphere.io/climate/{coordinates}?token={key}'
        url_data = requests.get(url).json()
        # gets temp data from latitude and longitude of city originally searched for thr month put in
        temp_max = url_data['data']['monthly'][month]['temperatureMax']
        temp_min = url_data['data']['monthly'][month]['temperatureMin']
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
        rain_for_dict = f'{rain:.2f} inches'
        sunshine_for_dict = f'{sunshine_hours:.2f} hours'
        # all weather info
        temp_dict = {'rain': rain_for_dict, 'sunshine': sunshine_for_dict, 'high_temp': high_for_dict, 'low_temp': low_for_dict}
        
        return temp_dict
    else:
        return None
    

def check_if_in_lat_long_cache(cooridinates, month):
    """ checks if the data from api is in cache"""
    if cooridinates and month :
    
        in_cache = cache.get(cooridinates)
        if in_cache == -1:
            content = get_climate(cooridinates, month)
            cache.put(cooridinates, content)
            return content
        return cache.get(cooridinates)
    else:
        return None

# if __name__ == '__main__':
#      main()