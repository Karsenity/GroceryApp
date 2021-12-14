from flask import Flask, Blueprint
from routing.auth import login_required
from flask import g
from routing.database import Database

user_app = Blueprint("user_routes", __name__, url_prefix="/user")


@user_app.route('/retrieve_user_list')
@login_required
def retrieve_user_list():
    """Retrieve a user's current shopping list..

    :return: list of products
        :rtype: list
    """
    db = Database.user.get_db().cursor()
    products = db.execute("SELECT * FROM User_Lists WHERE Username='%s'" % g.user["Username"])
    return products

@user_app.route('/user_list_add')
@login_required
def user_list_add():
    """Adds a list of products to the user's shopping list using their product_id's..

    :param product_ids: list of ID's corresponding to products added.
        :type: list
    :return: boolean corresponding to whether products were successfully added
        :rtype: bool
    """
    """
    We are given a list of type Product, need to add to user's shopping list
    
    1.) For each product:
        a.) Use the Username hash, product_id, and sale_type to add the object to User_Lists.
            Use cur_time as the time added.
            
    """
    return None


@user_app.route('/user_list_remove/{product_id}')
@login_required
def user_list_remove():
    """Removes a product from the user's shopping list using its product_id..

    :param product_id: ID of product to be removed
        :type: int
    :return: boolean corresponding to whether products were successfully removed
        :rtype: bool
    """
    return None


@user_app.route('/get_products')
@login_required
def get_products():
    """Uses passed keywords args to get all products satisfying conditions..

    :param search_args: dictionary of arguments to filter products based on.
        :type: dict
    :return: list of products satisfying search_args
        :rtype: list[dict]
    """
    return None


@user_app.route('/transactions')
@login_required
def get_transactions():
    """Retrieve all past products that a user has removed from their shopping list..

    :return: list of products
        :rtype: list[dict]
    """
    return None





