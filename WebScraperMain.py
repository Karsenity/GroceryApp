import mysql.connector as mysql
from flask import Flask

from Scrappers.ScrapeManager import ScrapeManager
from Scrappers.Stores.WholeFoods import WholeFoods


# Fake MySQL database

# db = mysql.connect(
#     user="root",
#     passwd="1234"
# )
#
#
# cursor = db.cursor()
# try:
#     cursor.execute("CREATE DATABASE projectDB")
# except mysql.errors.DatabaseError:
#     # Database already exists
#     pass
# cursor.close()
# exit()
# from src.routing.database import Database


# w = WholeFoods()
# keepGoing = True
# while keepGoing:
#     keepGoing = w.step()


# Basic way of doing it that only opens 1 Chrome tab
s = ScrapeManager()
s.addStore('WholeFoods')
keepGoing = True
while keepGoing:
    keepGoing = s.runAll()


# CREATE USER 'newuser'@'localhost' IDENTIFIED BY '1234';
# GRANT ALL PRIVILEGES ON * . * TO 'newuser'@'localhost';
# commit;
# use projectdb;
# create table Products(
#    Product_ID INT NOT NULL AUTO_INCREMENT,
#    Store_ID INT NOT NULL,
#    Name VARCHAR(50) NOT NULL,
#    Price_History INT NOT NULL,
#    Link_To_Item_URL VARCHAR(120),
#    PRIMARY KEY ( Product_ID )
# );

