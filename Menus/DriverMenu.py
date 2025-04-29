"""
This file contains the main frontend for the Driver Menu; also interfaces with the backend
"""

from Backend import db_conn as db
import utils

def change_address():
  """Allows a driver to change their address"""
  pass

def list_car_models():
  """Lists all available car models"""
  pass

def declare_models():
  """Allows a driver to declare which models they can drive"""
  pass

MENU_ACTIONS = {
  1:change_address,
  2:list_car_models,
  3:declare_models
}

def driver_main_menu(dri):
  while True:
    print("Please select a numerical option or 'x' to exit: ")
    utils.print_menu_options(["0. Exit", "1. Change Your Address", "2. List all Car Models", "3. Declare a Drivable Models"])
    command = input("> ") 
    if (command != "0"):
      MENU_ACTIONS[input("> ")]
    else:
      return

def handle_login():
  driver_name: str = input("Name: ")
  sql: str = "SELECT 1 FROM Driver WHERE name = %s"
  result = db.run_sql(sql = sql, vals = [driver_name], is_crud = False)  
  if result[0][0] > 0:
    print("Driver Main Menu") 
    driver_main_menu(driver_name)
  else:
    print("Invalid Driver")

def driver_login_menu():
  while True:
    print("Welcome, Driver! Please Login OR press 'x' to exit")
    print("1. Login")
    command = input("> ")
    if command == "1":
      handle_login()
    elif command == "x":
      return
    else:
      print("Invalid command")