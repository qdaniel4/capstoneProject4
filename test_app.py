import unittest 
from unittest import TestCase
from unittest.mock import patch

# from flask import Flask, request, render_template, redirect

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

        self.show_categories_patch = patch('scratch_module.show_categories')
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

        # TODO: replace scratch_module with correct modules after merge
        self.show_categories_patch = patch('scratch_module.show_categories')
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


    def get_response_result(self, param_string):
        # get a response with test_client version of Flask app
        url = f'/result{param_string}'
        with app.app.test_client() as client:
            response = client.get(url)
        # get html from the response
        html = response.data.decode()
        return response, html


    # TODO: this is very messy and it would be nice to clean it up a little
    @patch('scratch_module.get_coordinates', side_effect=['30.069128947931752,31.22197273660886'])
    @patch('scratch_module.get_holiday_data', side_effect=[[{
            'name': 'Holiday in Egypt',
            'description': 'Ed just made this up.',
            'date': 'Jan 20 2022'
        }]])
    @patch('scratch_module.get_climate', side_effect=[{
            'rainfall': '22 inches',
            'daylight': '22 hours',
            'hightemp': '89 F',
            'lowtemp': '45 F'
        }])
    @patch('scratch_module.get_image_list', side_effect=[['link-01', 'link02', 'link03']])
    def test_get_valid_result(self, mock_get_coords, mock_get_holiday, mock_get_climate, mock_get_webcams):
        # TODO: change so this uses get_response_result
        # test for user entry of Cairo, Egypt, on Jan 15 2022, Traffic webcams
        with app.app.test_client() as client:
            response = client.get('/result?city=Cairo&country=Egypt&date=01/15/2022&category=Traffic')
        html = response.data.decode()

        # expected data
        weather_info = '''<h3>Weather</h3>
    <p><i>Based on historic climate data in January from previous years.</i></p>

        <ul>
            <li>Rainfall: 22 inches</li>
            <li>Daylight Hours: 22 hours</li>
            <li>High Temp: 89 F</li>
            <li>Low Temp: 45 F</li>
        </ul>'''

        holiday_heading = '<h3>Holidays in Egypt during January:</h3>'
        holiday_info  = '''<p>Holiday in Egypt</p>
    <ul>
        <li>Jan 20 2022</li>
        <li>Ed just made this up.</li>
    </ul>
    <br>'''

        webcams = ['<img url="link-01" />',
        '<img url="link02" />',
        '<img url="link03" />']

        result_header = '<h2 id="result-title">Results for Cairo, Egypt in 01/2022.</h2>'


        self.assertIn(weather_info, html)
        self.assertIn(holiday_heading, html)
        self.assertIn(holiday_info, html)
        for webcam in webcams:
            self.assertIn(webcam, html)
        self.assertIn(result_header, html)

        
if __name__ == '__main__':
    unittest.main()