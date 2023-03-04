CREATE DATABASE SmartShopper;
USE SmartShopper;
SET SQL_SAFE_UPDATES = 0;
DROP DATABASE SmartShopper;

SELECT * FROM UserAccount; 
DROP TABLE UserAccount; 
CREATE TABLE UserAccount (
	UserID INT NOT NULL AUTO_INCREMENT,
    UserName VARCHAR(100),
    Email VARCHAR(300),
    Passwrd VARCHAR(100),
    PRIMARY KEY (UserID)
    );
    
INSERT INTO UserAccount (UserName, Email, Passwrd) 
VALUES ('Matilda','Matilda@hoglund.se','Lösenord'); 
###########################################################

SELECT * FROM UserProfiles; 
DROP TABLE UserProfiles; 
CREATE TABLE UserProfiles (
	ProfileID INT NOT NULL AUTO_INCREMENT,
    UserID INT,
    ProfileName VARCHAR (100),
    PRIMARY KEY (ProfileID),
    FOREIGN KEY(UserId) REFERENCES User(UserID)
    );

INSERT INTO UserProfiles (UserID, ProfileName) 
VALUES (0,'Matilda'); 
##############################################################

SELECT * FROM Groceries; 
DROP TABLE Groceries;
CREATE TABLE Groceries (
	ItemID  INT NOT NULL AUTO_INCREMENT, 
    ItemName VARCHAR(100),
	Category VARCHAR(200),
    PRIMARY KEY(ItemID)
    );

INSERT INTO Groceries (ItemName, Category)
VALUES ('Mjölk','Mejeri');
##############################################################

DROP TABLE Favorites;
SELECT * FROM Favorites;
CREATE TABLE Favorites (
UserID INT,
ItemID INT, 
CONSTRAINT PK_Favorites PRIMARY KEY (UserID,ItemID),
FOREIGN KEY(UserID) REFERENCES UserAccount(UserID),
FOREIGN KEY(ItemID) REFERENCES Groceries(ItemID)
);

INSERT INTO Favorites (UserID, ItemID)
VALUES (0,0); 
##############################################################
CREATE TABLE ShoppingListBank(
ListID INT AUTO_INCREMENT, 
UserID INT,
PRIMARY KEY(ListID),
FOREIGN KEY(UserID) REFERENCES USER(UserID)
); 

##############################################################

DROP TABLE ShoppingListRow;
SELECT * FROM ShoppingListRow;

CREATE TABLE ShoppingListRow(
ListRowID INT AUTO_INCREMENT,
ListID INT ,
ItemID INT,
ProfileID INT,
#DATUM#
PRIMARY KEY (ListID),
FOREIGN KEY(ProfileID) REFERENCES UserProfiles(UserID),
FOREIGN KEY(ItemID) REFERENCES Groceries(ItemID)

); 

##############################################################
CREATE TABLE StorageBank(
StorageID INT AUTO_INCREMENT, 
UserID INT,
PRIMARY KEY(StorageID),
FOREIGN KEY(UserID) REFERENCES USER(UserID)
); 

##############################################################

DROP TABLE StorageRow;
SELECT * FROM ShoppingListRow;

CREATE TABLE StorageRow(
StorageRowID INT AUTO_INCREMENT,
ListID INT ,
ItemID INT,
ProfileID INT,
#DATUM#
PRIMARY KEY (ListID),
FOREIGN KEY(ProfileID) REFERENCES UserProfiles(UserID),
FOREIGN KEY(ItemID) REFERENCES Groceries(ItemID)
);

############################################################

CREATE TABLE RecipeBank(
RecipeNumber int AUTO_INCREMENT, 
RecipeName VARCHAR(100), 
URL VARCHAR(100), 
UserID INT, 
PRIMARY KEY(RecipeNumber),
FOREIGN KEY(UserID) REFERENCES User(UserID)
);
##############################################################
