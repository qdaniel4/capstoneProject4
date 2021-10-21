import unittest
from unittest import TestCase
from unittest import mock
from unittest.mock import patch, call

import weather
from weather import capitolize_city

class TestWeather(TestCase):

    def test_capitolized_city_capitolizes_first_letter(self):
        self.assertEqual('New York', capitolize_city('new york'))

    def test_capitolized_city_capitolizes_lower_cases_all_but_last_letter(self):
        self.assertEqual('New York', capitolize_city('NEW YORK'))

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
        mock_city.side_effect = [ example_api_response]
        found_city = weather.check_if_found('Munich')
        expected = 'Munich'
        self.assertEqual(expected, found_city)