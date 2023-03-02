import mysql.connector as mysql
import pandas as pd
from os import path
from inspect import currentframe, getfile
from random import randint



MYSQL_USER =  'root' #replace with your user name.
MYSQL_PASS =  'SmartShopper123' #replace with your MySQL server password
MYSQL_DATABASE = 'SmartShopper_databas'#replace with your database name

connection = mysql.connect(user=MYSQL_USER,
                           passwd=MYSQL_PASS,
                           database=MYSQL_DATABASE, 
                           host='35.228.63.5')
cmd_folder = path.realpath(
    path.abspath(path.split(getfile(currentframe()))[0])) + '/'
""" Använder dict värden utanför select i selecten"""
# cnx.execute("SELECT * FROM Product Limimt 20 where type =  %s and subtype = %s and gender = %s", (categories["type"], categories["subtype"]))

def connecters():
    """ funktion som connecta till vår databas"""
    MYSQL_USER =  'root' #replace with your user name.
    MYSQL_PASS =  'SmartShopper123' #replace with your MySQL server password
    MYSQL_DATABASE = 'SmartShopper_databas'#replace with your database name
    connection = mysql.connect(user=MYSQL_USER,
                           passwd=MYSQL_PASS,
                           database=MYSQL_DATABASE, 
                           host='35.228.63.5')
    cnx = connection.cursor(dictionary=True)
    return cnx, connection


cnx,connection = connecters()
lista = []
cnx.execute("SELECT * from user ")
for row in cnx:
    lista.append(row)

print(lista)
