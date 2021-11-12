from flask import Flask, Blueprint

user_app = Blueprint("user_routes", __name__, url_prefix="/user")


@user_app.route('/login')
def login():
    """Sends login request to server..

    :param username: hashed username of the user
        :type username: string
    :param password: hashed password of the user
        :type password: string
    :return: boolean corresponding to whether login was successful
    :rtype: bool
    """
    return None


@user_app.route('/create_user')
def create_user():
    """Sends request to server to create new user..

    :param username: hashed username of the user
        :type username: string
    :param password: hashed password of the user
        :type password: string
    :return: boolean corresponding to whether creation was successful
    :rtype: bool
    """
    return None


@user_app.route('/retrieve_user_list')
def retrieve_user_list():
    """Sends login request to server..

    :param username: hashed username of the user
        :type username: string
    :param password: hashed password of the user
        :type password: string
    :return: boolean corresponding to whether login was successful
    :rtype: bool
    """
    return None


@user_app.route('/user_list_add')
def user_list_add():
    """Sends login request to server..

    :param username: hashed username of the user
        :type username: string
    :param password: hashed password of the user
        :type password: string
    :return: boolean corresponding to whether login was successful
    :rtype: bool
    """
    return None


@user_app.route('/user_list_remove')
def user_list_remove():
    return None


@user_app.route('/get_products')
def get_products():
    return None


@user_app.route('/transactions')
def get_transactions():
    return None

