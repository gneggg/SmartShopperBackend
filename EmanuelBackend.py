import mysql.connector as mysql
import pandas as pd
from os import path
from inspect import currentframe, getfile
from random import randint
import json



MYSQL_USER =  'root' #replace with your user name.
MYSQL_PASS =  'Godis9812' #replace with your MySQL server password
MYSQL_DATABASE = 'dv1587'#replace with your database name

connection = mysql.connect(user=MYSQL_USER,
                           passwd=MYSQL_PASS,
                           database=MYSQL_DATABASE, 
                           host='127.0.0.1')
cmd_folder = path.realpath(
    path.abspath(path.split(getfile(currentframe()))[0])) + '/'
""" Använder dict värden utanför select i selecten"""
# cnx.execute("SELECT * FROM Product Limimt 20 where type =  %s and subtype = %s and gender = %s", (categories["type"], categories["subtype"]))

def connecters():
    """ funktion som connecta till vår databas"""
    MYSQL_USER =  'root' #replace with your user name.
    MYSQL_PASS =  'Godis9812' #replace with your MySQL server password
    MYSQL_DATABASE = 'dv1587'#replace with your database name
    connection = mysql.connect(user=MYSQL_USER,
                           passwd=MYSQL_PASS,
                           database=MYSQL_DATABASE, 
                           host='127.0.0.1')
    cnx = connection.cursor(dictionary=True)
    return cnx, connection


cnx,connection = connecters()


###### Hjälp funktioner #########################################################################################################33
def get_item_id(json):
    """ Tar in en lista och hämta informationen om produkten och returnera en lisat med produkten"""
    cnx,connection = connecters()
    grocery = json["grocery"]
    id_lista=[]
    cnx.execute("SELECT ItemID FROM Groceries WHERE ItemName in (%s)",(grocery,))
    for row in cnx:
        id_lista.append(row)
    connection.close()
    for i in id_lista:
        return i["ItemID"]

def get_user_id(user_id):
    cnx,connection = connecters()
    id_lista = []
    cnx.execute("SELECT profileid as id, profilename FROM userprofiles WHERE profileid in (%s)",(user_id,))
    for row in cnx:
        id_lista.append(row)
    for i in id_lista:
        return i["Profileid"]


def good_exists(json):
    grocerie = json["grocerie"] 
    cnx,connection = connecters()
    cnx.execute("SELECT itemname FROM Groceries WHERE itemname  in (%s)",(grocerie,))
    for row in cnx:
        if row == None:
            return False
        else:
            return True 
    connection.close()

def get_date(item_id):
    id_lista = []
    cnx.execute("SELECT date FROM storagebank WHERE itemid  in (%s)",(item_id,))
    for row in cnx:
        id_lista.append(row)
    for i in id_lista:
        return i["last_shopped"]

def clear_shoppinglist():
    cnx.execute("Select itemid from shoppinglistrow")
    lista = []
    for id in cnx:
        lista.append(id["itemid"])
    for id in lista:
        cnx.execute("DELETE FROM ShoppingListRow where itemid = (%s)",(id,))
        connection.commit()

def get_category(item_id):
    lista = []
    cnx.execute("SELECT category FROM Groceries WHERE itemname  in (%s)",(item_id,))
    for row in cnx:
        lista.append(row)
    for i in lista:
        return i["category"] 
    
def readd_favorites(json):
    profileid = json["profileid"]
    cnx.execute("Select itemid from favorites")
    lista = []
    for id in cnx:
        lista.append(id["itemid"])
    for id in lista:
        cnx.execute("Insert into storagerow( ItemID, profileID,duration) Values(%s,%s,0)",(id,profileid))
        cnx.commit()
     

###### Storage funktioner ##################################################################################################
def add_into_storage():
    cnx,connection = connecters()
    cnx.execute("Select shoppinglistrow.itemid,userid from Favorites inner join shoppinglistrow where Favorites.itemid = shoppinglistrow.itemid")
    lista = []
    for row in cnx:
        lista.append(row)
    for row in lista:
        cnx.execute("Insert into storagerow( ItemID, profileID,last_shopped) Values(%s,%s,curdate())",(row["itemid"],row["userid"]))
        connection.commit()
    
def show_storage():
    cnx,connection = connecters()
    x = cnx.execute("Select groceries.itemname, groceries.category, storage.lastshopped from groceries inner join storage where groceries.itemid = storage.itemid order by itemname")
    whole_list = cnx.fetchall()
    return json(whole_list)

def remove_from_storage(id):
    cnx,connection = connecters()
    cnx.execute("DELETE FROM storage where itemid = (%s)",(id,))
    



#### listbank funktioner #########################################################################################################
def add_into_listbank(json):
    cnx.execute("Insert into listbank(userid) Values(%s)",(json["profileid"],))





#### Shoppginlistan funktioner #####################################################################################################
def add_to_shoppinglist(json):
    grocerie = json["itemname"]
    category = json["category"]
    user_id = json["user_id"]
    cnx,connection = connecters()
    if good_exists(grocerie) == None:
        cnx.execute( "Insert into Groceries (ItemName,Category) VALUES (%s,%s)",(grocerie,category))
        connection.commit()
    food_id = get_item_id(grocerie)
    cnx.execute( "Insert into Shoppinglistrow (UserID,ItemID,duration) VALUES (%s,%s,0)",(user_id,food_id))
    connection.commit()
    return 

def end_shopping(json):
    cnx,connection = connecters()
    add_into_storage()
    add_into_listbank(json)
    clear_shoppinglist()
    readd_favorites(json)
      
def remove_from_shoppinglist(id):
    cnx,connection = connecters()
    cnx.execute("DELETE FROM ShoppingListRow where itemid = (%s)",(id,))

def show_shoppinglist():
    cnx,connection = connecters()
    x = cnx.execute("Select groceries.itemname, groceries.category,shoppinglistrow.duration  from groceries inner join shoppinglistrow where groceries.itemid = shoppinglist.itemid order by category")
    whole_list = cnx.fetchall()
    return json(whole_list)

def updates():
    cnx,connection = connecters()
    cnx.execute("Update shoppinglistrow inner join storagerow set shoppinglistrow.duration = datediff(curdate(),last_shopped) where shoppinglistrow.itemid = storagerow.itemid")
    connection.commit()

    
    

##### Favorite funktioner#####################################################################################################################
def remove_from_favorites(id):
    cnx,connection = connecters()
    cnx.execute("DELETE FROM favorites where (%s) = item_id",(id,))
    cnx.execute("DELETE FROM Shoppinglistrow where (%s) = item_id",(id,))
    return
    
def show_favorites():
    cnx,connection = connecters()
    x = cnx.execute("Select groceries.itemname, groceries.category from groceries inner join favorites where groceries.itemid = favorites.itemid order by category")
    whole_list = cnx.fetchall()
    return json(whole_list)
    
def add_favorites(json):
    grocerie = json["itemname"]
    category = json["category"]
    user_id = json["user_id"]
    cnx,connection = connecters()
    if good_exists(grocerie) == None:
        cnx.execute( "Insert into Groceries (ItemName,Category) VALUES (%s,%s)",(grocerie,category))
        connection.commit()
    food_id = get_item_id(grocerie)
    cnx.execute( "Insert into Favorites (UserID,ItemID) VALUES (%s,%s)",(user_id,food_id))
    cnx.execute( "Insert into Shoppinglistrow (profileid,ItemID,duration) VALUES (%s,%s,0)",(user_id,food_id))
    connection.commit()
    return     
    


#### Recipe funktioner#############################################################################################################################
def add_recipe(json):
    name = json["recipename"]
    url = json["url"]
    return



    
# show_shoppinglist()
# print(get_item_id([1]))
# print(add_favorites("Saffran","bakelse",2))
# print(get_item_id("Mjölk"))
# print(good_exists("saffran"))
# item_ids = list(map(int, Groceries['items'].strip('[]').split(',')))
# print(item_ids)
