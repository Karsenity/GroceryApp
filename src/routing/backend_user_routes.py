from flask import Flask, Blueprint

backend_user_app = Blueprint("backend_user_routes", __name__, url_prefix="/backend_user")


@backend_user_app.route('/check_login')
def check_login():
    """
    Checks if a Username and Password is correct

    :param Username: Optional "kind" of ingredients.
    :type Username: str
    :param Password: Optional "kind" of ingredients.
    :type Password: str

    :return: CSV[ProductID, WasOnSaleBoolean, TimePurchased, TimeAddedToList, CountOfProduct]
    :rtype: list[str]
    """
    return None


@backend_user_app.route('/add_user')
def add_user():
    """
    Adds a User to [User] Table

    :param Username_Hash: Optional "kind" of ingredients.
    :type Username_Hash: str
    :param Password_Hash: Optional "kind" of ingredients.
    :type Password_Hash: str

    :return: Boolean for Succeeded or Failed
    :rtype: Boolean
    """
    return None


@backend_user_app.route('/add_transactions')
def add_transactions():
    """
    Add a Transaction Entry to [Transactions] Table

    :param Product_ID: Product Key
    :type Product_ID: int
    :param Price_History_ID: Price History Key
    :type Price_History_ID: int
    :param Username_Hash: Hashed version of a Username
    :type Username_Hash: str
    :param Time_Added: Datetime for time this item was added
    :type Time_Added: str

    :return: Boolean for Succeeded or Failed
    :rtype: Boolean
    """
    return None


@backend_user_app.route('/add_alert')
def add_alert():
    """
    Adds a Product_ID to [User_Alert_List] table

    :param Username_Hash: Optional "kind" of ingredients.
    :type Username_Hash: str
    :param Password: Optional "kind" of ingredients.
    :type Password: str

    :return: Boolean for Succeeded or Failed
    :rtype: Boolean
    """
    return None


@backend_user_app.route('/get_alerts')
def get_alerts():
    return None


@backend_user_app.route('/remove_alerts')
def remove_alerts():
    return None


@backend_user_app.route('/add_shopping_list')
def add_shopping_list():
    return None


@backend_user_app.route('/get_shopping_list')
def get_shopping_list():
    return None


