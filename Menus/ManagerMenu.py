import utils
from Backend.db_conn import run_sql

# ─── Auth Handlers ─────────────────────────────────────────────────────────────

def register_manager():
    """
    Register a brand new manager.
    """
    try:
        ssn   = int(input("Enter Your SSN: "))
        name  = input("Enter Your Name: ")
        email = input("Enter Your Email: ")

        # Check for existing SSN
        exists = run_sql(
            sql="SELECT COUNT(*) FROM Managers WHERE ssn = %s",
            vals=[ssn],
            is_crud=False
        )[0][0]
        if exists:
            print("Error: Manager already exists.")
            return

        # Insert new manager
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


def login_manager():
    """
    Login an existing manager by SSN.
    """
    try:
        ssn = int(input("Enter Your SSN: "))
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


# ─── Car Handlers ──────────────────────────────────────────────────────────────

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


# ─── Driver Handlers ──────────────────────────────────────────────────────────

def add_driver():
    city      = input("Driver city: ")
    house_num = input("Driver house number: ")
    road_name = input("Driver road name: ")
    name      = input("Driver name: ")

    run_sql(
        sql="INSERT INTO Address (city, house_number, road_name) VALUES (%s, %s, %s)",
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
    name = input("Enter driver name to remove: ")
    run_sql("DELETE FROM Driver WHERE driver_name = %s", [name], is_crud=True)
    print("Driver removed.")


# ─── Reporting Handlers ──────────────────────────────────────────────────────

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


# ─── What's Left ──────────────────────────────────────────

def add_model():
    print("add_model() not yet implemented")


def remove_model():
    print("remove_model() not yet implemented")


def problematic_local_drivers():
    print("problematic_local_drivers() not yet implemented")


def driver_ratings_and_rents_by_car_brand():
    print("driver_ratings_and_rents_by_car_brand() not yet implemented")


# ─── Menu Wiring ──────────────────────────────────────────────────────────────

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

def manager_main_menu():
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

    while True:
        print("\nManager Main Menu")
        utils.print_menu_options(options)
        choice = input("> ").strip()
        if choice == "0":
            print("Goodbye!")
            break

        action = MENU_ACTIONS.get(choice)
        if action:
            action()
        else:
            print("Invalid choice; please select from the menu.")


def manager_start_menu():
    """Initial login/register loop."""
    options = ["1. Login", "2. Register", "3. Return to Main Menu"]
    while True:
        utils.print_menu_options(options)
        choice = input("> ").strip()
        if choice == "1":
            if login_manager():
                manager_main_menu()
        elif choice == "2":
            register_manager()
        elif choice == "3" or choice.lower() == "x":
            break
        else:
            print("Invalid command.")


if __name__ == "__main__":
    manager_start_menu()
