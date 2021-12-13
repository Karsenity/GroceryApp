import mysql.connector as mysql
from routing.database import Database


def connect_admin_level():
    return Database().admin.get_db()


# Date = YYYY-MM-DD
def add_products(products):
    """
    This adds a Product to our [Products] Table

    :return: Pass/Failed
        :rtype: Boolean
    """
    db = connect_admin_level()
    c = db.cursor()

    for product in products:
        #do some sql here
        pass

    #     d = getAdminDatabase()
    #     lines = f.readlines()
    #     for l in lines:
    #         storeID = 1
    #
    #         sqlCommand = "INSERT INTO Products (Store_ID, Name, Price_History, Link_To_Item_URL) VALUES " \
    #                      "()'
    #         d.cursor().execute()

    return


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

