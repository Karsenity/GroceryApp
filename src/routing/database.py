import pymysql.cursors
from flaskext.mysql import MySQL
import mysql.connector as mysql


# This class is used for Flask
class Database:
    admin = None
    user = None
    app = None

    def __init__(self, app=None):
        if Database.admin is None:
            Database.app = app
            Database.admin = self.connect_admin_level()
            Database.user = self.connect_user_level()
        return

    def connect_admin_level(self):
        return MySQL(Database.app, host="%", user="root",
                     password="password", db="grocery_app_db", autocommit=True,
                     cursorclass=pymysql.cursors.DictCursor)

    def connect_user_level(self):
        return MySQL(Database.app, prefix="User", host="localhost", user="customer",
                     password="1234", db="grocery_app_db", autocommit=True,
                     cursorclass=pymysql.cursors.DictCursor)

        # return mysql.connect(
        #     user="root",
        #     passwd="1234",
        #     database='projectDB'
        # )


def init_db():
    conn = mysql.connect(user="root", password="password")
    cur = conn.cursor()
    with open("database_init.txt") as sql_file:
        sql_as_string = sql_file.read()
        cur.execute(sql_as_string)
    conn.close()


def getAdminDatabase():
    return mysql.connect(
        user="root",
        password="password",
        database='grocery_app_db'
    )


def getConnection(host, user, password, db='maybe', prefix='varName'):
    return
