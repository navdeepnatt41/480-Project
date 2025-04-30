import utils
from Backend.db_conn import run_sql

def get_manager_registration_input() -> tuple[str, str, str, bool]:
    """
    Retrieves the necessary manager information required from the user input.
    Parses and does error checking: fails if error checking went bad

    Returns:
        -   tuple[str, str, str, bool]: [ssn, name, email, successful_parse]
            -    If successful_parse is false, the first 3 values are supplied as empty strings 
    """
    ssn: str = (input("Enter Your SSN: "))
    if len(ssn) != 9:
        print("Invalid ssn")
        return ("","","",False)
    name: str = input("Enter Your Name: ")
    email: str = input("Enter Your Email: ")
    return (ssn, name, email, True)


def register_manager():
    """
    Register a brand new manager.
    """
    try:
        (ssn, name, email, successful_parse) = get_manager_registration_input()

        if not successful_parse:
            return None
        
        exists = run_sql(
            sql="SELECT COUNT(*) FROM Managers WHERE ssn = %s",
            vals=[ssn],
            is_crud=False
        )[0][0]

        if exists:
            print("Error: Manager already exists.")
            return

        run_sql(
            sql="INSERT INTO Managers (ssn, name, email) VALUES (%s, %s, %s)",
            vals=[ssn, name, email],
            is_crud=True
        )
        
        print("Manager registered successfully.")

    except ValueError:
        print("Invalid SSN format.")
    except Exception as e:
        print(f"Registration failed: {e}")
    finally:
        return 1

def login_manager():
    """
    Login an existing manager by SSN.
    """
    try:
        ssn = (input("Enter Your SSN: "))
        if len(ssn) < 8:
            print("Extra not good")
            return
        exists = run_sql(
            sql="SELECT COUNT(*) FROM Managers WHERE ssn = %s",
            vals=[ssn],
            is_crud=False
        )[0][0]
        if exists:
            print("Login successful!")
            return True
        else:
            print("No manager found with that SSN.")
    except ValueError:
        print("Invalid SSN format.")
    except Exception as e:
        print(f"Login error: {e}")
    return False

def add_car():
    car_id = input("Enter new car ID: ")
    brand  = input("Enter car brand: ")

    exists = run_sql(
        sql="SELECT 1 FROM Car WHERE car_id = %s",
        vals=[car_id],
        is_crud=False
    )
    if exists:
        print("That car already exists.")
    else:
        run_sql(
            sql="INSERT INTO Car (car_id, brand) VALUES (%s, %s)",
            vals=[car_id, brand],
            is_crud=True
        )
        print("Car inserted.")

def remove_car():
    car_id = input("Enter car ID to delete: ")
    # delete in correct dependency order
    run_sql("DELETE FROM Rent WHERE car_id = %s",     [car_id], is_crud=True)
    run_sql("DELETE FROM ModelDriver WHERE car_id = %s",[car_id], is_crud=True)
    run_sql("DELETE FROM Model WHERE car_id = %s",    [car_id], is_crud=True)
    run_sql("DELETE FROM Car WHERE car_id = %s",      [car_id], is_crud=True)
    print("Car deleted.")

def add_model():
    car_id   = input("Enter a existing car_id: ").strip()
    model_id = input("Enter the model_id: ").strip()
    color    = input("Enter the color of the car: ").strip()
    year     = input("Enter the year of the car (YYYY): ").strip()
    trans    = input("Enter the transmission of the car (manual/automatic): ").strip().lower()

    # Error checking
    if not run_sql("SELECT 1 FROM Car WHERE car_id = %s",
                [car_id], is_crud=False):
        print("That car_id is not in Car.  Insert the car first.")
        return
    if run_sql("SELECT 1 FROM Model WHERE car_id = %s AND model_id = %s",
               [car_id, model_id], is_crud=False):
        print("That (car_id, model_id) already exists.")
        return

    # Insert user input into the database
    run_sql(
        sql=("INSERT INTO Model "
             "(model_id, color, year, transmission, car_id) "
             "VALUES (%s, %s, %s, %s, %s)"),
        vals=[model_id, color, f"{year}-01-01", trans, car_id],  # DATE needs YYYY-MM-DD
        is_crud=True
    )
    print("Model inserted.")

def remove_model():
    """
    This function is for deleting a model from the model table.
    To do this we need to have car_id and model_id.
    We also need to take into account the ModelDriver table.
    If we are going to delete the model that has a particular model_id
    we also need to delete it from the ModelDriver table.   
    """
    car_id = input("Enter a existing car_id: ").strip()
    model_id = input("Enter a exitsting model_id: ").strip()

    run_sql("DELETE FROM ModelDriver WHERE car_id=%s AND model_id=%s",
        [car_id, model_id], is_crud=True)
    run_sql("DELETE FROM Rent WHERE car_id=%s AND model_id=%s",
        [car_id, model_id], is_crud=True)
    deleted = run_sql("DELETE FROM Model WHERE car_id=%s AND model_id=%s",
                      [car_id, model_id], is_crud=True)
    # print("Model removed." if deleted else "Nothing to delete.")
    print("Deletion Operation Successful")

def add_driver():
    # Maybe need to fix with try catch stuff
    # Driver Error stuff again - major issue with a driver not inserting
    city      = input("Driver city: ")
    house_num = input("Driver house number: ")
    road_name = input("Driver road name: ")
    name      = input("Driver name: ")

    exists = run_sql(
        sql=(
            "SELECT 1 FROM Address "
            "WHERE city = %s AND house_number = %s AND road_name = %s"
        ),
        vals=[city, house_num, road_name],
        is_crud=False
    )

    if not exists:
        run_sql(
            sql=(
                "INSERT INTO Address (city, house_number, road_name) "
                "VALUES (%s, %s, %s)"
            ),
            vals=[city, house_num, road_name],
            is_crud=True
        )

    run_sql(
        sql=(
            "INSERT INTO Driver "
            "(driver_name, city, house_number, road_name) "
            "VALUES (%s, %s, %s, %s)"
        ),
        vals=[name, city, house_num, road_name],
        is_crud=True
    )
    print("Driver added.")

def remove_driver():
    """
    Remove a driver and all of their associated records.
    """
    # Major issue; it seems a driver isn't being found and then removed
    name = input("Enter driver name to remove: ").strip()

    # 1) Verify the driver exists
    exists = run_sql(
        sql="SELECT 1 FROM Driver WHERE driver_name = %s",
        vals=[name],
        is_crud=False
    )
    if not exists:
        print(f"No driver found with name '{name}'.")
        return

    # 2) Delete dependent records in the correct order
    run_sql(
        sql="DELETE FROM ModelDriver WHERE driver_name = %s",
        vals=[name],
        is_crud=True
    )
    run_sql(
        sql="DELETE FROM Rent        WHERE driver_name = %s",
        vals=[name],
        is_crud=True
    )
    run_sql(
        sql="DELETE FROM Review      WHERE driver_name = %s",
        vals=[name],
        is_crud=True
    )

    # 3) Finally delete the driver
    run_sql(
        sql="DELETE FROM Driver      WHERE driver_name = %s",
        vals=[name],
        is_crud=True
    )

    print(f"Driver '{name}' and all related records removed.")

def top_k_clients():
    try:
        k = int(input("How many top clients to show? "))
    except ValueError:
        print("Please enter a number.")
        return

    rows = run_sql(
        sql=(
            "SELECT c.client_name, c.email, COUNT(r.rent_id) AS rents "
            "FROM Client c JOIN Rent r ON c.email = r.email "
            "GROUP BY c.client_name, c.email "
            "ORDER BY rents DESC LIMIT %s"
        ),
        vals=[k],
        is_crud=False
    )
    for name, email, count in rows:
        print(f"{name} <{email}> — {count} rents")


def all_models_and_rents():
    # Fix - Some weird bull with tables
    rows = run_sql(
        sql=(
            "SELECT m.car_id, m.model_id, COUNT(r.rent_id) "
            "FROM Model m JOIN Rent r "
            "  ON m.car_id = r.car_id AND m.model_id = r.model_id "
            "GROUP BY m.car_id, m.model_id"
        ),
        vals=[],
        is_crud=False
    )
    for car_id, model_id, cnt in rows:
        print(f"Car {car_id}, Model {model_id}: {cnt} rents")


def driver_stats():
    # Threw an error: need to check
    rows = run_sql(
        sql=(
            "SELECT d.driver_name, COUNT(r.rent_id) AS total_rents, "
            "AVG(rv.rating) AS avg_rating "
            "FROM Driver d "
            "LEFT JOIN Rent r ON d.driver_name = r.driver_name "
            "LEFT JOIN Review rv ON d.driver_name = rv.driver_name "
            "GROUP BY d.driver_name"
        ),
        vals=[],
        is_crud=False
    )
    for name, total, avg in rows:
        print(f"{name}: {total} rents, avg rating {avg:.2f}")


def find_clients_by_city_pair():
    c1 = input("City #1: ")
    c2 = input("City #2: ")
    rows = run_sql(
        sql=(
            "SELECT DISTINCT c.email, c.client_name "
            "FROM Client c "
            "  JOIN ClientAddress ca ON c.email = ca.email "
            "  JOIN Address a1 ON (ca.city,a1.house_number,ca.road_name) = "
            "                   (a1.city,a1.house_number,a1.road_name) "
            "  JOIN Rent r ON c.email = r.email "
            "  JOIN Driver d ON r.driver_name = d.driver_name "
            "  JOIN Address a2 ON (d.city,d.house_number,d.road_name) = "
            "                   (a2.city,a2.house_number,a2.road_name) "
            "WHERE a1.city = %s AND a2.city = %s"
        ),
        vals=[c1, c2],
        is_crud=False
    )
    for email, name in rows:
        print(f"{name} <{email}>")

def problematic_local_drivers():
    
    rows = run_sql(
    sql="""
            WITH avg_ratings AS (
                SELECT
                    driver_name,
                    AVG(rating) AS avg_rating
                FROM Review
                GROUP BY driver_name
            )
            SELECT
                d.driver_name
            FROM
                Driver AS d
            JOIN avg_ratings AS ar
                ON d.driver_name = ar.driver_name
            JOIN Rent AS r
                ON d.driver_name = r.driver_name
            JOIN ClientAddress AS ca
                ON r.email = ca.email
            WHERE
                d.city  = 'Chicago'
                AND ca.city = 'Chicago'
            GROUP BY
                d.driver_name, ar.avg_rating
            HAVING
                ar.avg_rating < 2.5
                AND COUNT(DISTINCT r.email) >= 2;

        """,
    vals=[],
    is_crud=False
    )

    if rows:
        print("Problematic local drivers:")
        for (name,) in rows:
            print(f" • {name}")
    else:
        print("None match the criteria.")

def driver_ratings_and_rents_by_car_brand():
    sql = """
            WITH driver_avg AS (
                SELECT driver_name, AVG(rating) AS avg_rating
                FROM   Review
                GROUP  BY driver_name
            ),
            brand_driver AS (
                SELECT DISTINCT c.brand, md.driver_name
                FROM   Car c
                JOIN   Model m    ON c.car_id   = m.car_id
                JOIN   ModelDriver md
                        ON md.car_id = m.car_id AND md.model_id = m.model_id
            ),
            brand_rents AS (
                SELECT c.brand, COUNT(r.rent_id) AS rent_count
                FROM   Car   c
                JOIN   Model m ON c.car_id = m.car_id
                JOIN   Rent  r ON m.car_id = r.car_id AND m.model_id = r.model_id
                GROUP  BY c.brand
            )
            SELECT
                b.brand,
                ROUND(AVG(da.avg_rating)::numeric, 2) AS avg_driver_rating,
                COALESCE(br.rent_count, 0)            AS rent_count
            FROM   brand_driver b
            LEFT   JOIN driver_avg  da ON b.driver_name = da.driver_name
            LEFT   JOIN brand_rents br ON b.brand = br.brand
            GROUP  BY b.brand, br.rent_count
            ORDER  BY b.brand
            """
    rows = run_sql(
        sql = sql,
        vals=[],
        is_crud=False
    )
    for brand, avg_rating, rent_cnt in rows:
        print(f"{brand:15}  avg driver rating: {avg_rating or 'N/A':>5}  rents: {rent_cnt}")

MENU_ACTIONS = {
    "1": add_car,
    "2": remove_car,
    "3": add_driver,
    "4": add_model,
    "5": remove_model,
    "6": remove_driver,
    "7": top_k_clients,
    "8": all_models_and_rents,
    "9": driver_stats,
    "10": find_clients_by_city_pair,
    "11": problematic_local_drivers,
    "12": driver_ratings_and_rents_by_car_brand,
}

def print_manager_main_menu_options():
    options = [
        "0. Exit",
        "1. Add a Car",
        "2. Remove a Car",
        "3. Add a Driver",
        "4. Add a Model",
        "5. Remove a Model",
        "6. Remove a Driver",
        "7. Top-K Clients",
        "8. All Models & Rents",
        "9. Driver Stats",
        "10. Find Clients by City Pair",
        "11. Problematic Local Drivers",
        "12. Driver Ratings & Rents by Brand",
    ]
    print("\nManager Main Menu")
    utils.print_menu_options(options)

def manager_main_menu():
    while True:
        print_manager_main_menu_options()
        choice = utils.get_user_input() 
        if choice == "0":
            print("Goodbye!")
            break
        action = MENU_ACTIONS.get(choice)
        if action:
            action()
        else:
            print("Invalid choice; please select from the menu.")

MANAGER_START_OPTIONS = {
    "1" : login_manager,
    "2" : register_manager,
    "3" : None
}

def handle_manager_start_menu_option(choice: str):
    """
    Handles calling the start menu option handles based off of the user choice; if
    choice is 3, returns None to signal exit from ManagerMenu


    Args:
        choice (str): The user input  
    """
    if choice == "3":
        return None
    elif choice in MANAGER_START_OPTIONS:
        return MANAGER_START_OPTIONS[choice]()
    else:
        print("Invalid Command")

def print_manager_start_menu_options() -> None:
    """
    Prints the manager start menu options to the screen 
    """
    options = ["1. Login", "2. Register", "3. Return to Main Menu"]
    utils.print_menu_options(options)

def manager_start_menu():
    """Initial login/register loop."""
    while True:
        print_manager_start_menu_options()
        choice: str = utils.get_user_input() 
        result = handle_manager_start_menu_option(choice) 
        if result == None:
            return
        elif result == True:
            manager_main_menu()
