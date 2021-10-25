

"""this is an example, we can use this to add images and videos to our web app"""
from flask import Flask, render_template
import windModule #example of windy_module file that is currently in github



app = Flask(__name__)

coordinates1 = '38.732534,0.217634'
radius1 = '100'
category1 = 'beach'
order1 = 'distance'
limit1 = '5'
nearby, category, orderby, limit = windModule.format_params(coordinates1, radius1, category1, order1, limit1)
daylight_links, current_links = windModule.get_image_list(nearby, category, orderby, limit)


# defining home page
@app.route('/')
def homepage():
    # returning image_add.html and list
    # and length of list to html page
    return render_template("image_add.html", len=len(daylight_links), daylight_links=daylight_links)


    app.run(use_reloader=True, debug=True)