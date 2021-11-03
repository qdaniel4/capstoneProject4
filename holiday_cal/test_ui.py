# from unittest import TestCase
# from unittest.mock import patch, Mock
# from requests import Response

# import redislite
# from redislite import Redis # self-contained, run separately
# import redislite.patch
# import redis
# import json
# import extract_holiday
# from datetime import timedelta

# redi = redis.Redis(host='localhost', port=6379, db=0)
# # country_res = redi.get('countries')
# # redi.set('countries',json.dumps(country_res), timedelta(seconds=360)) #prevents cache staleness

# class TestUI(TestCase):
    
#     def setUp(self):
#         #create fakeredis here
#         # redi.set('countries',json.dumps(country_res), timedelta(seconds=360)) #prevents cache staleness
#         redi = redis.Redis(host='localhost', port=6379, db=0)
#         self.td = extract_holiday.req_res_country()
#         self.test_list = []
#         for i in self.td:
#             self.test_list.append(i)
#         redi.set('countries',json.dumps(self.td), timedelta(seconds=360)) #prevents cache staleness
#         country_res = redi.get('countries')
            
            
#     @patch('requests.Response.json')
#     def test_redis(self,get_mock):
#         self.maxDiff = None
    
#         response = extract_holiday.req_res_country()
#         mock_res = self.test_list
#         mock_redis.return_value = mock_res
#         self.assertEqual(response,mock_res)
        
        
    
#     def test_country_code_returns_country_list(self):
#         """ testing expected dict is returned. """
#         with patch('requests.Response.json') as mock_res:
#             sample_response = self.test_list
#             mock_res.side_effect = sample_response
#             actual = extract_holiday.req_res_country()
#         self.assertListEqual(actual,sample_response)
        
#     #  Test countries endpoint
#     def test_country_code_returned(self):
#         pass

             


                
                
from unittest import TestCase
from unittest.mock import patch, Mock
from requests import Response

import redislite
from redislite import Redis # self-contained, run separately
import redislite.patch
import redis
import extract_holiday

class TestUI(TestCase):
    
    def setUp(self):
        #create fakeredis here
        redislite.patch.patch_redis()
        self.td = extract_holiday.req_res_country()
        self.test_list = []
        for i in self.td:
            self.test_list.append(i)
            
    @patch('requests.Response.json')
    def test_redis(self,get_mock):
        self.maxDiff = None
        redislite.patch.patch_redis()
        mock_redis = get_mock.StrictRedis.return_value
        response = extract_holiday.req_res_country()
        mock_res = self.test_list
        mock_redis.return_value = mock_res
        self.assertEqual(response,mock_res)
        
        
    
    def test_country_code_returns_country_list(self):
        """ testing expected dict is returned. """
        with patch('requests.Response.json') as mock_res:
            sample_response = self.test_list
            mock_res.side_effect = sample_response
            actual = extract_holiday.req_res_country()
        self.assertListEqual(actual,sample_response)
                    
#    holiday endpoint
    def test_holiday_returns_correct_value(self):
        with patch('requests.Response.json') as mock_req_json:
            expected_response = {'holiday_name': 'Independence Day', 'description': 'On Independence Day, Americans celebrate the anniversary of publication of the Declaration of Independence from Great Britain in 1776.', 'date': '2022-07-04'}
            mock_req_json.side_effect = expected_response
            for i in expected_response:
                actual = extract_holiday.display_holiday(i)
        self.assertDictEqual(actual,expected_response)