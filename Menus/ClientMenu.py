import utils

import Backend.db_conn as db
import random


# conn =psycopg2.connect(
#     host = "localhost",
#     port = 5432,
#     database = "ProjectCS480",
#     user = "postgres",
#     password = "Hitachi@123"
# )

# cur = conn.cursor()

# cur.execute("Select * from client;")
# rows = cur.fetchall()

# for row in rows:
#     print(row)

# cur.close()
# conn.close()

email = ""

def available_car_models():
    pass

def book_rent():
    pass

def list_client_rents():
    pass

def review_driver():
    pass

def book_model_best_driver():
    pass

def landing():
    result = db.run_sql(
        sql = "SELECT * from client;",
        vals = [],
        is_crud = False
    )
    
    return result



def insertClient():
    name = input("Provide your name: ")
    global email
    email = input("Please provide your email address: ")
    exists = db.run_sql(sql="""Select * from client
                               WHERE email = %s;""",
                        vals= [email],
                        is_crud= False
                        )
    if(exists):
        print(email, "exists. Can't add Client.")
        return False
    else:
        result = db.run_sql(
                    sql ="""INSERT INTO Client (email, client_name) 
                            Values (%s, %s);""",
                    vals = [email, name],
                    is_crud=True
                )
        # print(result)
        print("Client added")
        return True

def insertAddress():
    
    # email = input("Please provide your email address: ")
    city = input("Please provide your city: ")
    house_number = int(input("Please provide your house number: "))
    road_name = input("Please provide your road name: ")
    # exists = db.run_sql(sql="""Select * from client
    #                            WHERE email = %s;""",
    #                     vals= [email],
    #                     is_crud= False
    #                     )
    if(email != ""):
        result = db.run_sql(
                    sql ="""INSERT INTO Address (city, house_number, road_name) 
                            VALUES (%s, %s, %s);""",
                    vals = [city, house_number,road_name],
                    is_crud=True
                )
        result = db.run_sql(
                    sql ="""INSERT INTO ClientAddress (email, city, house_number, road_name) 
                            VALUES (%s, %s, %s, %s);""",
                    vals = [email, city, house_number,road_name],
                    is_crud=True
                )
        print("Address added successfully!!")
    else:
        print("Please add add client before adding the address")

def viewCurrentModelsByDate():
    date = input("Enter the date to view the current available models: ")
    result = db.run_sql(sql= """WITH RentedModels AS (
                                SELECT car_id, model_id
                                FROM Rent
                                Where rent_date = %s
                            ),

                            DriverOnD AS (
                                SELECT driver_name FROM rent
                                WHERE rent_date = %s
                            ),

                            ModelPlusFreeDrivers AS (
                                SELECT DISTINCT md.car_id, md.model_id
                                from modeldriver as md
                                where md.driver_name not in (select dod.driver_name from DriverOnD as dod)
                            ),

                            AvailableModel as (
                                SELECT m.car_id, m.model_id, m.color, m.year, m.transmission
                                from model as m
                                where (m.car_id, m.model_id) not in 
                                (SELECT * FROM RentedModels)
                            )

                            SELECT DISTINCT am.car_id, am.model_id, am.color, am.year, am.transmission
                            from AvailableModel as am
                            Join ModelPlusFreeDrivers mpfd 
                            On am.car_id = mpfd.car_id and am.model_id = mpfd.model_id;""",
                        vals=[date, date],
                        is_crud=False
                        )
    if result:
        print("{:<10} {:<10} {:<10} {:<6} {:<15}".format("Car ID", "Model ID", "Color", "Year", "Transmission"))
        print("-" * 60)
        for row in result:
            # Extract the year (if it's a string like '2021-01-01')
            year = row[3].year if hasattr(row[3], 'year') else datetime.strptime(row[3], '%Y-%m-%d').year
            print("{:<10} {:<10} {:<10} {:<6} {:<15}".format(row[0], row[1], row[2], year, row[4]))
    else:
        print("Models not available")

def insertCardInfo():
    cardnumber = input("Enter your card number: ")
    city = input("Please provide your city: ")
    house_number = int(input("Please provide your house number: "))
    road_name = input("Please provide your road name: ")

    exists = db.run_sql(sql= """select * from address 
                                where city = %s and house_number = %s and road_name = %s""",
                        vals= [city, house_number, road_name],
                        is_crud= False
                        )
    if(exists):
        result = db.run_sql(
                    sql ="""insert into creditcard (card_number, city, house_number, road_name, email) 
                            values (%s, %s, %s, %s, %s);""",
                    vals = [cardnumber, city,house_number,road_name,email],
                    is_crud=True
                )
        print("Credit card added successfully")
    else:
        print("address doesn't exists pls add the address before adding the credit card")

def bookCarRent():
    car_id = 0
    model_id = 0
    date = input("Enter the date to view the current available models: ")
    brand = input("Enter the car brand you would like to rent: ")
    result = db.run_sql(sql="""select car_id from car where brand = %s""",
                        vals=[brand],
                        is_crud=False)
    if(result):
        print(result[0][0])
        car_id = result[0][0]
    # model = input("Enter the car model you would like to rent: ")
    result = db.run_sql(sql="""select model_id from model where car_id = %s""",
                        vals=[car_id],
                        is_crud=False)
    if(result):
        print(result[0][0])
        model_id = result[0][0]
        # return
    print(car_id,model_id)
    if(car_id != 0 and model_id != 0):
        result = db.run_sql(sql=""" WITH DriverOnD AS (
                                    SELECT driver_name FROM Rent
                                    WHERE rent_date = %s
                                ),

                                AvailableDrivers AS (
                                    SELECT md.driver_name
                                    FROM ModelDriver md
                                    LEFT JOIN DriverOnD dod ON md.driver_name = dod.driver_name
                                    WHERE md.car_id = %s AND md.model_id = %s AND dod.driver_name IS NULL
                                ),

                                IsModelAvailable AS (
                                    SELECT 1 AS available
                                    FROM Model
                                    WHERE car_id = %s AND model_id = %s
                                    AND NOT EXISTS (
                                        SELECT 1 FROM Rent r
                                        WHERE r.car_id = %s AND r.model_id = %s AND r.rent_date = %s
                                    )
                                ),

                                SelectDriver AS (
                                    SELECT driver_name
                                    FROM AvailableDrivers
                                    LIMIT 1
                                ),

                                RentID AS (
                                    SELECT COALESCE(MAX(rent_id), 0) + 1 AS new_id
                                    FROM Rent
                                )

                                INSERT INTO Rent (rent_id, rent_date, car_id, model_id, driver_name, email)
                                SELECT nr.new_id, %s, %s, %s, sd.driver_name, %s
                                FROM SelectDriver sd, IsModelAvailable ima, RentID nr;""",
                            vals = [date, car_id, model_id, car_id, model_id, car_id, model_id, date, date, car_id, model_id, email],
                            is_crud=True
                            )
        
        print("Booking successful. Your rental has been confirmed for", date)
    else:
        print("Car or model not available")

def viewRentalDetails():
    result = db.run_sql(sql=""" select r.rent_id, r.rent_date, m.model_id, m.color, m.year, m.transmission, d.driver_name, c.brand
                                From Rent as r
                                join model as m on r.car_id = m.car_id and r.model_id = m.model_id
                                join driver as d on d.driver_name = r.driver_name
                                JOIN car as c on m.car_id = c.car_id
                                where r.email = %s;""",
                        vals=[email],
                        is_crud=False
                        )
    if(result):
        # print(result)
        for row in result:
            rent_id, rent_date, model_id, color, year, transmission, driver_name, brand = row
            formatted_date = rent_date.strftime('%d-%b-%Y') if hasattr(rent_date, 'strftime') else str(rent_date)
            year_str = year.year if hasattr(year, 'year') else str(year)[:4]
            print("{:<8} {:<12} {:<8} {:<10} {:<6} {:<15} {:<12} {:<10}".format(
                rent_id, formatted_date, model_id, color, year_str, transmission, driver_name, brand))
    else:
        print("No rental details")
                        
def writeReview():
    driver_name = input("Enter the driver you would like to enter a review for: ")
    result = db.run_sql(sql= """select DISTINCT r.driver_name
                                from rent r
                                where r.driver_name = %s
                                and r.email = %s """,
                        vals=[driver_name,email],
                        is_crud=False
                        )
    if(result):
        # print(result[0][0])
        review = input("Enter the review: ")
        rating = int(input("Enter the rating: "))
        review_id = random.randint(1, 100)
        result = db.run_sql(sql= """insert into review (review_id, message, rating, driver_name, email)
                                    values (%s,%s,%s,%s,%s)""",
                            vals=[review_id,review,rating,driver_name,email],
                            is_crud=True
                            )
        print("Review written successfully!")

def bookRentWithBestDriver():
    car_id = 0
    model_id = 0
    date = input("Enter the date to rent the car: ")
    brand = input("Enter the car brand you would like to rent: ")
    result = db.run_sql(sql="""select car_id from car where brand = %s""",
                        vals=[brand],
                        is_crud=False)
    if(result):
        print(result[0][0])
        car_id = result[0][0]
    # model = input("Enter the car model you would like to rent: ")
    result = db.run_sql(sql="""select model_id from model where car_id = %s""",
                        vals=[car_id],
                        is_crud=False)
    if(result):
        print(result[0][0])
        model_id = result[0][0]
        # return
    # print(car_id,model_id)
    if(car_id != 0 and model_id != 0):
        result = db.run_sql(sql= """WITH DriverOnD AS (
                                    SELECT driver_name
                                    FROM Rent 
                                    WHERE rent_date = %s
                                ),

                                AvailableDrivers AS (
                                    SELECT md.driver_name
                                    FROM ModelDriver md
                                    LEFT JOIN DriverOnD dod ON md.driver_name = dod.driver_name
                                    WHERE md.car_id = %s AND md.model_id = %s AND dod.driver_name IS NULL
                                ),

                                DriverRatings AS (
                                    SELECT driver_name, AVG(rating) AS avg_rating
                                    FROM Review
                                    GROUP BY driver_name
                                ),

                                BestDriver AS (
                                    SELECT ad.driver_name
                                    FROM AvailableDrivers ad
                                    LEFT JOIN DriverRatings dr ON dr.driver_name = ad.driver_name
                                    ORDER BY COALESCE(dr.avg_rating, 0) DESC
                                    LIMIT 1
                                ),

                                IsModelAvailable AS (
                                    SELECT 1 AS available
                                    FROM Model
                                    WHERE car_id = %s AND model_id = %s
                                    AND NOT EXISTS (
                                        SELECT 1 FROM Rent r
                                        WHERE r.car_id = %s AND r.model_id = %s AND r.rent_date = %s
                                    )
                                ),

                                RentID AS (
                                    SELECT COALESCE(MAX(rent_id), 0) + 1 AS new_id
                                    FROM Rent
                                )

                                INSERT INTO Rent(rent_id, rent_date, car_id, model_id, driver_name, email)
                                SELECT r.new_id, %s, %s, %s, bd.driver_name, %s
                                FROM BestDriver bd, IsModelAvailable, RentID r;""",
                                vals=[date,car_id,model_id,car_id,model_id,car_id,model_id,date,date,car_id,model_id,email],
                                is_crud=True
                                )
        print("Booking successful")
            

                        


def login_client():
    try:
        
        global email
        email = input("Enter your email: ")
        exists = db.run_sql(sql="""Select * from client
                               WHERE email = %s;""",
                        vals= [email],
                        is_crud= False
                        )
        if(exists):
            print("Login Successful!")
            return True
        else:
            print("No client found. If you are new user please register")
    except Exception as e:
        print(f"Login error: {e}")
    return False




def register_client():
    result = insertClient()
    if(result):
        return True
    else:
        return False
        

CLIENT_START_OPTIONS = {
    "1" : login_client,
    "2" : register_client,
    "3" : None
}

def handle_client_start_menu_option(choice: str):
    if(choice == "3"):
        return None
    elif choice in CLIENT_START_OPTIONS:
        return CLIENT_START_OPTIONS[choice]()
    else:
        print("Invalid Command")

def print_client_start_menu_options():
    # options = ["1. Add Client Info", "2. Add Client Address", "3. Add Client Credit Card Info", "4. Return to Main Menu"]
    options = ["1. Login", "2. Register", "3. Return to Main Menu"]
    utils.print_menu_options(options)

def print_client_main_menu_options():
    options = [
        "0. Exit",
        "1. Add Client Address",
        "2. Add Client Credit Card Info",
        "3. View current avaiable car models on certain date",
        "4. Book car for rent",
        "5. View Rental Details",
        "6. Write a Review for Driver",
        "7. Rent a car with the best driver"
    ]
    print("\nClient Main Menu")
    utils.print_menu_options(options)



MENU_ACTIONS = {
    "1": insertAddress,
    "2": insertCardInfo,
    "3": viewCurrentModelsByDate,
    "4": bookCarRent,
    "5": viewRentalDetails,
    "6": writeReview,
    "7": bookRentWithBestDriver
}

def client_main_menu():
    while True:
        print_client_main_menu_options()
        choice = utils.get_user_input()
        if choice == "0":
            print("Au revoir!!")
            email = ""
            break
        action = MENU_ACTIONS.get(choice)
        if action:
            action()
        else:
            print("Invalid choice; please select from the menu.")

def client_start_menu():
    while True:
        print_client_start_menu_options()
        choice: str = utils.get_user_input()
        result = handle_client_start_menu_option(choice)
        if result == None:
            return
        elif result == True:
            client_main_menu() 
