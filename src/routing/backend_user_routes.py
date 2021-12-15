from datetime import datetime

from flask import Flask, Blueprint, jsonify, g, session, request
from routing.database import Database

backend_user_app = Blueprint("backend_user_routes", __name__, url_prefix="/backend_user")


@backend_user_app.route('/get_filtered_products/<search_term>')
def get_filtered_products(search_term):
	db = Database.user.get_db().cursor()
	search_term = "%" + search_term + "%"
	db.execute("SELECT * FROM Products WHERE Name LIKE %s;", (search_term,))
	return jsonify(db.fetchall())


@backend_user_app.route('/add_transaction/<price_history_ID>-<count>')
def add_transaction(price_history_ID, count):
	if session.get("Username") is not None:
		entry = {
			"Price_History_ID": int(price_history_ID),
			"Username": session.get("Username"),
			"Time_Added": datetime.now(),
			"Count_of_Item": int(count)
		}
		db = Database.admin.get_db().cursor()
		db.execute("INSERT INTO Transaction (Price_History_ID, Username, Time_Added, Count_of_Item) "
				   "VALUES (%s, %s, %s, %s)",
				   tuple(entry.values()),)
		return jsonify(db.fetchone())
	return "Login not found, Aborting"


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


@backend_user_app.route('/get_user_list')
def get_user_list():
	if session.get("Username") is not None:
		db = Database.user.get_db().cursor()
		db.execute("SELECT * FROM User_Lists WHERE Username=%s", (session.get("Username"),))
		session["user_info"] = db.fetchall()
		return jsonify(session["user_info"])
	return "Login not found, Aborting"


@backend_user_app.route('/add_user_list/<product_id>-<sale_type>-<count>')
def add_user_list(product_id, sale_type, count):
	if session.get("Username") is not None:
		entry = {
			"Username": session.get("Username"),
			"Product_ID": int(product_id),
			"Sale_Type": sale_type,
			"Time_Added": datetime.now(),
			"Count": int(count)
		}
		db = Database.user.get_db().cursor()
		db.execute("INSERT INTO User_Lists VALUES (%s, %s, %s, %s, %s)", tuple(entry.values()))
		return jsonify(db.fetchone())
	return "Login not found, Aborting"


@backend_user_app.route('/remove_user_list/<product_id>-<sale_type>-<count>')
def remove_user_list(product_id, sale_type, count):
	count = int(count)
	if session.get("Username") is not None:
		db = Database.user.get_db().cursor()
		db.execute("SELECT * FROM User_Lists "
				   "WHERE Username=%s AND Product_ID=%s AND Sale_Type=%s",
				   (session.get("Username"), product_id, sale_type))
		entry = db.fetchone()
		new_count = entry["Count"] - count
		if new_count > 0 and count > 0:
			db.execute("UPDATE User_Lists "
					   "SET Count = %s"
					   "WHERE Username=%s AND Product_ID=%s AND Sale_Type=%s",
					   (new_count, session.get("Username"), product_id, sale_type))
		else:
			db.execute("DELETE FROM User_Lists "
					   "WHERE Username=%s AND Product_ID=%s AND Sale_Type=%s",
					   (session.get("Username"), product_id, sale_type))
		return jsonify(entry)
	return "Login not found, Aborting"
