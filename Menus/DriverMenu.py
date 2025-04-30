"""
This file contains the main frontend for the Driver Menu; also interfaces with the backend
"""

from Backend import db_conn as db

def change_address():
  pass

def list_car_models():
  pass

def declare_models():
  pass

def driver_main_menu():
  # while True:
  pass
    

def handle_login():
  driver_name: str = input("Name: ")
  sql: str = "SELECT 1 FROM Driver WHERE name = %s"
  result = db.run_sql(sql = sql, vars = [driver_name], is_crud = False)  
  if result[0][0] > 0:
    print("Driver Main Menu")
    driver_main_menu()



def driver_login_menu():
  print("Welcome, Driver! Please Login")
  # handle driver login