#!/usr/bin/python3
#-*- coding: utf-8 -*-
import sys, os, json
import mysql.connector

# Import default vars
from pyutil import defaults
defaults = defaults.mysql

home = os.path.expanduser("~")
user_settings_file = os.path.join(home, "pyutil_settings.json")

defaults = dict(defaults)

if os.path.exists(user_settings_file):
    with open(user_settings_file) as file:
        try:
            user_defaults = json.load(file)["mysql"]
        except json.decoder.JSONDecodeError:
            print(user_settings_file+" does not contain valid JSON format!")
        except KeyError:
            # No user settings set, so dont orverwrite package defaults
            defaults = defaults
        else:
            defaults.update(user_defaults)

class MySQL:
    def __init__(self, username=None, password=None, host=None):
        self.username = username if username is not None else defaults["username"]
        self.password = password if password is not None else defaults["password"]
        self.host = host if host is not None else defaults["host"]

    def connect(self, database=None):
        self.database = database if database is not None else defaults["database"]
        # Connect without database
        try:
            db = mysql.connector.connect(
                host = self.host,
                user = self.username,
                password = self.password,
            )
            cursor = db.cursor()
            # show all databases to verify if the requested database already exists
        except:
            print(f"Something went wrong, either you provided a wrong username/password combination, or there is no mysql server running/reachable on {self.host}")

        try:
            cursor.execute(f"use {self.database}")
        except:
        # if it doesnt exist yet, create it
            user_input = input(f"Database {self.database} doesnt exist, do you want to create it now? [y/n]: ")
            if user_input == "y":
                cursor.execute(f"CREATE DATABASE {self.database}")
            else:
                print(f"Not creating database {self.database}, please specify a valid database name")
                return None
                
        # Close the old connection and reconnect using the reqested database
        db.close()
        self.db = mysql.connector.connect(
            host = self.host,
            user = self.username,
            password = self.password,
            database = self.database,
        )
        self.cursor = self.db.cursor()
    
    def exec(self, command):
        self.cursor.execute(command)
        result = self.cursor.fetchall()

        for row in result:
            print(row)

        self.db.commit()

    def create_table(self, tablename, attributes):
        self.cursor.execute(f"CREATE TABLE {tablename} (id INT AUTO_INCREMENT PRIMARY KEY, {attributes})") # attributes variable for now to be in format 'column1 TYPE, column2 TYPE'; for instance: 'name VARCHAR(255), address VARCHAR(255)'
    
    # TODO 
    # add alter table
    # add alter table add column
    # drop table?
    
    def insert(self, tablename, columns=tuple, values=tuple):
        if len(columns) != len(values):
            print("Number of given columns and given values to insert do not match")
            return None
        else:
            self.cursor.execute(f"INSERT INTO {tablename} {columns} {values}")
    
    def select(self, columns=None, search_column=None, condition=None):
        if not search_column and not condition and not columns:
            self.cursor.execute(f"SELECT * FROM {self.database}")
        if not search_column and not condition and columns != None:
            self.cursor.execute(f"SELECT {columns} FROM {self.database}")
        else: 
            self.cursor.execute(f"SELECT {columns} FROM {self.database} WHERE {search_column} = '{condition}'")
        
        result = self.cursor.fetchall()

        for row in result:
            print(row)

    def update(self, update_column, new_value, search_column, condition):
        self.cursor.execute(f"UPDATE {self.database} SET {update_column} = '{new_value}' WHERE {search_column} = '{condition}'")
        self.db.commit()

        print(f"{self.cursor.rowcount} record(s) updated")

    def delete(self, search_column, condition):
        self.cursor.execute(f"DELETE FROM {self.database} WHERE {search_column} = '{condition}'")
        self.db.commit()

        print(f"{self.cursor.rowcount} record(s) deleted")

