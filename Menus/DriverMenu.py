"""
This file contains the main frontend for the Driver Menu; also interfaces with the backend
"""

from Backend import db_conn as db
import utils

def change_address(driver_name: str):
    print("-- Change Address --")
    city        = input("  New city: ").strip()
    house_num   = input("  House number: ").strip()
    road_name   = input("  Road name: ").strip()

    # 1. ensure Address exists
    db.run_sql(
        sql="""INSERT INTO Address (city, house_number, road_name)
               VALUES (%s,%s,%s)
               ON CONFLICT DO NOTHING""",          # harmless if it already exists
        vals=[city, house_num, road_name],
        is_crud=True
    )

    # 2. update Driver row
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
        sql = """
            SELECT c.car_id, c.brand,
                   m.model_id, m.color,
                   EXTRACT(YEAR FROM m.year)::int AS year,
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


def declare_models(driver_name: str):
    print("-- Declare Drivable Models --")
    list_car_models()

    while True:
        ids = input("Add (car_id model_id) or 'x' to finish: ").strip()
        if ids.lower() == "x":
            break

        try:
            car_id, model_id = ids.split()
        except ValueError:
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
  1:change_address,
  2:list_car_models,
  3:declare_models
}

def driver_main_menu(driver_name: str):
  options = [
    "0. Exit",
    "1. Change Your Address",
    "2. List all Car Models",
    "3. Declare Drivable Models"
  ]
  while True:
    print("\nDriver Main Menu")
    utils.print_menu_options(options)
    cmd = input("> ").strip()
    if cmd == "0":
        break
    action = {
        "1": lambda: change_address(driver_name),
        "2": list_car_models,
        "3": lambda: declare_models(driver_name)
    }.get(cmd)
    if action:
        action()
    else:
        print("Invalid selection.")

def handle_login():
  driver_name: str = input("Name: ")
  sql: str = "SELECT 1 FROM Driver WHERE driver_name = %s"
  result = db.run_sql(sql = sql, vals = [driver_name], is_crud = False)  
  if result[0][0] > 0:
    print("Driver Main Menu") 
    driver_main_menu(driver_name)
  else:
    print("Invalid Driver")

def driver_login_menu():
  while True:
    print("Welcome, Driver! Please Login OR press 'x' to exit")
    print("1. Login")
    command = input("> ")
    if command == "1":
      handle_login()
    elif command == "x":
      return
    else:
      print("Invalid command")