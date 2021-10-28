from unittest import TestCase
from unittest.mock import patch
import requests
from requests.exceptions import HTTPError
import exceptions
from exceptions import ValueTooLarge,NoStateRegion
import ui
import country_api as country

class TestUI(TestCase):
        
    #  Test countries endpoint
    def test_country_code_returns_ok_response(self):
        """ testing expected dict is returned. """
        with patch('requests.Response.json') as mock_res:
            sample_response = {'country_name': 'eSwatini', 'iso-3166': 'SZ', 'total_holidays': 17, 'supported_languages': 2, 'uuid': '7dabf5c198b0bab2eaa42bb03a113e55'}
            mock_res.return_value.json.return_value = sample_response
            actual = country.req_countries()
        self.assertDictEqual(actual.json(), sample_response)
        
            
    def test_req_countries_http_failed_response(self):
        """ testing an Http error exception is raised. """
        with patch('requests.Response.json') as mock_get:
            # MOCK the request.get function to return failed http
            http_error = requests.exceptions.HTTPError()
            mock_url = 'http://fakeCalendar.com/api/v2/countries?'
            mock_get.raise_for_status.side_effect = http_error
            mock_get.return_value.json.return_value  = mock_url
            response = country.req_countries()
        self.assertTrue(response,mock_url)
        self.assertNotEqual(response,mock_url)
    
    def test_no_state_region_is_raised(self):
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
                mock_req_json.return_value = mock_api_response
                
                holiday = ui.req_holiday({ 'country': mock_country,
                        'year': mock_year, 
                        'month': mock_month,'type':'national','api_key':'api_key'})
                
                expected = {'country': 'us',
                        'year': '2021', 
                        'month': '1', 'type':'national','api_key':'api_key'}
                self.assertEqual(expected,holiday)
                