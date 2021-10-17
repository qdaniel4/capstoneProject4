from peewee import *

db = SqliteDatabase('favorites.db')

class Favorites(Model):

    city = CharField(null=False)
    country = CharField(null=False)
    month = IntegerField(null=False, constraints=[Check('0 < month AND month < 13')])
    year = IntegerField(null=False)
    webcam = CharField()
    weather = CharField()
    holidays = CharField()
    nickname = CharField() # in case we want to allow the user to give their favorite a nickname

    class Meta: 
        database = db

    def __str__(self):
        return f'{self.city}, {self.country}, in {self.month}/{self.year}: Webcam: {self.webcam}, Weather: {self.weather}, Holidays: {self.holidays}, Nickname: {self.nickname}'


class FavoritesError(Exception):
    """Custom exception class.""" 
    pass


def create_table():
    """Create Favorites table."""
    db.create_tables([Favorites])
