"""
This file is the main file that starts the entire application. It has a main menu and passes
control to the respective packages.
"""
import utils

def main_menu() -> None:
  print("Please select one of the following roles:")
  utils.print_menu_options(["1. Client", "2. Driver", "3. Manager"])
  selected_option: str = input("> ") 
  match selected_option:
    case "Client":
      # Start Client Menu
      pass
    case "Driver":
      # Start Driver Menu
      pass
    case "Manager":
      # Start Manager Menu 
      pass
    case "x":
      print("Exiting application...")
      return
    case _:
      print("Invalid Command - Please try again")
  main_menu()

print("Welcome to the Taxi Rental Management Application!")
main_menu()