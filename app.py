from flask import Flask, request, render_template, redirect


# TODO: change to import the actual modules needed
# scratch_module is an empty file
# am using mocking for unit tests for the functions that need to be imported
# but I didn't know what to do about the invalid import statements
# & did not want to use placeholder functions in app.py because I didn't think I'd remember to update them all later...
import scratch_module as favorites_db
import scratch_module as holiday_api
import scratch_module as webcam_api
import scratch_module as weather_api

app = Flask(__name__)

def get_month_and_year_from_date(date):
    """Takes a date in the HTML datepicker format as param.
    Returns just the month and year from that date as tuple."""
    # TODO: Refactor this out of app.py + modify test file ?
    date_list = date.split('/')
    month = date_list[0]
    year = date_list[2]

    return month, year

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result')
def get_result():
    city = request.args.get('city')
    country = request.args.get('country')
    date = request.args.get('date')

    month, year = get_month_and_year_from_date(date)

    webcam_urls = webcam_api.get_webcam_urls(city, country)
    weather = weather_api.get_weather(city, country, month, year)


    webcam_urls = ['url1', 'url2']

    holidays = [{'name': 'holday1', 'description': 'this is a description','date': 'December 22nd'}, 
    {'name': 'holday2', 'description': 'this is another description','date': 'March 5th'}]

 
    # TODO: webcam_url = webcam_api.get_webcam(city, country, date)
    # or similar based on what the API modules end up looking like
    # will need one for each API

    # TODO: function that changes the date into something useful for APIs
    # this might be handled on an individual basis within the APIs
    # or could be in a separate module, or function within this module...

    return render_template('result.html', city=city, country=country, month=month, year=year, webcam_urls=webcam_urls, holidays=holidays)


@app.route('/favorites')
def get_favorites():
    favorites = favorites_db.get_favorites()

    return render_template('favorites.html', favorites=favorites)


@app.route('/favorite/<id>')
def get_favorite(id):
    favorite = favorites_db.get_favorite_by_id(id)
    city = favorite.city
    country = favorite.country
    month = favorite.month
    year = favorite.year

    webcam_urls = favorite.webcam
    weather = favorite.weather
    holidays = favorite.holidays

    return render_template('result.html', city=city, country=country, month=month, year=year, webcam_urls=webcam_urls, weather=weather, holidays=holidays)


@app.route('/favorite/delete/<id>')
def delete_favorite(id):
    #TODO: would be nice to ask the user if they are sure they want to delete the favorite...
    was_favorite_deleted = favorites_db.delete_favorite_by_id(id)
    deleted_confirmation = f'Unable to delete favorite. Please check if ID: {id} is a valid favorite.'
    if was_favorite_deleted == True:
        deleted_confirmation = 'Favorite was deleted.'
    
    return render_template('deleted.html', deleted_confirmation=deleted_confirmation)





# so far what we get from index is:
# result?city=user_input&country=user_input&date=2021-12-23