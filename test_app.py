import unittest 
from unittest import TestCase
from unittest.mock import patch

from ui_support import ui_support
import app




class TestIndexWithAPIData(TestCase):
        # resources I used to figure this out...
        # https://stanford-code-the-change-guides.readthedocs.io/en/latest/guide_flask_unit_testing.html
        # https://stackoverflow.com/questions/31710064/testing-flask-routes-do-and-dont-exist
        # https://flask.palletsprojects.com/en/2.0.x/api/#flask.Flask.test_client
        # https://flask.palletsprojects.com/en/2.0.x/testing/

    def setUp(self):
        # https://treyhunner.com/2014/10/the-many-flavors-of-mock-dot-patch/
        self.list_of_countries_patch = patch('scratch_module.list_of_countries')
        self.list_of_countries = self.list_of_countries_patch.start()
        self.list_of_countries.return_value = [{"country_name": "Afghanistan","country_code": "AF"},{"country_name": "Albania","country_code": "AL"}]

        self.show_categories_patch = patch('windy_module.windy_api_manager.show_categories')
        self.show_categories = self.show_categories_patch.start()
        self.show_categories.return_value = ['Beach', 'Harbor', 'Traffic']


    def get_response_index(self):
        # get a response with test_client version of Flask app
        with app.app.test_client() as client:
            response = client.get('/')
        # get html from the response
        html = response.data.decode()
        return response, html


    def test_index(self):
        response, html = self.get_response_index()
        # assert response was successful
        self.assertEqual(response.status_code, 200)


    def test_index_options_for_country_select(self):
        response, html = self.get_response_index()

        expected_select_for_categories_afghanistan_option = '<option value="Afghanistan">Afghanistan</option>'
        expected_select_for_categories_albania_option = '<option value="Albania">Albania</option>'

        self.assertIn(expected_select_for_categories_afghanistan_option, html)
        self.assertIn(expected_select_for_categories_albania_option, html)


    def test_index_options_for_webcam_API_category_select(self):
        response, html = self.get_response_index()

        expected_select_for_categories_beach_option = '<option value="Beach">Beach</option>'
        expected_select_for_categories_harbor_option = '<option value="Harbor">Harbor</option>'
        expected_select_for_categories_traffic_option = '<option value="Traffic">Traffic</option>'

        self.assertIn(expected_select_for_categories_beach_option, html)
        self.assertIn(expected_select_for_categories_harbor_option, html)
        self.assertIn(expected_select_for_categories_traffic_option, html)


    def tearDown(self):
        self.list_of_countries_patch.stop()
        self.show_categories_patch.stop()


class TestIndexWithNoAPIData(TestCase):

    def setUp(self):
        # TODO: replace scratch_module with correct modules after merge
        self.list_of_countries_patch = patch('scratch_module.list_of_countries')
        self.list_of_countries = self.list_of_countries_patch.start()
        self.list_of_countries.return_value = None

        self.show_categories_patch = patch('windy_module.windy_api_manager.show_categories')
        self.show_categories = self.show_categories_patch.start()
        self.show_categories.return_value = None


    def get_response_index(self):
        # get a response with test_client version of Flask app
        with app.app.test_client() as client:
            response = client.get('/')
        # get html from the response
        html = response.data.decode()
        return response, html


    def test_index(self):
        response, html = self.get_response_index()
        # assert response was successful
        self.assertEqual(response.status_code, 200)


    def test_error_messages_present(self):
        response, html = self.get_response_index()

        expected_error_message_countries = '<li>No response from Calendarific API for country names.</li>'
        expected_error_message_categories = '<li>No response from Windy API for webcam categories.</li>'

        self.assertIn(expected_error_message_countries, html)
        self.assertIn(expected_error_message_categories, html)


    def tearDown(self):
        self.list_of_countries_patch.stop()
        self.show_categories_patch.stop()


class TestResult(TestCase):

    # TODO: this is very messy and it would be nice to clean it up a little
    @patch('weather.weather_api.get_coordinates', side_effect=['30.069128947931752,31.22197273660886'])
    @patch('scratch_module.get_holiday_data', side_effect=[[{
            'holiday_name': 'Holiday in Egypt',
            'description': 'Ed just made this up.',
            'date': 'Jan 20 2022'
        }]])
    @patch('weather.weather_api.get_climate', side_effect=[{
            'rain': '22 inches',
            'sunshine': '22 hours',
            'high_temp': '89 F',
            'low_temp': '45 F'
        }])
    @patch('windy_module.windy_api_manager.get_image_list', side_effect=[['link-01', 'link02', 'link03']])
    def test_get_valid_result(self, mock_get_coords, mock_get_holiday, mock_get_climate, mock_get_webcams):
        # test for user entry of Cairo, Egypt, on Jan 15 2022, Traffic webcams
        with app.app.test_client() as client:
            response = client.get('/result?city=Cairo&country=Egypt&date=01/15/2022&category=Traffic')
        html = response.data.decode()

        self.assertEqual(response.status_code, 200)

        # expected data
        weather_values = ['<p><i>Based on historic climate data in January from previous years.</i></p>',
        '<li>Rainfall: 22 inches per month.</li>',
        '<li>Daylight Hours: 22 hours per day.</li>',
        '<li>High Temp: 89 F</li>',
        '<li>Low Temp: 45 F</li>']
        holiday_values  = ['<h3>Holidays in Egypt during January:</h3>', 
        '<p>Holiday in Egypt</p>', 
        '<li>Jan 20 2022</li>', 
        '<li>Ed just made this up.</li>']
        webcam_values = ['<img url="link-01" />',
        '<img url="link02" />',
        '<img url="link03" />']
        result_header = '<h2 id="result-title">Results for Cairo, Egypt in 01/2022.</h2>'

        self.assertIn(result_header, html)
        for weather_value in weather_values:
            self.assertIn(weather_value, html)
        for holiday_value in holiday_values:
            self.assertIn(holiday_value, html)
        for webcam_value in webcam_values:
            self.assertIn(webcam_value, html)


    # error page is displayed if coordinates = None
    @patch('weather.weather_api.get_coordinates', side_effect=[None])
    @patch('scratch_module.get_holiday_data', side_effect=[[{
            'holiday_name': 'Holiday in Egypt',
            'description': 'Ed just made this up.',
            'date': 'Jan 20 2022'
        }]])
    @patch('weather.weather_api.get_climate', side_effect=[{
            'rain': '22 inches',
            'sunshine': '22 hours',
            'high_temp': '89 F',
            'low_temp': '45 F'
        }])
    @patch('windy_module.windy_api_manager.get_image_list', side_effect=[['link-01', 'link02', 'link03']])
    def test_get_result_with_no_coordinates_shows_error_page(self, mock_get_coords, mock_get_holiday, mock_get_climate, mock_get_webcams):
        # test for user entry of Cairo, Egypt, on Jan 15 2022, Traffic webcams
        with app.app.test_client() as client:
            response = client.get('/result?city=Cairo&country=Egypt&date=01/15/2022&category=Traffic')
        html = response.data.decode()
        expected_error_html = '<li>Error getting location information from API. Please double check city name and country and try again.</li>'
        
        self.assertIn(expected_error_html, html)


    # correct messages displayed to user when optional API data is not found
    @patch('weather.weather_api.get_coordinates', side_effect=['30.069128947931752,31.22197273660886'])
    @patch('scratch_module.get_holiday_data', side_effect=[None])
    @patch('weather.weather_api.get_climate', side_effect=[None])
    @patch('windy_module.windy_api_manager.get_image_list', side_effect=[None])
    def test_result_page_shows_correct_error_messages_when_no_optional_data_from_APIs(self, mock_get_coords, mock_get_holiday, mock_get_climate, mock_get_webcams):
        # test for user entry of Cairo, Egypt, on Jan 15 2022, Traffic webcams
        with app.app.test_client() as client:
            response = client.get('/result?city=Cairo&country=Egypt&date=01/15/2022&category=Traffic')
        html = response.data.decode()
        expected_error_html = ['<h3>No weather data found for Egypt during January.</h3>',
        '<h3>No holidays found for Egypt during January.</h3>',
        '<h3>No webcams were found for Egypt. Try selecting a different category.</h3>']
        
        for expected_error in expected_error_html:
            self.assertIn(expected_error, html)


    # empty html not displayed to user when optional API data is not found
    @patch('weather.weather_api.get_coordinates', side_effect=['30.069128947931752,31.22197273660886'])
    @patch('scratch_module.get_holiday_data', side_effect=[None])
    @patch('weather.weather_api.get_climate', side_effect=[None])
    @patch('windy_module.windy_api_manager.get_image_list', side_effect=[None])
    def test_result_page_does_not_show_html_with_blank_entries_when_no_optional_data_from_APIs(self, mock_get_coords, mock_get_holiday, mock_get_climate, mock_get_webcams):
        # test for user entry of Cairo, Egypt, on Jan 15 2022, Traffic webcams
        with app.app.test_client() as client:
            response = client.get('/result?city=Cairo&country=Egypt&date=01/15/2022&category=Traffic')
        html = response.data.decode()

        weather_values = ['<p><i>Based on historic climate data in January from previous years.</i></p>',
        '<li>Rainfall:',
        '<li>Daylight Hours:',
        '<li>High Temp:',
        '<li>Low Temp:']
        holiday_value  = '<h3>Holidays in Egypt during January:</h3>'
        webcam_value = '<img url="" />'

        for weather_value in weather_values:
            self.assertNotIn(weather_value, html)
        self.assertNotIn(holiday_value, html)
        self.assertNotIn(webcam_value, html)


    # correct messages displayed to user when some optional API data is not found
    @patch('weather.weather_api.get_coordinates', side_effect=['30.069128947931752,31.22197273660886'])
    @patch('scratch_module.get_holiday_data', side_effect=[[{
            'holiday_name': 'Holiday in Egypt',
            'description': 'Ed just made this up.',
            'date': 'Jan 20 2022'
        }]])
    @patch('weather.weather_api.get_climate', side_effect=[None])
    @patch('windy_module.windy_api_manager.get_image_list', side_effect=[None])
    def test_result_page_shows_correct_error_messages_when_only_some_optional_data_from_APIs(self, mock_get_coords, mock_get_holiday, mock_get_climate, mock_get_webcams):
        # test for user entry of Cairo, Egypt, on Jan 15 2022, Traffic webcams
        with app.app.test_client() as client:
            response = client.get('/result?city=Cairo&country=Egypt&date=01/15/2022&category=Traffic')
        html = response.data.decode()
        expected_error_html = ['<h3>No weather data found for Egypt during January.</h3>',
        '<h3>No webcams were found for Egypt. Try selecting a different category.</h3>']
        not_expected_error_html = '<h3>No holidays found for Egypt during January.</h3>'
        holiday_values  = ['<h3>Holidays in Egypt during January:</h3>', 
        '<p>Holiday in Egypt</p>', 
        '<li>Jan 20 2022</li>', 
        '<li>Ed just made this up.</li>']

        for expected_error in expected_error_html:
            self.assertIn(expected_error, html)
        self.assertNotIn(not_expected_error_html, html)
        for holiday_value in holiday_values:
            self.assertIn(holiday_value, html)

if __name__ == '__main__':
    unittest.main()