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


# Database connected to Flask
d = Database(app)
# d.user.get_db().cursor()
# d.admin.get_db().cursor()


@app.route('/', methods=['GET', 'POST'])
def home():
    return "none"


app.run()







