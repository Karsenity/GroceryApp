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
        :type username: str
    :param password: hashed password of the user
        :type password: str
    :return: boolean corresponding to whether creation was successful
        :rtype: bool
    """
    return None


@user_app.route('/retrieve_user_list')
def retrieve_user_list():
    """Retrieve a user's current shopping list..

    :return: list of products
        :rtype: list
    """
    return None


@user_app.route('/user_list_add')
def user_list_add():
    """Adds a list of products to the user's shopping list using their product_id's..

    :param product_ids: list of ID's corresponding to products added.
        :type: list
    :return: boolean corresponding to whether products were successfully added
        :rtype: bool
    """
    return None


@user_app.route('/user_list_remove')
def user_list_remove():
    """Removes a product from the user's shopping list using its product_id..

    :param product_id: ID of product to be removed
        :type: int
    :return: boolean corresponding to whether products were successfully removed
        :rtype: bool
    """
    return None


@user_app.route('/get_products')
def get_products():
    """Uses passed keywords args to get all products satisfying conditions..

    :param search_args: dictionary of arguments to filter products based on.
        :type: dict
    :return: list of products satisfying search_args
        :rtype: list[dict]
    """
    return None


@user_app.route('/transactions')
def get_transactions():
    """Retrieve all past products that a user has removed from their shopping list..

    :return: list of products
        :rtype: list[dict]
    """
    return None

