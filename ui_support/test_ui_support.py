import unittest 
from unittest import TestCase

import ui_support
import json

class TestUI(TestCase):


    def test_add_error_to_error_list_valid_error(self):
        error = 'This is an error.'
        error_list = []

        ui_support.add_error_to_error_list(error, error_list)

        self.assertIn(error, error_list)


    def test_add_error_to_error_list_multiple_valid_errors(self):
        error_one = 'This is an error.'
        error_two = 'This is another error'
        error_list = []

        ui_support.add_error_to_error_list(error_one, error_list)
        ui_support.add_error_to_error_list(error_two, error_list)

        self.assertIn(error_one, error_list)
        self.assertIn(error_two, error_list)


    def test_add_error_to_error_list_does_not_add_None(self):
        error = None
        error_list = []
        error_list_expected_length = 0

        ui_support.add_error_to_error_list(error, error_list)

        self.assertNotIn(error, error_list)
        self.assertEqual(error_list_expected_length, len(error_list))


    def test_add_some_errors_to_error_list_and_does_not_add_None(self):
        error_one = 'This is an error.'
        error_two = 'This is another error'
        error_three = None
        error_four = 'Another error'
        error_five = None
        error_list = []

        error_list_expected_length = 3

        ui_support.add_error_to_error_list(error_one, error_list)
        ui_support.add_error_to_error_list(error_two, error_list)
        ui_support.add_error_to_error_list(error_three, error_list)
        ui_support.add_error_to_error_list(error_four, error_list)
        ui_support.add_error_to_error_list(error_five, error_list)

        self.assertIn(error_one, error_list)
        self.assertIn(error_two, error_list)
        self.assertNotIn(error_three, error_list)
        self.assertIn(error_four, error_list)
        self.assertNotIn(error_five, error_list)

        self.assertEqual(error_list_expected_length, len(error_list))



    def test_get_list_of_countries_valid(self):
        with open('all_countries_from_holiday_api.json') as countries_file:
            countries_from_API = json.load(countries_file)
        returned_countries_list, returned_error_message = ui_support.get_list_of_countries(countries_from_API)

        self.assertIsNotNone(returned_countries_list)
        self.assertIsNone(returned_error_message)

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
        expected_error_message = 'No response from Calendarific API for country names.'
        returned_countries_list, returned_error_message = ui_support.get_list_of_countries(countries_from_API)

        self.assertIsNone(returned_countries_list) 
        self.assertEqual(expected_error_message, returned_error_message)


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
        returned_month_name, returned_error = ui_support.get_name_of_month_from_number(month_number)

        self.assertEqual(expected_month_name, returned_month_name)
        self.assertIsNone(returned_error)


    def test_get_name_of_month_from_number_invalid_month_number(self):
        month_number = '24'
        expected_error_message = 'Error: Month needs to be a whole number 1-12.'
        returned_month_name, returned_error_message = ui_support.get_name_of_month_from_number(month_number) 

        self.assertIsNone(returned_month_name)
        self.assertEqual(expected_error_message, returned_error_message)


    def test_get_name_of_month_from_number_invalid_month_number_negative(self):
        month_number = '-24' 
        expected_error_message = 'Error: Month needs to be a whole number 1-12.'
        returned_month_name, returned_error_message = ui_support.get_name_of_month_from_number(month_number) 

        self.assertIsNone(returned_month_name)
        self.assertEqual(expected_error_message, returned_error_message) 


    def test_get_name_of_month_from_number_invalid_month_number_decimal(self):
        month_number = '01.23423'
        expected_error_message = 'Error: Month needs to be a whole number 1-12.'
        returned_month_name, returned_error_message = ui_support.get_name_of_month_from_number(month_number) 

        self.assertIsNone(returned_month_name)
        self.assertEqual(expected_error_message, returned_error_message)

        
    def test_get_name_of_month_from_number_month_is_not_a_valid_number(self):
        month_number = 'this is not a valid month number'
        expected_error_message = 'Error: Month needs to be a whole number 1-12.'
        returned_month_name, returned_error_message = ui_support.get_name_of_month_from_number(month_number) 

        self.assertIsNone(returned_month_name)
        self.assertEqual(expected_error_message, returned_error_message)


if __name__ == '__main__':
    unittest.main()