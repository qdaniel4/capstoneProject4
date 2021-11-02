import unittest
from unittest import TestCase
from unittest.case import expectedFailure
from unittest.mock import patch

import os

import holiday_api

api_key = os.environ.get('CALENDAR_KEY')

class TestHolidayAPI(TestCase):

    def test_is_country_supported(self):
        country_name = 'Afghanistan'
        returned_country_code = holiday_api.is_country_supported(country_name)
        expected_country_code = 'AF'

        self.assertEqual(expected_country_code, returned_country_code)


    def test_get_holiday_data(self):
        expected_holiday_data_response = [{'name': 'Christmas Day', 'description': 'Christmas Day is one of the biggest Christian celebrations and falls on December 25 in the Gregorian calendar.', 'country': {'id': 'se', 'name': 'Sweden'}, 'date': {'iso': '2022-12-25', 'datetime': {'year': 2022, 'month': 12, 'day': 25}}, 'type': ['National holiday'], 'locations': 'All', 'states': 'All'},
        {'name': 'Boxing Day', 'description': 'Boxing Day is a public holiday in Sweden', 'country': {'id': 'se', 'name': 'Sweden'}, 'date': {'iso': '2022-12-26', 'datetime': {'year': 2022, 'month': 12, 'day': 26}}, 'type': ['National holiday'], 'locations': 'All', 'states': 'All'}]
        returned_holiday_data_response = holiday_api.get_holiday_data('SE','2022','12')
        
        self.assertEqual(expected_holiday_data_response, returned_holiday_data_response)

    
    def test_req_holiday(self):
        expected_holidays_response = [{'name': 'Christmas Day', 'description': 'Christmas Day is one of the biggest Christian celebrations and falls on December 25 in the Gregorian calendar.', 'country': {'id': 'se', 'name': 'Sweden'}, 'date': {'iso': '2022-12-25', 'datetime': {'year': 2022, 'month': 12, 'day': 25}}, 'type': ['National holiday'], 'locations': 'All', 'states': 'All'},
        {'name': 'Boxing Day', 'description': 'Boxing Day is a public holiday in Sweden', 'country': {'id': 'se', 'name': 'Sweden'}, 'date': {'iso': '2022-12-26', 'datetime': {'year': 2022, 'month': 12, 'day': 26}}, 'type': ['National holiday'], 'locations': 'All', 'states': 'All'}]
        sample_query = {'country': 'SE', 'year': '2022', 'month': '12', 'type':'national','api_key':api_key}
        returned_holidays_response = holiday_api.req_holiday(sample_query)
        
        self.assertEqual(expected_holidays_response, returned_holidays_response)
    

    def test_get_holiday(self):
        expected_holiday_list = [{'holiday_name': 'Christmas Day', 'description': 'Christmas Day is one of the biggest Christian celebrations and falls on December 25 in the Gregorian calendar.', 'date': '2022-12-25'},
        {'holiday_name': 'Boxing Day', 'description': 'Boxing Day is a public holiday in Sweden', 'date': '2022-12-26'}]
        returned_holiday_list = holiday_api.get_holiday('Sweden','2022','12')

        self.assertEqual(expected_holiday_list, returned_holiday_list)

if __name__ == '__main__':
    unittest.main()

