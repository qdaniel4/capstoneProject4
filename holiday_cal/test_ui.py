from unittest import TestCase
from unittest.mock import patch
import ui

class TestUI(TestCase):
    def test_getting_ok_response(self):
        sample_json = {}
        with patch('ui.req_countries') as mock_res:
            mock_res.return_value.status_code = 200
            mock_res.return_value.json.return_value = sample_json
            
            actual = ui.req_countries()
            self.assertEqual(actual.status_code, 200)
            self.assertEqual(actual.json(), sample_json)
    
   
    @patch('requests.Response.json')
    def test_holiday_value(self,mock_req_json):
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
            