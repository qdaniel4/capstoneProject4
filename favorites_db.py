from peewee import *

db = SqliteDatabase('favorites.db')

class Favorites(Model):

    city = CharField(null=False)
    country = CharField(null=False)
    month = IntegerField(null=False, constraints=[Check('0 < month AND month < 13')])
    year = IntegerField(null=False)
    webcam = CharField(null=True) # for now I allow null values - in case we got nothing from one of the APIs, but user still wants to save favorite with remaining info
    weather = CharField(null=True) # however we could change this to a string that says 'no data found' instead if wanted?
    holidays = CharField(null=True)
    nickname = CharField(null=True) # in case we want to allow the user to give their favorite a nickname

    class Meta: 
        database = db

    def __str__(self):
        return f'ID {self.id}: {self.city}, {self.country}, in {self.month}/{self.year}: Webcam: {self.webcam}, Weather: {self.weather}, Holidays: {self.holidays}, Nickname: {self.nickname}'


class FavoritesError(Exception):
    """Custom exception class.""" 
    pass


def create_table():
    """Create Favorites table."""
    db.create_tables([Favorites])


def get_favorites():
    """Select all favorites from the favorites table.
    Return a list of favorites, or an empty list."""
    # TODO: handle an empty list elsewhere in the program
    # since we don't want there to be an error if the user has simply not added anything to faves yet.
    # want html to instead display something like 'nothing in favorites list, try adding something to favorites'
    favorites = Favorites.select()
    favorites_list = []
    for favorite in favorites:
        favorites_list.append(favorite)

    return favorites_list


def add_favorite(city, country, month, year, webcam, weather, holidays, nickname = None):
    """Expects parameters to successfully create a Favorites object
    Creates & saves this object to database.
    Default value of None for nickname, to make nickname optional parameter."""
    favorite = Favorites(city=city, country=country, month=month, year=year, webcam=webcam, weather=weather, holidays=holidays, nickname=nickname)
    favorite.save()


def delete_favorite(favorite):
    """Find favorite by ID, then delete that favorite.
    Return True is favorite was deleted.
    Return False if favorite was not deleted."""
    if not favorite.id:
        raise FavoritesError('Favorite does not have ID.')

    id = favorite.id
    rows_mod = Favorites.delete().where(Favorites.id == id).execute()

    if rows_mod == 0:
        # TODO: in ui of program, tailor message based on return value
        # since we would like to notify the user that their deletion request was completed
        return False
    else:
        return True


