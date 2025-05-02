"""
This file contains the main frontend for the Driver Menu; also interfaces with the backend
"""

from Backend import db_conn as db
import utils

driver_name: str = ""

def get_address_input() -> tuple[str, str, str]:
    """
    Parses and returns the user input for `change_address`

    Returns:
        -   tuple[str, str, str]: [city, house_num, road_name]
    """
    city      = input("  New city: ").strip()
    house_num = input("  House number: ").strip()
    road_name = input("  Road name: ").strip()
    return (city, house_num, road_name)


def change_address():
    print("-- Change Address --")
    (city, house_num, road_name) = get_address_input()

    db.run_sql(
        sql="""INSERT INTO Address (city, house_number, road_name)
               VALUES (%s,%s,%s)
               ON CONFLICT DO NOTHING""",
        vals=[city, house_num, road_name],
        is_crud=True
    )
    db.run_sql(
        sql="""UPDATE Driver
               SET city = %s, house_number = %s, road_name = %s
               WHERE driver_name = %s""",
        vals=[city, house_num, road_name, driver_name],
        is_crud=True
    )
    print("Address updated.")


def list_car_models():
    rows = db.run_sql(
        sql="""
            SELECT c.car_id, c.brand,
                   m.model_id, m.color,
                   m.year       AS year,
                   m.transmission
            FROM   Car   c
            JOIN   Model m ON c.car_id = m.car_id
            ORDER  BY c.car_id, m.model_id
        """,
        vals=[],
        is_crud=False
    )
    if not rows:
        print("No models in the system.")
        return

    print("-- All Car Models --")
    for car_id, brand, model_id, color, year, trans in rows:
        print(f"Car {car_id} ({brand})  Model {model_id}: {color}, {year}, {trans}")


def declare_drivable_models():
    print("-- Declare Drivable Models --")
    list_car_models()

    while True:
        ids = input("Add (car_id model_id) or 'x' to finish: ").strip()
        if ids.lower() == "x":
            break

        try:
            car_id, model_id = ids.split()
            car_id = int(car_id)
            model_id = int(model_id) 
        except (TypeError, ValueError):
            print("Enter two integers separated by a space.")
            continue

        # verify model exists
        ok = db.run_sql(
            sql="SELECT 1 FROM Model WHERE car_id=%s AND model_id=%s",
            vals=[car_id, model_id],
            is_crud=False
        )
        if not ok:
            print("  -- That (car_id, model_id) does not exist.")
            continue

        # insert if not already present
        db.run_sql(
            sql="""
                INSERT INTO ModelDriver (car_id, model_id, driver_name)
                VALUES (%s,%s,%s)
                ON CONFLICT DO NOTHING
            """,
            vals=[car_id, model_id, driver_name],
            is_crud=True
        )
        print(" Driver declare added.")


MENU_ACTIONS = {
    "1": change_address,
    "2": list_car_models,
    "3": declare_drivable_models
}

def print_driver_main_menu_opts() -> None:
    """
    Prints the main menu options for driver
    """
    print("Please select a numerical option or 'x' to exit: ")
    utils.print_menu_options([
        "0. Exit",
        "1. Change Your Address",
        "2. List all Car Models",
        "3. Declare a Drivable Models"
    ])

def driver_main_menu(dri: str):
    global driver_name
    driver_name = dri
    while True:
        print_driver_main_menu_opts()
        command = utils.get_user_input()
        if command != "0":
            MENU_ACTIONS[command]()
        else:
            return

def handle_login():
    driver_input: str = input("Name: ")
    sql: str = "SELECT 1 FROM Driver WHERE driver_name = %s"
    result = db.run_sql(sql=sql, vals=[driver_input], is_crud=False)
    if result and result[0][0] > 0:
        print("Driver Main Menu")
        driver_main_menu(driver_input)
    else:
        print("Invalid Driver")

def empty_func() -> None:
    pass

DRIVER_LOGIN_OPTIONS = {
    "1": (handle_login, False),
    "x": (empty_func, True)
}

def handle_driver_login_user_inputs(command: str):
    """
    Matches user input at login stage to a function call

    Returns:
        -   bool: Condition checking whether the command is a request to exit the login menu
                  or calling login menu
    """
    if command in DRIVER_LOGIN_OPTIONS:
        DRIVER_LOGIN_OPTIONS[command][0]()
        return DRIVER_LOGIN_OPTIONS[command][1]
    else:
        print("Invalid Command")


def print_driver_login_menu() -> None:
    """
    Prints the driving menu option
    """
    print("1. Login")

def driver_login_menu():
    print("Welcome, Driver! Please Login OR press 'x' to exit")
    while True:
        print_driver_login_menu()
        command = utils.get_user_input()
        if handle_driver_login_user_inputs(command) is True:
            return
