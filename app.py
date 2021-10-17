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

    # TODO: webcam_url = webcam_api.get_webcam(city, country, date)
    # or similar based on what the API modules end up looking like
    # will need one for each API

    # TODO: function that changes the date into something useful for APIs
    # this might be handled on an individual basis within the APIs
    # or could be in a separate module, or function within this module...

    return render_template('result.html', city=city, country=country, date=date)


# so far what we get from index is:
# result?city=user_input&country=user_input&date=2021-12-23