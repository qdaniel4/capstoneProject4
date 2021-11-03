from unittest import TestCase
from unittest.mock import patch, Mock
from requests import Response

import redislite
from redislite import Redis # self-contained, run separately
import redislite.patch
import redis
import extract_holiday
from extract_holiday import redi


class TestUI(TestCase):
    
    def setUp(self):
        #create fakeredis here
        redislite.patch.patch_redis()
        self.fake_redis = redislite.StrictRedis(host="localhost", port=6379,db=0)#will get a reference to the existing running redis instance so both instances share the same redis-server process 
    
    def test_country_code_is_supported(self):
        with patch('requests.Response.json') as mock_res:
            mock_code ='AF'
            mock_res.return_value = mock_code
            td = extract_holiday.is_country_supported('Afghanistan')
        self.assertIn(mock_code,td)
            
        
    
    def test_country_code_is_not_supported(self):
        """ testing expected dict is returned. """
        with patch('requests.Response.json') as mock_res:
            sample_response = 'MK'
            mock_res.return_value = sample_response
            actual = extract_holiday.is_country_supported('Afghanistan')
        self.assertIsNot(actual,sample_response)
        self.assertNotEqual(actual,sample_response)
        
        
    def test_country_returns_not_none_if_it_is_suported(self):
        with patch('requests.Response.json') as mock_get:
            expected = 'US'
            mock_get.return_value = expected
            actual = extract_holiday.is_country_supported('united states')
        self.assertEqual(actual,expected)
        self.assertIsNotNone(actual,expected)
        
        
        
    def test_country_returns_none_if_no_countries_returned(self):
        with patch('requests.Response.json') as mock_get:
            expected = []
            mock_get.side_effect = None
            actual = extract_holiday.req_countries()
        self.assertIsNone(actual,expected)
        self.assertFalse(actual,expected)
     
                      
# #    holiday endpoint
    def test_holiday_returns_correct_dictionary(self):
        with patch('requests.Response.json') as mock_get:
            expected_response = {'holiday_name': 'Independence Day', 'description': 'On Independence Day, Americans celebrate the anniversary of publication of the Declaration of Independence from Great Britain in 1776.', 'date': '2022-07-04'}
            hol_sample = [{'name': 'Independence Day', 'description': 'On Independence Day, Americans celebrate the anniversary of publication of the Declaration of Independence from Great Britain in 1776.', 'country': {'id': 'us', 'name': 'United States'}, 'date': {'iso': '2022-07-04', 'datetime': {'year': 2022, 'month': 7, 'day': 4}}, 'type': ['National holiday'], 'locations': 'All', 'states': 'All'}]
            mock_get.return_value = expected_response
            actual = extract_holiday.extract_country_holiday(hol_sample)
        self.assertEqual(expected_response,actual)


        
      