import unittest
from unittest import TestCase
from unittest import mock
from unittest.mock import patch, call

import weather
from weather import capitolize_city

class TestWeather(TestCase):

    def test_capitolized_city_capitolizes_first_letter(self):
        self.assertEqual('Miami', capitolize_city('miami'))

    def test_capitolized_city_capitolizes_lower_cases_all_but_last_letter(self):
        self.assertEqual('Miami', capitolize_city('MIAMI'))

    def test_capitolized_city_with_2_words(self):
        self.assertEqual('New York', capitolize_city('new york'))


    @patch('weather.check_if_found')
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
        found_city = weather.check_if_found(city)
        the_city = found_city['data'][0]['name']
        expected = 'Munich'
        self.assertEqual(expected, the_city)

    @patch('weather.check_if_found')
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

        return_respponse= {
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
        found_city = weather.check_if_found(city)
        self.assertEqual(found_city, return_respponse)



    #@patch('weather.get_coordinates')
    def test_get_coordinates_works(self):
        lat = 48.13743
        lon = 11.57549
        mock_response = {
"id": 2867714,
"name": "Munich",
"latitude": lat,
"longitude": lon,
"continent": "EU",
"country": "Germany",
"countryEmoji": "🇩🇪",
"admin1": "Bavaria",
"admin2": "Upper Bavaria",
"admin3": "Munich, Urban District",
"admin4": "Munich",
"type": "place"
}
    
        returned_latitude, returned_longitude = weather.get_coordinates(mock_response)
        self.assertEqual(returned_latitude, lat)
        self.assertEqual(returned_longitude, lon)