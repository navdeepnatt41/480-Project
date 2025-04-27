"""
This file is the main file that starts the entire application. It has a main menu and passes control to the respective packages.
"""
import utils
from Menus import ManagerMenu

def main_menu() -> None:
  print("Please select one of the following roles/options:")
  utils.print_menu_options(["- Client", "- Driver", "- Manager", "- x (to exit)"])
  selected_option: str = input("> ")
  match selected_option:
    case "Client":
      # Start Client Menu 
      pass
    case "Driver":
      # Start Driver Menu
      pass
    case "Manager":
      print("Welcome, manager. Please select an option:") 
      # Start Manager Menu 
      ManagerMenu.manager_start_menu()
      pass 
    case "x":
      print("Exiting application...") 
      return 
    case _: 
      print("Invalid Command - Please try again") 
  main_menu()
    
main_menu()