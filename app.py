from flask import Flask, request, render_template, redirect

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')


# so far what we get from index is:
# result?city=user_input&country=user_input&date=2021-12-23