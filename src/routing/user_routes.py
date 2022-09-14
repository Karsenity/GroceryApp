from flask import Flask, Blueprint, render_template, request, jsonify, session
from routing.auth import login_required
from flask import g

from routing.backend_user_routes import get_user_list
from routing.database import Database

user_app = Blueprint("user_routes", __name__, url_prefix="/user")


@user_app.route('/retrieve_user_list')
@login_required
def retrieve_user_list():
    """Retrieve a user's current shopping list..

    :return: list of products
        :rtype: list
    """
    get_user_list()
    products = session["user_info"]
    return render_template("user/user_list.html", products=products)


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
        a.) Use the Username, product_id, and sale_type to add the object to User_Lists.
            Use cur_time as the time added.
            
    """
    return None


@user_app.route('/get_products', methods=("GET", "POST"))
@login_required
def get_products():
    """Uses passed keywords args to get all products satisfying conditions..

    :return: list of products satisfying search_args
        :rtype: list[dict]
    """
    if request.method == "POST":
        db = Database.user.get_db().cursor()

        search_term = "%" + request.form["search_term"] + "%"
        db.execute("SELECT * FROM Products WHERE Name LIKE %s;", (search_term,))
        return jsonify(db.fetchall())
    return render_template("user/get_products.html")



@user_app.route('/transactions')
@login_required
def get_transactions():
    """Retrieve all past products that a user has removed from their shopping list..

    :return: list of products
        :rtype: list[dict]
    """
    return None





