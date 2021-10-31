import unittest 
from unittest import TestCase

import ui_support
import json

class TestUI(TestCase):


    def test_get_list_of_countries_valid(self):
        with open('all_countries_from_holiday_api.json') as countries_file:
            countries_from_API = json.load(countries_file)
        returned_countries_list, err = ui_support.get_list_of_countries(countries_from_API)

        self.assertIsNotNone(returned_countries_list)

        self.assertIn('Algeria', returned_countries_list)
        self.assertIn('Mauritania', returned_countries_list)
        self.assertIn('Saudi Arabia', returned_countries_list)
        self.assertIn('United Kingdom', returned_countries_list)

        self.assertNotIn('DZ', returned_countries_list)
        self.assertNotIn('MR', returned_countries_list)
        self.assertNotIn('SA', returned_countries_list)
        self.assertNotIn('GB', returned_countries_list)


    def test_get_list_of_countries_no_response_from_API_returns_None(self):
        countries_from_API = None
        returned_countries_list, err = ui_support.get_list_of_countries(countries_from_API)

        self.assertIsNone(returned_countries_list)


    def test_get_month_and_year_from_date(self):
        date = '12/30/2022'

        expected_month_and_year = ('12', '2022')
        expected_month = '12'
        expected_year = '2022'

        returned_month_and_year = ui_support.get_month_and_year_from_date(date)
        returned_month, returned_year = returned_month_and_year

        self.assertEqual(expected_month_and_year, returned_month_and_year)
        self.assertEqual(expected_month, returned_month)
        self.assertEqual(expected_year, returned_year)


    def test_get_name_of_month_from_number_valid_month_number(self):
        month_number = '05'
        expected_month_name = 'May'
        returned_month_name, err = ui_support.get_name_of_month_from_number(month_number)

        self.assertEqual(returned_month_name, expected_month_name)


    def test_get_name_of_month_from_number_invalid_month_number(self):
        month_number = '24'
        returned_month_name, err = ui_support.get_name_of_month_from_number(month_number) 

        self.assertIsNone(returned_month_name)

        
    def test_get_name_of_month_from_number_month_is_not_a_valid_number(self):
        month_number = 'this is not a valid month number'
        returned_month_name, err = ui_support.get_name_of_month_from_number(month_number) 

        self.assertIsNone(returned_month_name)


if __name__ == '__main__':
    unittest.main()