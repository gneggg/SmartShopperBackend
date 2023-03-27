#!/usr/bin/env python3
import mysql.connector as mysql

MYSQL_USER =  'root' #replace with your user name.
MYSQL_PASS =  'BestBuy1213' #replace with your MySQL server password
MYSQL_DATABASE = 'SmartShopper'#replace with your database name

mydb = mysql.connect(user=MYSQL_USER,
                           passwd=MYSQL_PASS,
                           database=MYSQL_DATABASE, 
                           host='127.0.0.1')


def get_all_users():
    mycursor = mydb.cursor(dictionary=True)

    mycursor.execute("SELECT * FROM UserAccount;") 
    return mycursor.fetchall()

def get_all_userprofiles():
    mycursor = mydb.cursor(dictionary=True)

    mycursor.execute("SELECT * FROM UserProfiles;") 
    return mycursor.fetchall()
   
def verify_pass(passwrd):
    specialchar="$@_!#%&?"
    sum = 0
    if (len(passwrd) >= 8):
        for i in passwrd:
            # counting lowercase alphabets
            if (i.islower()):
                sum+=1           
 
        # counting uppercase alphabets
            if (i.isupper()):
                sum+=1           
 
        # counting digits
            if (i.isdigit()):
                sum+=1        

            if(i in specialchar):
                sum+=1 

    if sum==len(passwrd):     
        #print("Valid Password")
        return True
    else:
        #print("Invalid Password")
        return False
 
    


def create_new_account(new_user):
    mycursor = mydb.cursor()
    name = new_user['username']
    email = new_user['email']
    passwrd = new_user['passwrd']

    mycursor.execute(f"SELECT UserID FROM UserAccount WHERE  username = '{name}' AND email ='{email}' AND passwrd = '{passwrd}';")
    userID = mycursor.fetchone()

    if userID == None and verify_pass(passwrd) is True:
        mycursor.execute(f"INSERT INTO UserAccount (UserName, Email, Passwrd) VALUES ('{name}', '{email}', '{passwrd}');")
        mycursor.execute(f"SELECT UserID FROM UserAccount WHERE  username = '{name}' AND email ='{email}' AND passwrd = '{passwrd}';")
        userID = mycursor.fetchone()     
        res_userID=[]
        res_userID.append(*userID)
 # Update the table UserProfiles
        mycursor.execute(f"INSERT INTO UserProfiles (UserID, ProfileName) VALUES ('{res_userID[0]}', '{name}');")    
        mydb.commit()
    
    else: 
        print("Invalid email or password")
   
def create_new_profile(new_profile):
    mycursor = mydb.cursor()
    user = new_profile['userID']
    name = new_profile['username']
    mycursor.execute(f"INSERT INTO UserProfiles (UserID, ProfileName) VALUES ('{user}', '{name}');")    
    mydb.commit()

def search_groceries(values):
    mycursor=mydb.cursor(dictionary=True)

    item_search = "SELECT * FROM Groceries WHERE ItemName LIKE"
    for word in range(len(values)):
        item_search+=  f" '%{values[word]}%'"
        if word < len(values)-1:
          item_search += " OR"

        else:
            item_search  += ";"

    mycursor.execute(item_search)
    myresult = mycursor.fetchall()

    res=[]
    for row in myresult:
       res.append(row)
    return res


def log_in(user_values):
    mycursor = mydb.cursor()
    email = user_values['email']
    passwrd = user_values['passwrd']
    mycursor.execute(f"SELECT UserID FROM UserAccount WHERE  AND email ='{email}' AND passwrd = '{passwrd}';")
    userID = mycursor.fetchone()

    if userID == None:
        print("No user found, please try create account")
    else: 
        print("Log in sucsessfull")


    
#if __name__ == '__main__':
#    main()


new_user = {'username': 'Matilda' , 'email':'mahu19@bth.se', 'passwrd': 'heja123!'}
#values = ["Mjölk"]
#print(search_groceries(values))
#user = ("namn@mail.com", "BuckBeat12")
print(create_new_account(new_user))
#print(create_new_account(user))
#  print(get_all_users())
#print(get_all_userprofiles())

#passwrd="Heja123!"
#verify_pass(passwrd)

