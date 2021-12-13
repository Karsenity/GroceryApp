from flask import Flask, g, session
from routing.user_routes import user_app
from routing.analytics_routes import analytics_app
from routing.backend_user_routes import backend_user_app
from src.routing.database import Database

app = Flask(__name__)

blueprints = [
    user_app,
    analytics_app,
    backend_user_app
]

[app.register_blueprint(bp) for bp in blueprints]


# d.user.get_db().cursor()
# d.admin.get_db().cursor()
# @app.before_first_request
# def initialize_database():
#     try:
#         # Database connected to Flask
#         d = Database(app)
#     except Exception as e:
#         print(e)
#         initialize_database()


@app.route('/', methods=['GET', 'POST'])
def home():
    return "none"


#app.run()







