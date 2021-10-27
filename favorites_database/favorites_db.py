from peewee import *

db = SqliteDatabase('favorites.db')

class Favorite(Model):

    city = CharField(null=False)
    country = CharField(null=False)
    month = IntegerField(null=False, constraints=[Check('1 <= month AND month <= 12')])
    year = IntegerField(null=False)
    webcam = CharField(null=True) 
    weather = CharField(null=True) 
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
    db.create_tables([Favorite])


def get_favorites():
    """Select all favorites from the favorites table.
    Return a list of favorites, or an empty list."""
    # TODO: handle an empty list elsewhere in the program
    # since we don't want there to be an error if the user has simply not added anything to faves yet.
    # want html to instead display something like 'nothing in favorites list, try adding something to favorites'
    favorites = Favorite.select()
    favorites_list = list(favorites)

    return favorites_list


def get_favorite_by_id(favorite_id):
    """Gets a favorite by its id, or gets None.
    Raises an error if None.
    Returns favorite if not None."""
    favorite = Favorite.get_or_none(id=favorite_id)

    if not favorite:
        raise FavoritesError(f'Error: No favorite with id {favorite_id} found.')

    return favorite


def add_favorite(city, country, month, year, webcam, weather, holidays, nickname = None):
    """Expects parameters to successfully create a Favorites object
    Creates & saves this object to database.
    Default value of None for nickname, to make nickname optional parameter."""
    favorite = Favorite(city=city, country=country, month=month, year=year, webcam=webcam, weather=weather, holidays=holidays, nickname=nickname)
    favorite.save()


def delete_favorite_by_id(favorite_id):
    """Find favorite by ID, then delete that favorite.
    Return True is favorite was deleted.
    Return False if favorite was not deleted.""" 
    rows_mod = Favorite.delete().where(Favorite.id == favorite_id).execute()

    if rows_mod == 0:
        return False
    else:
        return True


