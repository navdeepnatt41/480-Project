"""
This file contains some functions that end up being used across the application
"""

def print_menu_options(options_list: list[str]) -> None:
  print("\n".join(options_list))

def get_user_input() -> str:
  """
  Simply gets and returns the user input from the terminal

  Returns:
  str: The user input 
  """
  return input("> ").strip()