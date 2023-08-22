import sqlite3
import os

try: # Try to create the table where the user info will be stored
    sqlite_connection = sqlite3.connect('Database.db')
    sqlite_create_table = '''CREATE TABLE if not Exists users (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                password TEXT NOT NULL);'''

    cursor = sqlite_connection.cursor()
    cursor.execute(sqlite_create_table)
    sqlite_connection.commit()
    print("OK! Database connection established.\n")
    cursor.close()
except sqlite3.Error as error:
    print("ERROR! Error while creating a SQLite table.", error)
finally: 
    if sqlite_connection:
        sqlite_connection.close()

def create_account(username, password): # This function inserts the account information into the 'users' table
    try:
        sqlite_connection = sqlite3.connect('Database.db')
        cursor = sqlite_connection.cursor()

        sqlite_insert_with_param = f"""INSERT INTO users (username, password) VALUES ('{username}', '{password}');"""

        cursor.execute(sqlite_insert_with_param)
        sqlite_connection.commit()
        print("Account succesfully created.")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert credentials into SQLite table.", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def login_account(username, password): # Login to your 'account' if the name and password exists in the table
    try:
        sqlite_connection = sqlite3.connect('Database.db')
        cursor = sqlite_connection.cursor()

        sqlite_check_login = f"""SELECT username from users WHERE username='{username}' and password='{password}';"""
        cursor.execute(sqlite_check_login)
        if not cursor.fetchone():
            print("Login failed.")
        else:
            print("Welcome.")

        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to select username and password.", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def check_for_account(username, password): # Checks if the account name already exists in the table
    try:
        sqlite_connection = sqlite3.connect('Database.db')
        cursor = sqlite_connection.cursor()

        sqlite_check_login = f"""SELECT username from users WHERE username='{username}';"""
        cursor.execute(sqlite_check_login)
        if not cursor.fetchone():
            create_account(username, password)
        else:
            print("Username already in use.")

        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print(error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# Interact with the user and ask for username and password
while True:
    print("Hello and welcome to the login page. In order to gain access to the control panel please log in with your account.\nDon't have an account? Leave the field blank and continue.\n")

    login_page_user = str((input("Username: ")))
    login_page_pass = str((input("Password: ")))

    # If the user doesn't have an account already they can register
    if login_page_user == "" and login_page_pass == "":
        os.system('cls')
        print("This is the register page. Please provide your credentials.\n")

        register_page_user = str((input("Username: ")))
        register_page_pass = str((input("Password: ")))

        if register_page_user == "" or register_page_pass == "":
            print("You must fill out all credentials.")
            continue

        check_for_account(register_page_user, register_page_pass)
    #If both credentials are provided then login to the account
    else:
        login_account(login_page_user, login_page_pass)
