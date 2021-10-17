
import unittest 
from unittest import TestCase
from peewee import *

import db_config
test_db_path = 'test_favorites.db'
db_config.database_path = test_db_path 

import favorites_db
from favorites_db import Favorites

class TestQuiz(TestCase):

    test_db_url = 'test_quiz.db'

    """
    Before running these test, test_favorites.db
    Create expected Favorites table
    """

    def setUp(self):
        '''Clear and remake favorites table for test database.'''
        self.db = SqliteDatabase(test_db_path)
        self.db.drop_tables([Favorites])
        self.db.create_tables([Favorites])

    
    def test_get_list_of_favorites_from_db(self):
        favorite_one = Favorites(city="City1", country="Country1", month=1, year=2020, webcam="http://url.com/", weather="weather", holidays="holiday1, holiday2", nickname="nickname")
        favorite_two = Favorites(city="City2", country="Country2", month=7, year=2020, webcam="http://url3.com/", weather="weather", holidays="holiday1", nickname="nickname")
        favorite_one.save()
        favorite_two.save()

        expected = []
        expected.append('<Favorites: ID 1: City1, Country1, in 1/2020: Webcam: http://url.com/, Weather: weather, Holidays: holiday1, holiday2, Nickname: nickname>')
        expected.append('<Favorites: ID 2: City2, Country2, in 7/2020: Webcam: http://url3.com/, Weather: weather, Holidays: holiday1, Nickname: nickname>')

        result = favorites_db.get_favorites()

        self.assertNotEqual(result, expected)


    def test_get_empty_list_from_db_when_no_records_in_db(self):
        result = favorites_db.get_favorites()
        
        expected = []

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()