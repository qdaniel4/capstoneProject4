from flask import Flask, request, render_template, redirect

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/result')
def get_result():
    city = request.args.get('city')
    country = request.args.get('country')
    date = request.args.get('date')

    month = 'sample month'
    year = 'sample year'

    webcam_urls = ['url1', 'url2']

    holidays = [{'name': 'holday1', 'description': 'this is a description','date': 'December 22nd'}, 
    {'name': 'holday2', 'description': 'this is another description','date': 'March 5th'}]


    # TODO: webcam_url = webcam_api.get_webcam(city, country, date)
    # or similar based on what the API modules end up looking like
    # will need one for each API

    # TODO: function that changes the date into something useful for APIs
    # this might be handled on an individual basis within the APIs
    # or could be in a separate module, or function within this module...

    return render_template('result.html', city=city, country=country, date=date, month=month, year=year, webcam_urls=webcam_urls, holidays=holidays)


@app.route('/favorites')
def get_favorites():

    return render_template('favorites.html')


# so far what we get from index is:
# result?city=user_input&country=user_input&date=2021-12-23