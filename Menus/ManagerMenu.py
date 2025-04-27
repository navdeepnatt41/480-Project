
import utils
import Backend.db_conn as db

def handle_register():
  try:
      ssn: int = int(input("Enter Your SSN: "))
      name: str = input("Enter Your Name: ") 
      email: str = input("Enter Your Email: ")
      
      ssn_check_query = "SELECT COUNT(*) FROM Managers WHERE ssn = %s"
      result = db.run_sql(sql=ssn_check_query, vals=[ssn], is_crud=False)
      
      if result[0][0] > 0:
          print("Error: This Manager exists. Returning to manager login menu...") 
          return
      
      insert_query = "INSERT INTO Managers (ssn, name, email) VALUES (%s, %s, %s)"
      db.run_sql(sql=insert_query, vals=[ssn, name, email], is_crud=True)
      
      print("New Manager Added. Logging you in...")
      # Placeholder for going to manager login menu
      return

  except ValueError:
      print("SSN format not accepted. Returning to manager login menu...")
      
def handle_login():
  try:
    ssn: int = int(input("Enter Your SSN: "))
    ssn_check_query: str = "SELECT COUNT(*) FROM Managers WHERE ssn = %s"
    result: list = db.run_sql(sql=ssn_check_query, vals=[ssn], is_crud=False)
      
    if result[0][0] > 0:
      print("Welcome back! Taking you to your main menu...")
      return
  
  except Exception as e:
    print("An error has occurred. Maybe check your formats?")
    print("Returning to login menu...")

def add_car():
  pass

def remove_car():
  pass

def add_driver():
  pass

def manager_main_menu():
  options: list[str] = [
    "1. Add a Car",
    "2. Remove a Car",
    "3. Add a Driver", 
    "4. Add a Model",
    "5. Remove a Model",
    "6. Remove a Driver",
    "7. Top-K Clients",
    "8. All Models and Rents",
    "9. Driver Stats",
    "10. Find Clients by City Pair",
    "11. Problematic Local Drivers",
    "12. Driver Ratings and Rents by Car Brand"
  ]
  print("Manager Main Menu\n\n")
  utils.print_menu_options(options)
  user_input: str = input("Please provide an option number: ")


def manager_start_menu():
  utils.print_menu_options(["- Login", "- Register", "- Return to Main Menu"]) 
  option: str = input("> ")
  match option:
    case "3":
      print("Returning to main menu...")
      return
    case "2":
      handle_register()
      pass
    case "1":
      # handle login
      pass
    case _:
      print("Invalid Command.")
  manager_start_menu()

      

