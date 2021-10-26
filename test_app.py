import unittest 
from unittest import TestCase



import app


class AppTest(TestCase):

    def test_get_month_and_year_from_date(self):
        date = '12/30/2022'

        expected_month = '12'
        expected_year = '2022'

        returned_month, returned_year = app.get_month_and_year_from_date(date)

        self.assertEqual(expected_month, returned_month)
        self.assertEqual(expected_year, returned_year)

    def test_get_month_and_year_from_date_tuple(self):
        date = '12/30/2022'

        expected_month_and_year = ('12', '2022')

        returned_month_and_year = app.get_month_and_year_from_date(date)

        self.assertEqual(expected_month_and_year, returned_month_and_year)

        
if __name__ == '__main__':
    unittest.main()