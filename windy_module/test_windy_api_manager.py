import unittest
from unittest import TestCase
from unittest.mock import patch
import windy_api_manager

class TestWindyApiManager(TestCase):
    @patch ('windy_api_manager.get_windy_response')  #still haven't made a get windy response function but wanted to turn this unittest in before the deadline
    def test_get_image_link(self, mock_response):
        mock_response.return_value = {'result': {'limit': 1,
            'offset': 0,
            'total': 1193,
            'webcams': [{'id': '1604868023',
                         'image': {'current': {'icon': 'https://images-webcams.windy.com/23/1604868023/current/icon/1604868023.jpg',
                                               'preview': 'https://images-webcams.windy.com/23/1604868023/current/preview/1604868023.jpg',
                                               'thumbnail': 'https://images-webcams.windy.com/23/1604868023/current/thumbnail/1604868023.jpg',
                                               'toenail': 'https://images-webcams.windy.com/23/1604868023/current/thumbnail/1604868023.jpg'},
                                   'daylight': {'icon': 'https://images-webcams.windy.com/23/1604868023/daylight/icon/1604868023.jpg',
                                                'preview': 'https://images-webcams.windy.com/23/1604868023/daylight/preview/1604868023.jpg',
                                                'thumbnail': 'https://images-webcams.windy.com/23/1604868023/daylight/thumbnail/1604868023.jpg',
                                                'toenail': 'https://images-webcams.windy.com/23/1604868023/daylight/thumbnail/1604868023.jpg'},
                                   'sizes': {'icon': {'height': 48,
                                                      'width': 48},
                                             'preview': {'height': 224,
                                                         'width': 400},
                                             'thumbnail': {'height': 112,
                                                           'width': 200},
                                             'toenail': {'height': 112,
                                                         'width': 200}},
                                   'update': 1635709281},
                         'location': {'city': 'Stevens Square - Loring Heights',
                                      'continent': 'North America',
                                      'continent_code': 'NA',
                                      'country': 'United States',
                                      'country_code': 'US',
                                      'latitude': 44.964378,
                                      'longitude': -93.285306,
                                      'region': 'Minnesota',
                                      'region_code': 'US.MN',
                                      'timezone': 'America/Chicago',
                                      'wikipedia': ''},
                         'status': 'active',
                         'title': 'Stevens Square - Loring Heights: I- EB @ '
                                  'Lyndale Ave'}]},
            'status': 'OK'}
        expected = mock_response.return_value.get('result').get('webcams')[0].get('image').get('daylight').get('preview')
        actual = windy_api_manager.get_image_list('44.953744,-93.293146','traffic')
        self.assertEqual(expected,actual[0])