"""
This file is the main file that starts the entire application. It has a main menu and passes control to the respective packages.
"""
import utils
from Menus import ManagerMenu

def main_menu() -> None:
  """
  Prints the main menu and allows users to enter the application as client, 
  driver, or manager. 
  """
  while True:
    print("-------------------------------------------------\n")
    print("Please provide an option number, or 'x' to exit")
    utils.print_menu_options(["1. Client", "2. Driver", "3. Manager"])
    selected_option: str = input("> ")
    match selected_option:
      case "1":
        # Start Client Menu 
        pass
      case "2":
        # Start Driver Menu
        pass
      case "3":
        print()
        print("Welcome, manager. Please select an option, or 'x' to return:") 
        print("-------------------------------------------------------\n")
        # Start Manager Menu 
        ManagerMenu.manager_start_menu()
        pass 
      case "x":
        print("Exiting application...") 
        return 
      case _: 
        print("Invalid Command - Please try again") 
    
if __name__ == "__main__":
  print("Welcome to the Taxi Rental Service")
  main_menu()