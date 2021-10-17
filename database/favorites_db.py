from peewee import *

db = SqliteDatabase('favorites.db')

class Favorites(Model):

    nickname = CharField() # in case we want to allow the user to give their favorite a nickname
    city = CharField(null=False)
    country = CharField(null=False)
    month = IntegerField(null=False, constraints=[Check('0 < month AND month < 13')])
    year = IntegerField(null=False)
    webcam = CharField()
    weather = CharField()
    holidays = CharField()

    class Meta: 
        database = db

    def __str__(self):
        question_info = f'ID. {self.id} Difficulty: {self.difficulty}, Points: {self.points}, Category: {self.category}'
        question_and_answers = f'Q: {self.question}, A: {self.answercorrect}; {self.answerincorrecta}; {self.answerincorrectb}; {self.answerincorrectc}'
        return f'{question_info}\n{question_and_answers}\n'


class FavoritesError(Exception):
    """Custom exception class."""
    pass


def create_table():
    """Create Favorites table."""
    db.create_tables([Favorites])