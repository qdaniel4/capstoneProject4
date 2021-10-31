import unittest 
from unittest import TestCase
from unittest.mock import patch

# from flask import Flask, request, render_template, redirect

from ui_support import ui_support
from app import app


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
        with app.test_client() as client:
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



if __name__ == '__main__':
    unittest.main()