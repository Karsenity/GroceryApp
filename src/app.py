from flask import Flask, g, session
from routing.user_routes import user_app
from routing.analytics_routes import analytics_app
from routing.backend_user_routes import backend_user_app


app = Flask(__name__)

blueprints = [
    user_app,
    analytics_app,
    backend_user_app
]

[app.register_blueprint(bp) for bp in blueprints]









