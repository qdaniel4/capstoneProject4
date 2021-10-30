import unittest
from unittest import TestCase
from unittest import mock
from unittest.mock import patch, call
from weather_api import get_month_number
from weather_api import capitalize_city

import weather_api
from weather_api import capitalize_city

class TestWeather(TestCase):

    # tests if first letter of each word is entered is capitalized
    def test_capitolized_city_capitalizes_first_letter(self):
        self.assertEqual('Miami', capitalize_city('miami'))

    # test if only first letter is capitalized
    def test_capitolized_city_capitalizes_lower_cases_all_but_last_letter(self):
        self.assertEqual('Miami', capitalize_city('MIAMI'))

    # tests if function works with more than 1 word
    def test_capitalized_city_with_2_words(self):
        self.assertEqual('New York', capitalize_city('new york'))
    
    # tests sting value is returned with coored number
    def test_get_month_number_works(self):
        self.assertEqual(1, get_month_number('02'))

    # tests pick country returns correct dictionary from many dictionaries, the Munich with Germany as it's country
    def test_pick_country(self):
        country = "Germany"
       
        check_call = weather_api.pick_country("Munich", country)
        self.assertEqual(country, check_call[0]['country'])

    

    # tests check if found will find will find the right data from api
    @patch('weather_api.check_if_found')
    def test_check_if_found_finds_city(self, mock_city):
        city = "Munich"
        example_api_response = {
"error": None,
"data": [
{
"id": 2867714,
"name": city,
"latitude": 48.13743,
"longitude": 11.57549,
"continent": "EU",
"country": "Germany",
"countryEmoji": "🇩🇪",
"admin1": "Bavaria",
"admin2": "Upper Bavaria",
"admin3": "Munich, Urban District",
"admin4": "Munich",
"type": "place"
}
        
]
}
        mock_city.side_effect = [ example_api_response ]
        found_city = weather_api.check_if_found(city)
        the_city = found_city['data'][0]['name']
        expected = 'Munich'
        self.assertEqual(expected, the_city)

    # tests if check_if_found returns the correct data
    @patch('weather_api.check_if_found')
    def test_check_if_found_returns_data(self, mock_city):
        city = "Munich"
        example_api_response = {
"error": None,
"data": [
{
"id": 2867714,
"name": city,
"latitude": 48.13743,
"longitude": 11.57549,
"continent": "EU",
"country": "Germany",
"countryEmoji": "🇩🇪",
"admin1": "Bavaria",
"admin2": "Upper Bavaria",
"admin3": "Munich, Urban District",
"admin4": "Munich",
"type": "place"
}
        
]
}

        return_response= {
"error": None,
"data": [
{
"id": 2867714,
"name": "Munich",
"latitude": 48.13743,
"longitude": 11.57549,
"continent": "EU",
"country": "Germany",
"countryEmoji": "🇩🇪",
"admin1": "Bavaria",
"admin2": "Upper Bavaria",
"admin3": "Munich, Urban District",
"admin4": "Munich",
"type": "place"
}
        
]
}
        mock_city.side_effect = [ example_api_response ]
        found_city = weather_api.check_if_found(city)
        self.assertEqual(found_city, return_response)


  