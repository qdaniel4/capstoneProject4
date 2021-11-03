from flask import Flask, request, render_template, redirect

from ui_support import ui_support
from favorites_database import favorites_db

from holiday_cal import holiday_api
from weather import weather_api
from windy_module import windy_api_manager as webcam_api

app = Flask(__name__)

favorites_db.create_table()

@app.route('/')
def index():
    error_list = []
    # get list of countries to populate options for select element
    country_api_response = holiday_api.list_of_countries()
    all_countries, country_api_error = ui_support.get_list_of_countries(country_api_response)

    # get list of web api categories to populate options for select element
    webcam_api_response = webcam_api.show_categories()
    webcam_api_categories, webcam_api_error = ui_support.get_list_of_webcam_categories(webcam_api_response)

    # add any errors received during program to error_list
    ui_support.add_error_to_error_list(country_api_error, error_list)
    ui_support.add_error_to_error_list(webcam_api_error, error_list)
    if len(error_list):
        return render_template('error.html', error_list=error_list)

    return render_template('index.html', all_countries=all_countries, webcam_api_categories=webcam_api_categories)


@app.route('/result')
def get_result():
    error_list = []
    # get all user input required for API calls
    city = request.args.get('city')
    country = request.args.get('country')
    date = request.args.get('date')
    category = request.args.get('category')

    # get useful API parameters or get error messages
    month, year, month_year_from_date_error = ui_support.get_month_and_year_from_date(date)
    month_name, month_name_error = ui_support.get_name_of_month_from_number(month)
    coordinates_from_API = weather_api.get_coordinates(city, country)
    coordinates, no_coordinates_error = ui_support.check_if_coordinates(coordinates_from_API)

    # check for errors and display them on error page if present
    ui_support.add_error_to_error_list(month_year_from_date_error, error_list)
    ui_support.add_error_to_error_list(month_name_error, error_list)    
    ui_support.add_error_to_error_list(no_coordinates_error, error_list)
    if len(error_list):
        return render_template('error.html', error_list=error_list)

    # get a list of holidays from holiday API
    # each holiday is a dictionary that contains name, description and date of holiday
    holidays_list = holiday_api.get_holiday(country, year, month)

    # get a dictionary of climate data for the specified month
    # contains temp high, temp low, rainfall in inches, sunshine hours
    weather_data = weather_api.get_climate(coordinates, month)

    # Get two lists of webcam urls based on the user's selected category
    # and the coordinates of the city from troposphere
    # we are just using webcam_urls_daylight for now, but could use current in extended functionality
    webcam_urls = webcam_api.get_video_link(coordinates, category)

    # create a dictionary to pass to template - to make creation of favorite easier later on
    result = ui_support.create_result_dictionary(city, country, month, month_name, year, webcam_urls, holidays_list, weather_data)

    return render_template('result.html', result=result)


@app.route('/favorites')
def get_favorites():
    # get all favorites from the DB
    # in template - user will receive a message stating no favorites, if no results retrieved
    favorites = favorites_db.get_all_favorites()

    return render_template('favorites.html', favorites=favorites)
    # unit test - put data in db, call route handler, examine response, assert example data on page, assert example data on page, etc


@app.route('/favorite/<int:id>')
def get_favorite(id):
    error_list = []
    # get favorites from the database by id or get None
    favorite = favorites_db.get_favorite_by_id(id)

    if not favorite:
        # show error message on error page if None and do not continue function
        error_message = ['Sorry, could not retrieve favorite.']
        return render_template('error.html', error_list=error_message)

    # create expected dictionary for result.html template from retrieved favorite object
    month_name, month_error = ui_support.get_name_of_month_from_number(favorite.month)

    # turn strings from the database back into useful python objects
    webcams = ui_support.create_webcams_list_from_database_favorite(favorite.webcam)
    holidays = ui_support.create_holidays_list_from_database_favorite(favorite.holidays)
    weather = ui_support.create_weather_dict_from_database_favorite(favorite.weather)

    # create expected result dictionary
    result = ui_support.create_result_dictionary(favorite.city, favorite.country, favorite.month, month_name, favorite.year, webcams, holidays, weather)
    
    if len(error_list):
        # for errors that may occur after attempt to retrieve favorite
        return render_template('error.html', error_list=error_list)

    return render_template('result.html', result=result)


@app.route('/favorite/add', methods = ['POST'])
def add_favorite(): 
    # take entries from result dictionary passed from result.html to create and save a favorite object
    result_string = request.form.get('result') # the response is a string
    result = result_string.split('\\') # turn into list
    favorites_db.add_favorite(result[0], result[1], result[2], result[3], result[4], result[5], result[6])
    
    return redirect('../favorites')


@app.route('/favorite/delete/<int:id>', methods = ['GET', 'DELETE'])
def delete_favorite(id):
    error_list = []

    #TODO: would be nice to ask the user if they are sure they want to delete the favorite...
    was_favorite_deleted = favorites_db.delete_favorite_by_id(id)

    if was_favorite_deleted == False:
        # show error message on error page if favorite not deleted
        error_message = f'Favorite with ID: {id} not found in database.'
        ui_support.add_error_to_error_list(error_message, error_list)

    if len(error_list):
        return render_template('error.html', error_list=error_list), 200
        # not sure if it matters or not but had to manually ask it to return 200 status code OK
    
    # It was not automatically redirecting, which I didn't like...
    # so am just getting all favorites again and rendering favorites.html
    # TODO: could show a 'favorite was deleted' message
    favorites = favorites_db.get_all_favorites()
    return render_template('favorites.html', favorites=favorites)

