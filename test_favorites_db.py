
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
    Create expected Question table & Result table
    """

    def setUp(self):
        '''Clear and remake Question and Result tables for test database.'''
        self.db = SqliteDatabase(test_db_path)
        self.db.drop_tables([Favorites])
        self.db.create_tables([Favorites])


if __name__ == '__main__':
    unittest.main()