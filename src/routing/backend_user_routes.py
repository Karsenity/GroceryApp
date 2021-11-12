from flask import Flask, Blueprint

backend_user_app = Blueprint("backend_user_routes", __name__, url_prefix="/backend_user")


@backend_user_app.route('/check_login')
def check_login():
    return None


@backend_user_app.route('/add_user')
def add_user():
    return None


@backend_user_app.route('/add_transactions')
def add_transactions():
    return None


@backend_user_app.route('/get_transactions')
def get_transactions():
    return None


@backend_user_app.route('/add_alert')
def login():
    return None


@backend_user_app.route('/get_alerts')
def login():
    return None


@backend_user_app.route('/remove_alerts')
def login():
    return None


@backend_user_app.route('/add_shopping_list')
def login():
    return None


@backend_user_app.route('/get_shopping_list')
def login():
    return None


