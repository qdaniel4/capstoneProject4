import unittest 
from unittest import TestCase
from unittest.mock import patch

from peewee import database_required


from ui_support import ui_support
import app


from peewee import *

from favorites_database import db_config
test_db_path = 'test_favorites.db'
db_config.database_path = test_db_path 
import favorites_database.favorites_db
from favorites_database.favorites_db import Favorite


class TestIndexWithAPIData(TestCase):
        # resources I used to figure this out...
        # https://stanford-code-the-change-guides.readthedocs.io/en/latest/guide_flask_unit_testing.html
        # https://stackoverflow.com/questions/31710064/testing-flask-routes-do-and-dont-exist
        # https://flask.palletsprojects.com/en/2.0.x/api/#flask.Flask.test_client
        # https://flask.palletsprojects.com/en/2.0.x/testing/

    def setUp(self):
        # https://treyhunner.com/2014/10/the-many-flavors-of-mock-dot-patch/
        self.list_of_countries_patch = patch('holiday_cal.holiday_api.list_of_countries')
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
        self.list_of_countries_patch = patch('holiday_cal.holiday_api.list_of_countries')
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

        expected_error_message_countries = 'No response from Calendarific API for country names.'
        expected_error_message_categories = 'No response from Windy API for webcam categories.'

        self.assertIn(expected_error_message_countries, html)
        self.assertIn(expected_error_message_categories, html)


    def tearDown(self):
        self.list_of_countries_patch.stop()
        self.show_categories_patch.stop()


class TestResultRoute(TestCase):

    def create_sample_coordinates():
        sample_coordinates = '30.069128947931752,31.22197273660886'
        return sample_coordinates


    def create_sample_holiday_data():
        sample_holiday_data = [{
            'holiday_name': 'Holiday in Egypt',
            'description': 'Ed just made this up.',
            'date': 'Jan 20 2022'
        }]
        return sample_holiday_data

    
    def create_sample_multple_holiday_data():
        sample_holiday_data = [{
            'holiday_name': 'Holiday in Egypt',
            'description': 'Ed just made this up.',
            'date': 'Jan 20 2022'
        },
        {
            'holiday_name': 'Another Holiday',
            'description': 'Ed made this one up too.',
            'date': 'Jan 25 2022'
        },
        {
            'holiday_name': 'National Party Day',
            'description': 'A holiday Ed made up for Egypt, where everyone has a party.',
            'date': 'Jan 13 2022'
        }]
        return sample_holiday_data

    
    def create_sample_weather_data():
        sample_weather_data = {
            'rain': '22 inches',
            'sunshine': '22 hours',
            'high_temp': '89 F',
            'low_temp': '45 F'
        }
        return sample_weather_data

    
    def create_sample_webcam_data():
        sample_webcam_data = ['link-01', 'link02', 'link03']
        return sample_webcam_data


    @patch('weather.weather_api.get_coordinates', side_effect=[create_sample_coordinates()])
    @patch('holiday_cal.holiday_api.get_holiday', side_effect=[create_sample_holiday_data()])
    @patch('weather.weather_api.get_climate', side_effect=[create_sample_weather_data()])
    @patch('windy_module.windy_api_manager.get_image_list', side_effect=[create_sample_webcam_data()])
    def test_get_valid_result(self, mock_get_coords, mock_get_holiday, mock_get_climate, mock_get_webcams):
        # test for user entry of Cairo, Egypt, on Jan 15 2022, Traffic webcams
        with app.app.test_client() as client:
            response = client.get('/result?city=Cairo&country=Egypt&date=2022-01-15&category=Traffic')
        html = response.data.decode()

        self.assertEqual(response.status_code, 200)

        weather_values = ['Based on historic climate data in January from previous years.',
        'Rainfall: 22 inches per month.',
        'Daylight Hours: 22 hours per day.',
        'High Temp: 89 F',
        'Low Temp: 45 F']
        holiday_values  = ['Holidays in Egypt during January:', 
        'Holiday in Egypt', 
        'Jan 20 2022', 
        'Ed just made this up.']
        webcam_values = ['img src="link-01"',
        'img src="link02"',
        'img src="link03"']
        result_header = 'Results for Cairo, Egypt in 01/2022.'

        self.assertIn(result_header, html)
        for weather_value in weather_values:
            self.assertIn(weather_value, html)
        for holiday_value in holiday_values:
            self.assertIn(holiday_value, html)
        for webcam_value in webcam_values:
            self.assertIn(webcam_value, html)


    @patch('weather.weather_api.get_coordinates', side_effect=[None])
    @patch('holiday_cal.holiday_api.get_holiday', side_effect=[create_sample_holiday_data()])
    @patch('weather.weather_api.get_climate', side_effect=[create_sample_weather_data()])
    @patch('windy_module.windy_api_manager.get_image_list', side_effect=[create_sample_webcam_data()])
    def test_get_result_with_no_coordinates_shows_error_page(self, mock_get_coords, mock_get_holiday, mock_get_climate, mock_get_webcams):
        # test for user entry of Cairo, Egypt, on Jan 15 2022, Traffic webcams
        with app.app.test_client() as client:
            response = client.get('/result?city=Cairo&country=Egypt&date=2022-01-15&category=Traffic')
        html = response.data.decode()
        expected_error_html = 'Error getting location information from API. Please double check city name and country and try again.'
        
        self.assertIn(expected_error_html, html)


    @patch('weather.weather_api.get_coordinates', side_effect=[create_sample_coordinates()])
    @patch('holiday_cal.holiday_api.get_holiday', side_effect=[None])
    @patch('weather.weather_api.get_climate', side_effect=[None])
    @patch('windy_module.windy_api_manager.get_image_list', side_effect=[None])
    def test_result_page_shows_correct_error_messages_when_no_optional_data_from_APIs(self, mock_get_coords, mock_get_holiday, mock_get_climate, mock_get_webcams):
        # test for user entry of Cairo, Egypt, on Jan 15 2022, Traffic webcams
        with app.app.test_client() as client:
            response = client.get('/result?city=Cairo&country=Egypt&date=2022-01-15&category=Traffic')
        html = response.data.decode()
        expected_error_html = ['No weather data found for Egypt during January.',
        'No holidays found for Egypt during January.',
        'No webcams were found for Egypt. Try selecting a different category.']
        
        for expected_error in expected_error_html:
            self.assertIn(expected_error, html)


    @patch('weather.weather_api.get_coordinates', side_effect=[create_sample_coordinates()])
    @patch('holiday_cal.holiday_api.get_holiday', side_effect=[None])
    @patch('weather.weather_api.get_climate', side_effect=[None])
    @patch('windy_module.windy_api_manager.get_image_list', side_effect=[None])
    def test_result_page_does_not_show_html_with_blank_entries_when_no_optional_data_from_APIs(self, mock_get_coords, mock_get_holiday, mock_get_climate, mock_get_webcams):
        # test for user entry of Cairo, Egypt, on Jan 15 2022, Traffic webcams
        with app.app.test_client() as client:
            response = client.get('/result?city=Cairo&country=Egypt&date=2022-01-15&category=Traffic')
        html = response.data.decode()

        weather_values = ['Based on historic climate data in January from previous years.',
        'Rainfall:',
        'Daylight Hours:',
        'High Temp:',
        'Low Temp:']
        holiday_value  = 'Holidays in Egypt during January:'
        webcam_value = '<img src="" />'

        for weather_value in weather_values:
            self.assertNotIn(weather_value, html)
        self.assertNotIn(holiday_value, html)
        self.assertNotIn(webcam_value, html)


    @patch('weather.weather_api.get_coordinates', side_effect=[create_sample_coordinates()])
    @patch('holiday_cal.holiday_api.get_holiday', side_effect=[create_sample_holiday_data()])
    @patch('weather.weather_api.get_climate', side_effect=[None])
    @patch('windy_module.windy_api_manager.get_image_list', side_effect=[None])
    def test_result_page_shows_correct_error_messages_when_only_some_optional_data_from_APIs(self, mock_get_coords, mock_get_holiday, mock_get_climate, mock_get_webcams):
        # test for user entry of Cairo, Egypt, on Jan 15 2022, Traffic webcams
        with app.app.test_client() as client:
            response = client.get('/result?city=Cairo&country=Egypt&date=2022-01-15&category=Traffic')
        html = response.data.decode()
        expected_error_html = ['No weather data found for Egypt during January.',
        'No webcams were found for Egypt. Try selecting a different category.']
        not_expected_error_html = 'No holidays found for Egypt during January.'
        holiday_values  = ['Holidays in Egypt during January:', 
        'Holiday in Egypt', 
        'Jan 20 2022', 
        'Ed just made this up.']

        for expected_error in expected_error_html:
            self.assertIn(expected_error, html)
        self.assertNotIn(not_expected_error_html, html)
        for holiday_value in holiday_values:
            self.assertIn(holiday_value, html)


    @patch('weather.weather_api.get_coordinates', side_effect=[create_sample_coordinates()])
    @patch('holiday_cal.holiday_api.get_holiday', side_effect=[create_sample_multple_holiday_data()])
    @patch('weather.weather_api.get_climate', side_effect=[None])
    @patch('windy_module.windy_api_manager.get_image_list', side_effect=[None])
    def test_result_page_shows_multiple_holidays(self, mock_get_coords, mock_get_holiday, mock_get_climate, mock_get_webcams):
        # test for user entry of Cairo, Egypt, on Jan 15 2022, Traffic webcams
        with app.app.test_client() as client:
            response = client.get('/result?city=Cairo&country=Egypt&date=2022-01-15&category=Traffic')
        html = response.data.decode()
        holiday_values  = ['Holidays in Egypt during January:', 
        'Holiday in Egypt', 
        'Jan 20 2022', 
        'Ed just made this up.',
        'Another Holiday', 
        'Jan 25 2022', 
        'Ed made this one up too.',
        'National Party Day', 
        'Jan 13 2022', 
        'A holiday Ed made up for Egypt, where everyone has a party.']

        for holiday_value in holiday_values:
            self.assertIn(holiday_value, html)


class TestFavoritesRoute(TestCase):

    def get_response_favorites(self):
        with app.app.test_client() as client:
            response = client.get('/favorites')
        # get html from the response
        html = response.data.decode()
        return html


    def create_favorite():
        favorite = Favorite(id=1, city="City1", country="Country1", month=1, year=2020, webcam="http://url.com/", weather="weather", holidays="holiday1, holiday2", nickname="nickname")
        favorite_list = [favorite]
        return favorite_list 


    def create_favorites():
        favorite_one = Favorite(id=1, city="City1", country="Country1", month=1, year=2020, webcam="http://url.com/", weather="weather", holidays="holiday1, holiday2", nickname="nickname")
        favorite_two = Favorite(id=2, city="City2", country="Country2", month=12, year=2023, webcam="http://url.com/", weather="weather", holidays="holiday1, holiday2")
        favorite_three = Favorite(id=3, city="City3", country="Country3", month=5, year=2021, webcam="http://url.com/", weather="weather", holidays="holiday1, holiday2")
        favorite_four = Favorite(id=4, city="City4", country="Country4", month=3, year=2024, webcam="http://url.com/", weather="weather", holidays="holiday1, holiday2", nickname="name")
        favorite_list = [favorite_one, favorite_two, favorite_three, favorite_four]
        return favorite_list


    @patch('favorites_database.favorites_db.get_all_favorites', side_effect=[create_favorite()])
    def test_favorites_page_with_one_favorite(self, mock_get_favorites):
        html = self.get_response_favorites()
        expected_in_favorites_table = ['City1, Country1',
            '1/2020',
            'href="/favorite/1">Show Results</a>',
            'href="/favorite/delete/1">Delete</a>']
        
        for expected_favorite in expected_in_favorites_table:
            self.assertIn(expected_favorite, html)


    @patch('favorites_database.favorites_db.get_all_favorites', side_effect=[create_favorites()])
    def test_favorites_page_with_multiple_favorites(self, mock_get_favorites):
        html = self.get_response_favorites()
        expected_in_favorites_table = ['City1, Country1',
            '1/2020',
            'City2, Country2',
            '12/2023',
            'href="/favorite/2">Show Results</a>',
            'href="/favorite/delete/2">Delete</a>',
            'City3, Country3',
            '5/2021',
            'href="/favorite/3">Show Results</a>',
            'href="/favorite/delete/3">Delete</a>',
            'City4, Country4',
            '3/2024',
            'href="/favorite/4">Show Results</a>',
            'href="/favorite/delete/4">Delete</a>']
        
        for expected_favorite in expected_in_favorites_table:
            self.assertIn(expected_favorite, html)


    @patch('favorites_database.favorites_db.get_all_favorites', side_effect=[[]])
    def test_favorites_page_with_no_favorites(self, mock_get_favorites):
        html = self.get_response_favorites()
        expected_no_favorites_message = 'There are no favorites to display. Try searching for a location and adding it to your favorites!'

        self.assertIn(expected_no_favorites_message, html)


class TestFavoriteAddRoute(TestCase):
    test_db_url = 'test_quiz.db'

    """
    Create expected Favorites table
    """

    def setUp(self):
        """Clear and remake favorites table for test database."""
        self.db = SqliteDatabase(test_db_path)
        self.db.drop_tables([Favorite])
        self.db.create_tables([Favorite])


    def create_sample_result(self):
        sample_coordinates = '30.069128947931752,31.22197273660886'
        sample_holiday_data = [{
            'holiday_name': 'Holiday in Egypt',
            'description': 'Ed just made this up.',
            'date': 'Jan 20 2022'
        },
        {
            'holiday_name': 'Another Holiday',
            'description': 'Ed made this one up too.',
            'date': 'Jan 25 2022'
        },
        {
            'holiday_name': 'National Party Day',
            'description': 'A holiday Ed made up for Egypt, where everyone has a party.',
            'date': 'Jan 13 2022'
        }]
        sample_weather_data = {
                    'rain': '22 inches',
                    'sunshine': '22 hours',
                    'high_temp': '89 F',
                    'low_temp': '45 F'
                }
        sample_webcam_data = ['http://link.com', 'http://link2.com', 'http://link3.com']
        result = {
            'city': 'Cairo',
            'country': 'Egypt',
            'month': '01',
            'month_name': 'January',
            'year': '2022',
            'webcams': sample_webcam_data,
            'holidays': sample_holiday_data,
            'weather': sample_weather_data
        }
        return result


    def test_save_favorite_from_result_page(self):
        result = self.create_sample_result()
        result_string = f"{result['city']}\{result['country']}\{result['month']}\{result['year']}\{result['webcams']}\{result['weather']}\{result['holidays']}"
        with app.app.test_client() as client:
            response = client.post('/favorite/add', data={'result': result_string})

        favorite = Favorite.get_or_none(id=1)
        expected_city = 'Cairo' 
        expected_webcam = "['http://link.com', 'http://link2.com', 'http://link3.com']"

        self.assertEqual(expected_city, favorite.city)
        self.assertEqual(expected_webcam, favorite.webcam)
        self.assertIsNotNone(favorite)


class TestResultFavoritebyIDRoute(TestCase):
    test_db_url = 'test_quiz.db'

    """
    Create expected Favorites table
    """

    def setUp(self):
        """Clear and remake favorites table for test database."""
        self.db = SqliteDatabase(test_db_path)
        self.db.drop_tables([Favorite])
        self.db.create_tables([Favorite])


    def create_sample_result(self):
        sample_coordinates = '30.069128947931752,31.22197273660886'
        sample_holiday_data = [{
            'holiday_name': 'Holiday in Egypt',
            'description': 'Ed just made this up.',
            'date': 'Jan 20 2022'
        },
        {
            'holiday_name': 'Another Holiday',
            'description': 'Ed made this one up too.',
            'date': 'Jan 25 2022'
        },
        {
            'holiday_name': 'National Party Day',
            'description': 'A holiday Ed made up for Egypt, where everyone has a party.',
            'date': 'Jan 13 2022'
        }]
        sample_weather_data = {
                    'rain': '22 inches',
                    'sunshine': '22 hours',
                    'high_temp': '89 F',
                    'low_temp': '45 F'
                }
        sample_webcam_data = ['http://link.com', 'http://link2.com', 'http://link3.com']
        result = {
            'city': 'Cairo',
            'country': 'Egypt',
            'month': '01',
            'month_name': 'January',
            'year': '2022',
            'webcams': sample_webcam_data,
            'holidays': sample_holiday_data,
            'weather': sample_weather_data
        }
        return result


    def create_and_save_favorites(self):
        result = self.create_sample_result()
        favorites_database.favorites_db.add_favorite(result['city'], result['country'], result['month'], result['year'], result['webcams'], result['weather'], result['holidays'])
        favorites_database.favorites_db.add_favorite(result['city'], result['country'], result['month'], result['year'], None, None, None)
        favorites_database.favorites_db.add_favorite(result['city'], result['country'], result['month'], result['year'], 'None', 'None', 'None')


    def test_display_results_for_favorite_from_database(self):
        self.create_and_save_favorites()
        with app.app.test_client() as client:
            response = client.get('/favorite/1')
        html = response.data.decode()

        self.assertEqual(response.status_code, 200)

        weather_values = ['Based on historic climate data in January from previous years.',
        'Rainfall: 22 inches per month.',
        'Daylight Hours: 22 hours per day.',
        'High Temp: 89 F',
        'Low Temp: 45 F']
        holiday_values  = ['Holidays in Egypt during January:', 
        'Holiday in Egypt', 
        'Jan 20 2022', 
        'Ed just made this up.']
        webcam_values = ['"http://link.com"',
        '"http://link2.com"',
        '"http://link3.com"']
        result_header = 'Results for Cairo, Egypt in 1/2022.'

        self.assertIn(result_header, html)
        for weather_value in weather_values:
            self.assertIn(weather_value, html)
        for holiday_value in holiday_values:
            self.assertIn(holiday_value, html)
        for webcam_value in webcam_values:
            self.assertIn(webcam_value, html)


    def test_result_page_shows_correct_error_messages_when_None_values_from_DB(self):
        # test for favorite with ID 2 which has 3 None values
        self.create_and_save_favorites()
        with app.app.test_client() as client:
            response = client.get('/favorite/2')
        html = response.data.decode()

        self.assertEqual(response.status_code, 200)

        expected_error_html = ['No weather data found for Egypt during January.',
        'No holidays found for Egypt during January.',
        'No webcams were found for Egypt. Try selecting a different category.']
        
        for expected_error in expected_error_html:
            self.assertIn(expected_error, html)


    def test_result_page_does_not_show_html_with_blank_entries_when_None_values_from_DB(self):
        # test for favorite with ID 2 which has 3 None values
        self.create_and_save_favorites()
        with app.app.test_client() as client:
            response = client.get('/favorite/2')
        html = response.data.decode()

        self.assertEqual(response.status_code, 200)

        weather_values = ['Based on historic climate data in January from previous years.',
        'Rainfall:',
        'Daylight Hours:',
        'High Temp:',
        'Low Temp:']
        holiday_value  = 'Holidays in Egypt during January:'
        webcam_value = 'src="" />'

        for weather_value in weather_values:
            self.assertNotIn(weather_value, html)
        self.assertNotIn(holiday_value, html)
        self.assertNotIn(webcam_value, html)


    def test_result_page_shows_correct_error_messages_when_None_strings_from_DB(self):
        # test for favorite with ID 3 which has 3 'None' strings
        self.create_and_save_favorites()
        with app.app.test_client() as client:
            response = client.get('/favorite/3')
        html = response.data.decode()

        self.assertEqual(response.status_code, 200)

        expected_error_html = ['No weather data found for Egypt during January.',
        'No holidays found for Egypt during January.',
        'No webcams were found for Egypt. Try selecting a different category.']
        
        for expected_error in expected_error_html:
            self.assertIn(expected_error, html)


    def test_result_page_does_not_show_html_with_blank_entries_when_None_strings_from_DB(self):
        # test for favorite with ID 3 which has 3 'None' strings
        self.create_and_save_favorites()
        with app.app.test_client() as client:
            response = client.get('/favorite/3')
        html = response.data.decode()

        self.assertEqual(response.status_code, 200)

        weather_values = ['Based on historic climate data in January from previous years.',
        'Rainfall:',
        'Daylight Hours:',
        'High Temp:',
        'Low Temp:']
        holiday_value  = 'Holidays in Egypt during January:'
        webcam_value = 'src=""'

        for weather_value in weather_values:
            self.assertNotIn(weather_value, html)
        self.assertNotIn(holiday_value, html)
        self.assertNotIn(webcam_value, html)


class TestFavoriteDeleteRoute(TestCase):
    test_db_url = 'test_quiz.db'

    """
    Create expected Favorites table
    """

    def setUp(self):
        """Clear and remake favorites table for test database."""
        self.db = SqliteDatabase(test_db_path)
        self.db.drop_tables([Favorite])
        self.db.create_tables([Favorite])


    def create_sample_result(self):
        sample_coordinates = '30.069128947931752,31.22197273660886'
        sample_holiday_data = [{
            'holiday_name': 'Holiday in Egypt',
            'description': 'Ed just made this up.',
            'date': 'Jan 20 2022'
        },
        {
            'holiday_name': 'Another Holiday',
            'description': 'Ed made this one up too.',
            'date': 'Jan 25 2022'
        },
        {
            'holiday_name': 'National Party Day',
            'description': 'A holiday Ed made up for Egypt, where everyone has a party.',
            'date': 'Jan 13 2022'
        }]
        sample_weather_data = {
                    'rain': '22 inches',
                    'sunshine': '22 hours',
                    'high_temp': '89 F',
                    'low_temp': '45 F'
                }
        sample_webcam_data = ['http://link.com', 'http://link2.com', 'http://link3.com']
        result = {
            'city': 'Cairo',
            'country': 'Egypt',
            'month': '01',
            'month_name': 'January',
            'year': '2022',
            'webcams': sample_webcam_data,
            'holidays': sample_holiday_data,
            'weather': sample_weather_data
        }
        return result


    def create_and_save_favorites(self):
        result = self.create_sample_result()
        favorites_database.favorites_db.add_favorite(result['city'], result['country'], result['month'], result['year'], result['webcams'], result['weather'], result['holidays'])
        favorites_database.favorites_db.add_favorite(result['city'], result['country'], result['month'], result['year'], None, None, None)
        favorites_database.favorites_db.add_favorite(result['city'], result['country'], result['month'], result['year'], 'None', 'None', 'None')


    def test_delete_favorite_from_database(self):
        self.create_and_save_favorites()
        with app.app.test_client() as client:
            response = client.get('/favorite/delete/1')
        html = response.data.decode()

        favorite_was_deleted = Favorite.get_or_none(id=1)
        # check to see favorites page is displayed with some info that was not deleted from db
        expected_favorites_page_html = [
        'Cairo, Egypt',
        'href="/favorite/3">Show Results</a>',
        'href="/favorite/delete/3">Delete</a>'
        ]

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(favorite_was_deleted)
        for expected_favorite_html in expected_favorites_page_html:
            self.assertIn(expected_favorite_html, html)


    def test_delete_favorite_not_in_database_shows_error(self):
        self.create_and_save_favorites()
        with app.app.test_client() as client:
            response = client.get('/favorite/delete/8')
        html = response.data.decode()

        expected_error_message = 'Favorite with ID: 8 not found in database.'

        self.assertEqual(response.status_code, 200)
        self.assertIn(expected_error_message, html)


    def test_delete_favorite_from_database_with_delete_not_get(self):
        # was originally testing with delete method
        # but the program when running actually uses get for this
        self.create_and_save_favorites()
        with app.app.test_client() as client:
            response = client.delete('/favorite/delete/1')
        html = response.data.decode()

        favorite_was_deleted = Favorite.get_or_none(id=1)
        # check to see favorites page is displayed with some info that was not deleted from db
        expected_favorites_page_html = [
        'Cairo, Egypt',
        'href="/favorite/3">Show Results</a>',
        'href="/favorite/delete/3">Delete</a>'
        ]

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(favorite_was_deleted)
        for expected_favorite_html in expected_favorites_page_html:
            self.assertIn(expected_favorite_html, html)


    def test_delete_favorite_not_in_database_shows_error_with_delete_not_get(self):
        self.create_and_save_favorites()
        with app.app.test_client() as client:
            response = client.delete('/favorite/delete/8')
        html = response.data.decode()

        expected_error_message = 'Favorite with ID: 8 not found in database.'

        self.assertEqual(response.status_code, 200)
        self.assertIn(expected_error_message, html)


if __name__ == '__main__':
    unittest.main()