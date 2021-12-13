import os

import pymysql.cursors
from flaskext.mysql import MySQL
import mysql.connector as mysql


# This class is used for Flask
class Database:
    admin = None
    user = None
    app = None

    def __init__(self, app):
        if self.admin is None:
            self.app = app
            self.admin = self.connect_admin_level()
            self.user = self.connect_user_level()
        return

    def connect_admin_level(self):
        return MySQL(self.app, prefix="Admin", host="localhost", user="root",
                     password="1234", db="projectDB", autocommit=True,
                     cursorclass=pymysql.cursors.DictCursor)

    def connect_user_level(self):
        return MySQL(self.app, prefix="User", host="localhost", user="newuser",
                     password="1234", db="projectDB", autocommit=True,
                     cursorclass=pymysql.cursors.DictCursor)

        # return mysql.connect(
        #     user="root",
        #     passwd="1234",
        #     database='projectDB'
        # )


def testing():
    mysql = MySQL()

    # mysql.init_app(app)
    app = 3
    mysql_1 = MySQL(app, prefix="mysql1", host=os.getenv("“db_host”"), user=os.getenv("“db_username”"),
                    password=os.getenv("“db_pass”"), db=os.getenv("“db_name"), autocommit=True,
                    cursorclass=pymysql.cursors.DictCursor)

    mysql_2 = MySQL(app, prefix="”mysql2”", host="”host2”", user="”UN”", passwd="”&&”", db="”DB”",
                    autocommit=True, cursorclass=pymysql.cursors.DictCursor)


def getAdminDatabase():
    return mysql.connect(
        user="root",
        passwd="1234",
        database='projectDB'
    )


def getConnection(host, user, password, db='maybe', prefix='varName'):
    return
