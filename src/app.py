from flask import Flask, g, session
from routing.user_routes import user_app
from routing.analytics_routes import analytics_app
from routing.backend_user_routes import backend_user_app
from routing.auth import auth

from routing.database import Database, init_db

app = Flask(__name__)
# TODO: Move secret key to a config file instead of being in the code
app.config['SECRET_KEY'] = "f83c599251aa636b0b0a55aabc55793e"

""" Registering  blueprints for each section of the app. These correspond to the 3
user's we would consider to be sending us requests: ourselves, customers, and people interested
in purchase data"""
blueprints = [
    user_app,
    analytics_app,
    backend_user_app,
    auth
]
[app.register_blueprint(bp) for bp in blueprints]

""" Attempt to initialize the database until it succeeds."""
# TODO: Move Database to separate container and change this section accordingly
while True:
    try:
        init_db()
        break
    except Exception as e:
        pass

d = None
@app.before_first_request
def initialize_db_conn():
    global d
    d = Database(app=app)


""" Testing homepage route to make sure the website loads"""
# TODO: Figure out what homepage is going to actually go to/do
@app.route('/', methods=['GET', 'POST'])
def home():
    return "none"







