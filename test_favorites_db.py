
import unittest 
from unittest import TestCase
from peewee import *

import db_config
test_db_path = 'test_favorites.db'
db_config.database_path = test_db_path 

import favorites_db
from favorites_db import Favorite
from favorites_db import FavoritesError

class FavoritesTest(TestCase):

    test_db_url = 'test_quiz.db'

    """
    Before running these test, test_favorites.db
    Create expected Favorites table
    """

    def setUp(self):
        """Clear and remake favorites table for test database."""
        self.db = SqliteDatabase(test_db_path)
        self.db.drop_tables([Favorite])
        self.db.create_tables([Favorite])

    
    def test_get_favorites_returns_list_of_favorites_from_db(self):
        favorite_one = Favorite(city="City1", country="Country1", month=1, year=2020, webcam="http://url.com/", weather="weather", holidays="holiday1, holiday2", nickname="nickname")
        favorite_two = Favorite(city="City2", country="Country2", month=7, year=2020, webcam="http://url3.com/", weather="weather", holidays="holiday1", nickname="nickname")
        favorite_one.save()
        favorite_two.save()

        empty_list = []
        list_of_favorites = favorites_db.get_favorites()

        self.assertNotEqual(empty_list, list_of_favorites)


    def test_get_favorites_returns_empty_list_when_no_records_in_db(self):
        empty_list = []
        empty_list_of_favorites = favorites_db.get_favorites()

        self.assertEqual(empty_list_of_favorites, empty_list)

    
    def test_delete_favorite_from_db(self):
        favorite_one = Favorite(city="City1", country="Country1", month=1, year=2020, webcam="http://url.com/", weather="weather", holidays="holiday1, holiday2", nickname="nickname")
        favorite_two = Favorite(city="City2", country="Country2", month=7, year=2020, webcam="http://url3.com/", weather="weather", holidays="holiday1", nickname="nickname")
        favorite_one.save()
        favorite_two.save()

        favorites_db.delete_favorite(2)

        was_deleted = Favorite.get_or_none(id=2)

        self.assertIsNone(was_deleted)


    def test_delete_favorite_returns_True_when_deleted(self):
        favorite_one = Favorite(city="City1", country="Country1", month=1, year=2020, webcam="http://url.com/", weather="weather", holidays="holiday1, holiday2", nickname="nickname")
        favorite_two = Favorite(city="City2", country="Country2", month=7, year=2020, webcam="http://url3.com/", weather="weather", holidays="holiday1", nickname="nickname")
        favorite_one.save()
        favorite_two.save()

        was_deleted = favorites_db.delete_favorite(2)

        self.assertTrue(was_deleted)


    def test_delete_favorite_returns_False_when_valid_id_not_in_database(self):
        favorite_one = Favorite(city="City1", country="Country1", month=1, year=2020, webcam="http://url.com/", weather="weather", holidays="holiday1, holiday2", nickname="nickname")
        favorite_two = Favorite(city="City2", country="Country2", month=7, year=2020, webcam="http://url3.com/", weather="weather", holidays="holiday1", nickname="nickname")
        favorite_one.save()
        favorite_two.save()
        favorite_two.delete().execute()
        
        was_deleted = favorites_db.delete_favorite(2)

        self.assertFalse(was_deleted)


    def test_delete_favorite_returns_False_when_invalid_id_type(self):
        favorite_one = Favorite(city="City1", country="Country1", month=1, year=2020, webcam="http://url.com/", weather="weather", holidays="holiday1, holiday2", nickname="nickname")
        favorite_two = Favorite(city="City2", country="Country2", month=7, year=2020, webcam="http://url3.com/", weather="weather", holidays="holiday1", nickname="nickname")
        favorite_one.save()
        
        was_deleted = favorites_db.delete_favorite('asdf')

        self.assertFalse(was_deleted) 


    def test_add_favorite(self):
        city = 'city1'
        country = 'country1'
        month = 2
        year = 2022
        webcam = 'webcamlink'
        weather = 'weatherdata'
        holidays = 'holidays'
        nickname = 'nickname'

        favorites_db.add_favorite(city, country, month, year, webcam, weather, holidays, nickname)

        added_favorite = Favorite.get_or_none(city = 'city1')
        
        self.assertIsNotNone(added_favorite)


    def test_add_favorite_no_nickname(self):
        city = 'city1'
        country = 'country1'
        month = 2
        year = 2022
        webcam = 'webcamlink'
        weather = 'weatherdata'
        holidays = 'holidays'

        favorites_db.add_favorite(city, country, month, year, webcam, weather, holidays)

        added_favorite_no_nickname = Favorite.get_or_none(city = 'city1')
        
        self.assertIsNotNone(added_favorite_no_nickname)


    def test_add_favorite_no_nickname_and_null_values(self):
        city = 'city1'
        country = 'country1'
        month = 2
        year = 2022
        webcam = None
        weather = None
        holidays = None

        favorites_db.add_favorite(city, country, month, year, webcam, weather, holidays)

        added_favorite_no_nickname_null_values = Favorite.get_or_none(city = 'city1')
        
        self.assertIsNotNone(added_favorite_no_nickname_null_values)


if __name__ == '__main__':
    unittest.main()