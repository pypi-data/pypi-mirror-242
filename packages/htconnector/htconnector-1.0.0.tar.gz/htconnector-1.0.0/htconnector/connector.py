import psycopg2
from psycopg2 import sql
import hashlib
from tkinter import *
import tkinter as tk
from tkinter import simpledialog, messagebox

##Function to connect to database::
def ConnectBaseStorages(htbase, htuser, htpass, hthost, htport):

    try:
        connection = psycopg2.connect(
            dbname = htbase,
            user =  htuser,
            password = htpass,
            host = hthost,
            port = htport
        )

        cursor = connection.cursor()
        print("\nConnection to the base storages is successfully..")
        print("-------------------------------------------------.\nConnected at database {htbase}.")
        
        return connection, cursor
    except psycopg2.Error as e:
        print(f"\nUnable to connect to the base storage. Error: {e}.")
        print("\n------")
        
        

##Disconnect option and sending information for user::
def DisconnectBaseStorages(connection, cursor):
    if connection:
        connection.close()
        print("\nDisconnected from base storages")
        print("Lost connection\n")
        
        
##For execution query to add smthg:: featch
def execute_query(cursor, query, params=None):
    try:
        cursor.execute(query, params)
        cursor.connection.commit()
        print("\nINFO: UseDefaultModel was created with success.\n")
        print("Table created: ok")
        print("Table name: htCase_user")
        print("Direct migration: ok")
        print("-----------------------------------------------------\nYou can use it for your default user_model")
   
    except psycopg2.Error as e:
        if  e.pgcode == '42P07':
            print("\nError: The table 'htCase_user' already  exists. You may need to handle this situation")
        else:
            print(f"Error executing query. Error: {e}\n")
        
        
##Get data from bs if exist::
def FetchDataFrom(cursor, query, params=None):
    try:
        cursor.execute(query, params)
        resutl = cursor.fetchall()
        return resutl
    except psycopg2.Error as e:
        print(f"\nError fetching data...\n Error: {e}")
        return None
    
    
            
#Create model user::
def UseDefaultUserModel(db_cursor):
    
    #Htmodeluser::
    create_table_query = """
        CREATE TABLE IF NOT EXISTS htCase_user (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            lastname VARCHAR(50),
            firstname VARCHAR(50),
            is_active BOOLEAN DEFAULT TRUE,
            gender VARCHAR(10)
        );
    """
    execute_query(db_cursor, create_table_query)


##To secure password::
def UseMd5(password):
    return hashlib.md5(password.encode()).hexdigest()


def check_password(input_password, hashed_password):
    return UseMd5(input_password) == hashed_password


###Create login registration with tkinter::
##Only for the desktop apps by default
###Create register apps::
def CreateUser(db_cursor):

    # Get user input using Tkinter dialogs
    username = simpledialog.askstring("Input", "Enter username:")
    password = simpledialog.askstring("Input", "Enter password:", show='*')
    email = simpledialog.askstring("Input", "Enter email:")
    lastname = simpledialog.askstring("Input", "Enter lastname (optional):")
    firstname = simpledialog.askstring("Input", "Enter firstname (optional):")
    is_active_str = simpledialog.askstring("Input", "Is the user active? (True/False, default is True):")
    is_active = is_active_str.lower() == 'true'
    gender = simpledialog.askstring("Input", "Enter gender (optional):")

    # Hash the password
    hashed_password = UseMd5(password)

    # SQL query to insert user data
    insert_user_query = """
        INSERT INTO htcase_user (username, password, email, lastname, firstname, is_active, gender)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """
    user_data = (username, hashed_password, email, lastname, firstname, is_active, gender)

    try:
        # Execute the query
        db_cursor.execute(insert_user_query, user_data)
        user_id = db_cursor.fetchone()[0]
        db_cursor.connection.commit()
        print(f"\n -------------------------------------\nUser '{username}' created with ID: {user_id}")
        return user_id
    except psycopg2.Error as e:
        print(f"\nError creating user. Error: {e}")
        db_cursor.connection.rollback()
        return None

##Update user model::
def UpdateUserValue(db_cursor, user_id):
    email = simpledialog.askstring("Input", "Enter new email:")
    lastname = simpledialog.askstring("Input", "Enter new lastname (optional):")
    firstname = simpledialog.askstring("Input", "Enter new firstname (optional):")
    is_active_str = simpledialog.askstring("Input", "Is the user active? (True/False):")
    is_active = is_active_str.lower() == 'true'
    gender = simpledialog.askstring("Input", "Enter new gender (optional):")
    
    update_user_query = """
        UPDATE htcase_user
        SET email = %s, lastname = %s, firstname = %s, is_active = %s, gender = %s
        WHERE id = %s;
    """
    user_data = (email, lastname, firstname, is_active, gender, user_id)

    try:
        # Execute the update query
        db_cursor.execute(update_user_query, user_data)
        db_cursor.connection.commit()
        print(f"\n---------------------------------------\nUser with ID {user_id} updated successfully.")
    except psycopg2.Error as e:
        print(f"\nError updating user. Error: {e}")
        db_cursor.connection.rollback()
    
    
##Delete user from database::
def DeleteUserValue(db_cursor, user_id):
    confirm_delete = simpledialog.askstring("Confirmation", f"Are you sure you want to delete the user with ID {user_id}? (Type 'yes' to confirm):")
    if confirm_delete.lower() != 'yes':
        print("\n---------------------------------\nDeletion canceled by the user.")
        return
    
    delete_user_query = """
        DELETE FROM htcase_user
        WHERE id = %s;
    """
    
    try:
        db_cursor.execute(delete_user_query, (user_id,))
        db_cursor.connection.commit()
        print(f"\n---------------------------------------\nUser with ID {user_id} deleted successfully.")
    except psycopg2.Error as e:
        print(f"\nError deleting user. Error: {e}")
        db_cursor.connection.rollback()
    

##Create login::
def AuthForUser(db_cursor):

    # Get user input using Tkinter dialogs
    username = simpledialog.askstring("Input", "Enter username:")
    password = simpledialog.askstring("Input", "Enter password:", show='*')

    select_user_query = """
        SELECT id, password
        FROM htcase_user
        WHERE username = %s;
    """
    
    try:
        db_cursor.execute(select_user_query, (username,))
        user_data = db_cursor.fetchone()

        if user_data:
            user_id, hashed_password = user_data
            if check_password(password, hashed_password):
                print(f"\nUser '{username}' authenticated with ID: {user_id}\n")
                return user_id
            else:
                print(f"\nAuthentication failed. Incorrect password.\n")
                return None
        else:
            print(f"User '{username}' not found.")
            return None
    except psycopg2.Error as e:
        print(f"Error authenticating user. Error: {e}\n")
        return None
    
##Logout::
def LogoutUser():
    print("\n---------------------------------\nUser logged out successfully\n")    
    
#################################################################
### About frameword apps:::
#################################################################



