"""
This file is the main file that starts the entire application. It has a main menu and passes control to the respective packages.
"""
import utils
from Menus import ManagerMenu, DriverMenu, ClientMenu
from typing import Callable
import sys

MAIN_MENU_OPTIONS: dict[str, Callable] = {
  "1" : ClientMenu.client_start_menu,
  "2" : DriverMenu.driver_login_menu,
  "3" : ManagerMenu.manager_start_menu,
}

def handle_menu_option(selected_option: str) -> None:
  """
  Reads the user command and handles it:
    -     If the user command is valid (i.e. a valid string in MAIN_MENU_OPTIONS), calls the function
    -     If the user command is invalid, exits

  Args:
      selected_option (str): The user's command entered in the terminal
  """
  if selected_option in MAIN_MENU_OPTIONS.keys():
    MAIN_MENU_OPTIONS[selected_option]()
  elif selected_option == "x":
    print("Farewell!")
    sys.exit(0)
  else:
    print("Invalid Command. Please try again...")

def print_menu_options() -> None:
  """
  Prints the main menu options 
  """
  print("Please provide an option number, or 'x' to exit")
  utils.print_menu_options(["1. Client", "2. Driver", "3. Manager"])

def main_menu() -> None:
  """
  Prints the main menu and allows users to enter the application as client, 
  driver, or manager. 
  """
  while True:
    print("-------------------------------------------------\n")
    print_menu_options()
    selected_option: str = utils.get_user_input() 
    handle_menu_option(selected_option=selected_option)

if __name__ == "__main__":
  print("Welcome to the Taxi Rental Service")
  main_menu()
