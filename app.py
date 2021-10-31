from flask import Flask, request, render_template, redirect

from ui_support import ui
from favorites_database import favorites_db

#TODO: change import statements as merges are made

# from holiday_cal import country_api
from scratch_module import country_code_handler as get_countries_from_API

# from holiday_cal import holiday as holiday_api
import scratch_module as holiday_api

# from weather import weather_api
import scratch_module as weather_api

# import windy_api_manager as webcam_api
import scratch_module as webcam_api


app = Flask(__name__)


@app.route('/')
def index():
    # get list of countries to populate options for select element
    country_api_response = get_countries_from_API()
    all_countries = ui.get_list_of_countries(country_api_response)

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
    month, year = ui.get_month_and_year_from_date(date)
    coordinates = weather_api.get_coordinates(city)
    month_name = ui.get_name_of_month_from_number(month)

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

    # create a dictionary to pass to template - to make creation of favorite easier later on
    result = ui.create_result_dictionary(city, country, month, month_name, year, webcam_urls_daylight, holidays_list, weather_data)

    return render_template('result.html', result=result)


@app.route('/favorites')
def get_favorites():
    # get all favorites from the DB
    # in template - user will receive a message stating no favorites, if no results retrieved
    favorites = favorites_db.get_favorites()

    return render_template('favorites.html', favorites=favorites)
    # unit test - put data in db, call route handler, examine response, assert example data on page, assert example data on page, etc


@app.route('/favorite/<id>')
def get_favorite(id):
    # get favorites from the database by id or get None
    favorite = favorites_db.get_favorite_by_id(id)

    if not favorite:
        # show error message on error page if None
        error_message = 'Sorry, could not retrieve favorite.'
        return render_template('error.html', error_message=error_message)

    # create expected dictionary for result.html template from retrieved favorite object
    month_name = ui.get_name_of_month_from_number(favorite.month)
    result = ui.create_result_dictionary(favorite.city, favorite.country, favorite.month, month_name, favorite.year, favorite.webcam, favorite.holidays, favorite.weather)

    return render_template('result.html', result=result)


@app.route('/favorite/add')
def add_favorite(result): 
    # take entries from result dictionary passed from result.html to create and save a favorite object
    favorites_db.add_favorite(result['city'], result['country'], result['month'], result['year'], result['webcams'], result['weather'], result['holidays'])
    
    return redirect('favorites.html')


@app.route('/favorite/delete/<id>')
def delete_favorite(id):
    #TODO: would be nice to ask the user if they are sure they want to delete the favorite...
    was_favorite_deleted = favorites_db.delete_favorite_by_id(id)

    if was_favorite_deleted == False:
        # show error message on error page if favorite not deleted
        error_message = f'Unable to delete favorite. Please check if ID: {id} is a valid favorite.'
        return render_template('error.html', error_message=error_message)
    
    return redirect('favorites.html')
