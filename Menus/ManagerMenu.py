
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
      manager_main_menu()
  except ValueError:
      print("SSN format not accepted. Returning to manager login menu...")
      
def handle_login():
  try:
    ssn: int = int(input("Enter Your SSN: "))
    ssn_check_query: str = "SELECT COUNT(*) FROM Managers WHERE ssn = %s"
    result: list = db.run_sql(sql=ssn_check_query, vals=[ssn], is_crud=False)
      
    if result[0][0] > 0:
      print("Welcome back! Taking you to your main menu...")
      manager_main_menu()
      return
  
  except Exception as e:
    print("An error has occurred. Maybe check your formats?")
    print("Returning to login menu...")

def add_car():
  """Handles adding a new car to the system."""
  car_id: str = input("Enter your car id: ")
  brand: str = input("Enter the car's brand: ")

  result = db.run_sql(
     sql = "SELECT 1 FROM Car where brand LIKE %s",
     vals = [car_id],
     is_crud = False
  )

  if result == []:
     db.run_sql(
        sql = "INSERT INTO Car (car_id, brand) VALUES (%s, %s)",
        vals = [car_id, brand],
        is_crud = True
     )
     print("Car inserted into db")
  else:
     print("Car already exists")
  manager_main_menu() 
  breakpoint()

  pass

def remove_car():
    """Handles removing an existing car from the system."""
    car_id: str = input("Enter car id to delete: ")
    db.run_sql(sql = "DELETE FROM Rent WHERE car_id = %s;", vals=[], is_crud=True)
    db.run_sql(sql = "DELETE FROM ModelDriver WHERE car_id = %s;", vals=[], is_crud=True)
    db.run_sql(sql = "DELETE FROM Model WHERE car_id = %s;", vals=[], is_crud=True)
    db.run_sql(sql = "DELETE FROM Car WHERE car_id = %s;", vals=[], is_crud=True)
    print("Deleted car")

def add_driver():
    """Handles adding a new driver to the system."""
    city: str = input("Enter Driver's Address - City: ")
    house_num: str = input("Enter Driver's Address - House Number: ")
    road_name: str = input("Enter Driver's Address - Road Name: ")
    name: str = input("Enter Driver's Name")
    db.run_dql(
        sql = "INSERT INTO Address (city, house_number, road_name) VALUES (%s, %s, %s)",
        vals = [city, house_num, road_name],
        is_crud = True
    )
    db.run_sql(
        sql = "INSERT INTO Driver (driver_name, city, house_number, road_name) VALUES (%s, %s, %s, %s)",
        vals = [name, city, house_num, road_name],
        is_crud = False
    )
    print("Inserted Driver")


def remove_driver():
    """Handles removing an existing driver from the system."""
    name: str = input("Provide the name of the driver to remove: ") 
    db.run_sql(
        sql = "DELETE FROM Driver WHERE name = %s",
        vals = [name],
        is_crud = True
    )

def add_model():
    """Handles adding a new car model to the system."""
    pass

def remove_model():
    """Handles removing a car model from the system."""
    pass

def top_k_clients():
    """Handles fetching and displaying the top-K clients."""
    k: str = input("How many top clients by rent to display: ")
    sql = """
            SELECT client_name
            FROM Client
            JOIN Rent
                ON Client.email = Rent.email
            GROUP BY Client.name
            ORDER BY COUNT(Rent.rent_id) desc
            LIMIT %s
          """
    print(db.run_sql(sql = sql, vals = [k], is_crud=False))

def all_models_and_rents():
    """Handles displaying all models along with their rents."""
    sql = """
            SELECT Model.car_id, Model.model_id, COUNT(Rent.rent_id)
            FROM Model
            JOIN Rent
                ON Model.car_id = Rent.car_id
                AND Model.model_id = Rent.model_id
            GROUP BY Model.car_id, Model.model_id;
          """
    print(db.run_sql(
        sql = sql,
        vals = [],
        is_crud = False
    ))

def driver_stats():
    """Handles displaying driver statistics."""
    sql = """
            SELECT 
            d.driver_name,
            COUNT(DISTINCT r.rent_id) AS total_rents,
            AVG(rv.rating) AS average_rating
            FROM 
                Driver d
            LEFT JOIN 
                Rent r ON d.driver_name = r.driver_name
            LEFT JOIN 
                Review rv ON d.driver_name = rv.driver_name
            GROUP BY 
                d.driver_name;

            """ 

def find_clients_by_city_pair():
    """Handles finding clients based on city pairs."""
    sql =   """
            SELECT DISTINCT c.email, c.client_name
            FROM Client c
            JOIN ClientAddress ca ON c.email = ca.email
            JOIN Address a1 ON ca.city = a1.city AND ca.house_number = a1.house_number AND ca.road_name = a1.road_name
            JOIN Rent r ON c.email = r.email
            JOIN Driver d ON r.driver_name = d.driver_name
            JOIN Address a2 ON d.city = a2.city AND d.house_number = a2.house_number AND d.road_name = a2.road_name
            WHERE a1.city = :C1
            AND a2.city = :C2;
            
            """
    pass 

def problematic_local_drivers():
    """Handles identifying problematic local drivers."""
    pass

def driver_ratings_and_rents_by_car_brand():
    """Handles showing driver ratings and rents, filtered by car brand."""
    pass

def manager_main_menu():
    options: list[str] = [
        "0. Exit",
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
    
    while True:
        print("\nManager Main Menu\n")
        utils.print_menu_options(options)
        user_input: str = input("Please provide an option number, or 'x' to return to manager login menu: ")

        match user_input:
            case "0":
                print("Exiting Manager Menu. Goodbye!")
                break  # Exit the loop safely

            case "1":
                add_car()
            case "2":
                remove_car()
            case "3":
                add_driver()
            case "4":
                add_model()
            case "5":
                remove_model()
            case "6":
                remove_driver()
            case "7":
                top_k_clients()
            case "8":
                all_models_and_rents()
            case "9":
                driver_stats()
            case "10":
                find_clients_by_city_pair()
            case "11":
                problematic_local_drivers()
            case "12":
                driver_ratings_and_rents_by_car_brand()
            case _:
                print("Invalid option. Please enter a number from the menu.")

def manager_start_menu():
  while True:
    utils.print_menu_options(["- Login", "- Register", "- Return to Main Menu"]) 
    option: str = input("> ")
    match option:
        case "3":
            print("Returning to main menu...")
            return
        case "2":
            handle_register()
        case "1":
            handle_login()
        case _:
            print("Invalid Command.")

      

