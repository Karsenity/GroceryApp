import mysql.connector as mysql

from src.routing.database import Database


def connect_admin_level():
    return Database().admin.get_db()


def add_store():
    """
    This Adds a Store to our [Store] Table

    :return: Pass/Failed
        :rtype: Boolean
    """
    return


def add_image():
    """
    Called by backend_calls.py/add_product()
        This adds a set of pictures to our [Images] Table

    :return: Pass/Failed
        :rtype: Boolean
    """
    return

