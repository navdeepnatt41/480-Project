--- Client 1:
/* When a new client registers they should add their information (name, and email
address). Furthermore, they insert their address(es) and credit card(s). Notice that a
client might have an address X but some credit card with a payment address Y which
is not the same as X. If a client is registered in the system, then the client can login to
the system using their email.
*/

-- the user inputs the name, email, address (city, house_number, road_name)

-- When a new client registers they should add their information (name, and email address).
INSERT INTO Client (email, client_name) 
SELECT 'priya@gmail.com', 'Priya'
where not exists (
    select 1 from client where email = 'priya@gmail.com'
);
INSERT INTO Address (city, house_number, road_name) VALUES ('aurora', 1234, 'aurora dr');
INSERT INTO ClientAddress (email, city, house_number, road_name) VALUES ('john@gmail.com', 'aurora', 1234, 'aurora dr');

-- insert creditcard for the client

-- if different address 
    -- insert the address
    INSERT INTO Address (city, house_number, road_name) VALUES ('new address', 1234, 'new address dr');
    now you insert the credit card

-- if no different address insert the credit card directly 
insert into creditcard (card_number, city, house_number, road_name, email) values ('1234567890123456', 'aurora', 1234, 'aurora dr', 'john@gmail.com');

SELECT * from clientaddress;
SELECT * from client;
SELECT * from creditcard;


-- Client 2

/* A client should be able to give as input a date D, and see the list of each available
(current) car models on D. A car model X is available on D if: i) X is not used at
another rent on the same date D, ii) there exists at least one driver R who can drive X,
and iii) driver R does not drive on another rent that date D. */

-- date = '2024-05-01'
-- This gets the models on that date

WITH RentedModels AS (
    SELECT car_id, model_id
    FROM Rent
    Where rent_date = '2024-05-01'
),

-- this gets the drivers on that date
DriverOnD AS (
    SELECT driver_name FROM rent
    WHERE rent_date = '2024-05-01'
),

-- combines that have at lest one free driver
ModelPlusFreeDrivers AS (
    SELECT DISTINCT md.car_id, md.model_id
    from modeldriver as md
    where md.driver_name not in (select dod.driver_name from DriverOnD as dod)
),

-- models not rented on date

AvailableModel as (
    SELECT m.car_id, m.model_id, m.color, m.year, m.transmission
    from model as m
    where (m.car_id, m.model_id) not in 
    (SELECT * FROM RentedModels)
)
-- Available models with at least one free driver
SELECT DISTINCT am.car_id, am.model_id, am.color, am.year, am.transmission
from AvailableModel as am
Join ModelPlusFreeDrivers mpfd 
On am.car_id = mpfd.car_id and am.model_id = mpfd.model_id;


-- Client 3
/* 
A client should be able to book a rent with an available car model on a specific date.
The system automatically assigns any arbitrary available driver who can drive the
requested car model. If there is no available car model on thar date the system should
return an error message to the user. */

WITH
-- Drivers already booked on the date
DriverOnD AS (
    SELECT driver_name FROM Rent
    WHERE rent_date = '2025-05-01'
),

-- this is avaibel drivers on the model that is available that day
AvailableDrivers AS (
    SELECT md.driver_name
    FROM ModelDriver md
    LEFT JOIN DriverOnD dod ON md.driver_name = dod.driver_name
    WHERE md.car_id = 1 AND md.model_id = 100 AND dod.driver_name IS NULL
),

-- this confirms that there is a model avaiabel that day
IsModelAvailable AS (
    SELECT 1 AS available
    FROM Model
    WHERE car_id = 1 AND model_id = 100
    AND NOT EXISTS (
        SELECT 1 FROM Rent r
        WHERE r.car_id = 1 AND r.model_id = 100 AND r.rent_date = '2025-05-01'
    )
),

-- picks one avaiable driver
SelectDriver AS (
    SELECT driver_name
    FROM AvailableDrivers
    LIMIT 1
),

-- this gets the next rent_id
RentID AS (
    SELECT COALESCE(MAX(rent_id), 0) + 1 AS new_id
    FROM Rent
)


INSERT INTO Rent (rent_id, rent_date, car_id, model_id, driver_name, email)
SELECT nr.new_id, '2025-05-01', 1, 100, sd.driver_name, 'kavya@gmail.com'
FROM SelectDriver sd, IsModelAvailable ima, RentID nr;

-- Client 4
/* A client should be able to see a list of all rents that the client has booked, along with
the car model and the assigned driver.
*/

select r.rent_id, r.rent_date, m.model_id, m.color, m.year, m.transmission, d.driver_name, c.brand
From Rent as r
join model as m on r.car_id = m.car_id and r.model_id = m.model_id
join driver as d on d.driver_name and r.driver_name
JOIN car as c on m.car_id = c.car_id
where r.email = 'kavya@gmail.com';


--Client 5
/* The user should be able to enter a review to a driver (that currently exists in the
system). The system should check whether the driver has been assigned to a rent
booked by the client. Otherwise, the system should not allow user to enter a review */

With DriverWithClient as (
    select DISTINCT r.driver_name
    from rent r
    where r.driver_name = 'hristian'
    and r.email = 'kavya@gmail.com'
)

insert into review (review_id, message, rating, driver_name, email)
select 2001, 'AMAZING!!', 5, 'hristian', 'kavya@gmail.com'
from DriverWithClient
where EXISTS (
    select 1
    from DriverWithClient
);

--Client 6
/* A client should have the option to book a rent with an available
specific car model with the best driver. If the client chooses this option then the system
automatically assigns the driver in the rent with the highest average rating among the
available drivers who can drive the requested available car model. */

WITH DriverOnD AS (
    SELECT driver_name
    FROM Rent 
    WHERE rent_date = '2025-05-10'
),

AvailableDrivers AS (
    SELECT md.driver_name
    FROM ModelDriver md
    LEFT JOIN DriverOnD dod ON md.driver_name = dod.driver_name
    WHERE md.car_id = 1 AND md.model_id = 100 AND dod.driver_name IS NULL
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
    WHERE car_id = 1 AND model_id = 100
      AND NOT EXISTS (
          SELECT 1 FROM Rent r
          WHERE r.car_id = 1 AND r.model_id = 100 AND r.rent_date = '2025-05-10'
      )
),

RentID AS (
    SELECT COALESCE(MAX(rent_id), 0) + 1 AS new_id
    FROM Rent
)

INSERT INTO Rent(rent_id, rent_date, car_id, model_id, driver_name, email)
SELECT r.new_id, '2025-05-10', 1, 100, bd.driver_name, 'kavya@gmail.com'
FROM BestDriver bd, IsModelAvailable, RentID r;


-- Ignore below queries

select * from address;
select * from clientaddress;
select * from creditcard;

INSERT INTO car (car_id, brand) VALUES
(1, 'Toyota'),
(2, 'Honda'),
(3, 'Ford');

INSERT INTO model (car_id, model_id, color, year, transmission) VALUES
(1, 100, 'Red', '2020-01-01', 'Automatic'),
(2, 200, 'Blue', '2021-01-01', 'Manual'),
(3, 300, 'Black', '2022-01-01', 'Automatic');

INSERT INTO driver (driver_name, city, house_number, road_name) VALUES
('Alice', 'naperville', 1234, 'naperville dr'),
('Bob', 'devon', 1234, 'devon dr'),
('Charlie', 'aurora', 1234, 'aurora dr');

INSERT INTO modeldriver (driver_name, car_id, model_id) VALUES
('Alice', 1, 100),
('Bob', 2, 200),
('Charlie', 3, 300),
('Alice', 2, 200);

INSERT INTO rent (rent_id, rent_date, car_id, model_id, driver_name, email) VALUES
(1, '2024-05-01', 1, 100, 'Alice', 'kavya@gmail.com');

select * from review;
select * from rent;



