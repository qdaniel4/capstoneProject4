from unittest import TestCase
from unittest.mock import patch, Mock
from requests import Response

import redislite
from redislite import Redis # self-contained, run separately
import redislite.patch

import extract_holiday

class TestUI(TestCase):
    
    def setUp(self):
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
        
    #  Test countries endpoint
    def test_country_code_returned(self):
        pass

             

#    holiday endpoint
    def test_holiday_returns_correct_value(self):
        with patch('requests.Response.json') as mock_req_json:
                mock_country = 'us'
                mock_year = '2021'
                mock_month = '1'
                mock_api_response = {
                        'country': mock_country,
                        'year': mock_year, 
                        'month': mock_month, 
                        'type':'national',
                        'api_key':'api_key'
                        }
                mock_req_json.json.return_value.return_value = mock_api_response
                
                holiday = extract_holiday.get_holiday_data(mock_country, mock_year, mock_month)
                
                expected = {'country': 'us',
                        'year': '2021', 
                        'month': '1', 'type':'national','api_key':'api_key'}
                self.assertEqual(mock_api_response,holiday)
                