"""
This file contains the main frontend for the Driver Menu; also interfaces with the backend
"""

def driver_login_menu():
  print("Welcome, Driver! Please Login")
  driver_name: str = input("Name: ")
  # handle driver login