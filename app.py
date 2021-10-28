from flask import Flask, request, render_template, redirect

from favorites_database import favorites_db

#TODO: change import statements as merges are made

# from holiday_cal import country_api
from scratch_module import country_api

# from holiday_cal import holiday as holiday_api
import scratch_module as holiday_api

# from weather import weather_api
import scratch_module as weather_api

# import windy_api_manager as webcam_api
import scratch_module as webcam_api


app = Flask(__name__)


def get_month_and_year_from_date(date):
    """Takes a date in the HTML datepicker format as param.
    Returns just the month and year from that date as tuple."""
    # TODO: Refactor this out of app.py + modify test file ?
    date_list = date.split('/')
    month = date_list[0]
    year = date_list[2]

    return month, year


def get_coordinates_string(city):
    """Gets latitude and longitude for param city from weather_api.
    Returns it as a formatted string for use in future API calls."""
    lat, lon = weather_api.get_coordinates(city)
    coordinates_string = f'{lat},{lon}'
    return coordinates_string


def get_list_of_countries():
    """Gets list of countries and country codes from the country_api in holiday_cal
    Pulls just the country names out, puts them in a list, then returns that list."""
    country_api_response = country_api.country_code_handler()
    country_name_list = []
    for country_name_and_code in country_api_response:
        country_name_list.append(country_name_and_code['country_name'])
    return country_name_list


@app.route('/')
def index():

    # get list of countries to populate options for select element
    all_countries = get_list_of_countries()

    # get list of web api categories to populate options for select element
    webcam_api_categories = webcam_api.show_categories()

    return render_template('index.html', all_countries=all_countries, webcam_api_categories=webcam_api_categories)


@app.route('/result')
def get_result():
    # get all user input required for API calls
    city = request.args.get('city')
    country = request.args.get('country')
    date = request.args.get('date')
    category = request.args.get('category')

    # convert some user input into useful API parameters
    month, year = get_month_and_year_from_date(date)
    coordinates = get_coordinates_string(city)

    # get a list of holidays from holiday API
    # each holiday is a dictionary that contains name, description and date of holiday
    holidays_list = holiday_api.get_holiday_data(country, year, month)

    # get a dictionary of climate data for the specified month
    # contains temp high, temp low, rainfall in inches, sunshine hours
    weather_data = weather_api.get_climate(coordinates, month)

    # Get two lists of webcam urls based on the user's selected category
    # and the coordinates of the city from troposphere
    # we are just using webcam_urls_daylight for now, but could use current in extended functionality
    webcam_urls_daylight, webcam_urls_current = webcam_api.get_image_list(coordinates, category)

    return render_template('result.html', city=city, country=country, month=month, year=year, holidays=holidays_list, weather=weather_data, webcam_urls=webcam_urls_daylight)


@app.route('/favorites')
def get_favorites():
    favorites = favorites_db.get_favorites()

    return render_template('favorites.html', favorites=favorites)
    # unit test - put data in db, call route handler, examine response, assert example data on page, assert example data on page, etc


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


@app.route('/favorite/add/<id>')
def add_favorite(favorite):
    was_favorite_deleted = favorites_db.delete_favorite_by_id(id)
    added = f'Unable to delete favorite. Please check if ID: {id} is a valid favorite.'
    if was_favorite_deleted == True:
        added = 'Favorite was deleted.'
    
    return render_template('added.html', added=added)


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