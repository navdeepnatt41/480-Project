-- Step 1
CREATE TABLE Managers (
    ssn int check (ssn BETWEEN 001010001 and 999999999) PRIMARY KEY,
    name varchar(255),
    email varchar(255)
);

CREATE TABLE Client (
    email varchar(255) PRIMARY KEY,
    client_name varchar(255)
);

-- CREATE TABLE Driver (  -- old so scrap
--     driver_name varchar(255) PRIMARY KEY
-- );

CREATE TABLE Address (
    city varchar(255),
    house_number int,
    road_name varchar(255),
    PRIMARY KEY (city, house_number, road_name)
);

CREATE TABLE Car (
    car_id int PRIMARY KEY,
    brand varchar(255)
);

-- CREATE TABLE CreditCard ( -- old so scrap
--     card_number char(16) PRIMARY KEY
-- );

-- CREATE TABLE Rent ( -- old so scrap
--     rent_id int PRIMARY KEY,
--     rent_date DATE
-- );

-- Step 2:

-- CREATE TABLE Model ( -- old so scrap
--     model_id int,
--     color varchar(40),
--     year DATE,
--     transmission varchar(30),
--
--     car_id int NOT NULL, -- added #1
--
--     PRIMARY KEY (car_id, model_id),
--     FOREIGN KEY (car_id) REFERENCES Car
-- );


-- CREATE TABLE Review ( -- old so scrap
--     review_id int,
--     message varchar(255),
--     rating int check (rating BETWEEN 0 AND 5),
--     driver_name varchar(255),
--
--     PRIMARY KEY (review_id, driver_name),
--     FOREIGN KEY (driver_name) REFERENCES Driver
-- );


-- Step 4 Relationships


-- 0 : N <---> 1 : 1



CREATE TABLE Model (                    --     # 1 i.e. Car <---> Model
    model_id int,
    color varchar(40),
    year DATE,
    transmission varchar(30),

    car_id int NOT NULL, -- added #1

    PRIMARY KEY (car_id, model_id),
    FOREIGN KEY (car_id) REFERENCES Car
);


CREATE TABLE Driver (                                   -- #8 Address <---> Driver
    driver_name varchar(255) PRIMARY KEY,

    city varchar(255) NOT NULL,                         -- added NOT NULL from Address
    house_number int NOT NULL,                          -- added NOT NULL from Address
    road_name varchar(255) NOT NULL,                    -- added NOT NULL from Address
    FOREIGN KEY (city, house_number, road_name)         -- added NOT NULL from Address
                        REFERENCES Address
);

CREATE TABLE Rent (                     --      # 2, 3, 4 i.e. Model <---> Rent, Driver <---> Rent, Client <---> Rent
    rent_id int PRIMARY KEY,
    rent_date DATE,

    car_id int NOT NULL,                             -- added from model
    model_id int NOT NULL,                            -- added from model
    FOREIGN KEY (car_id, model_id) REFERENCES Model,  -- added from model

    driver_name varchar(255) NOT NULL,                -- added from Driver
    FOREIGN KEY (driver_name) REFERENCES Driver,      -- added from Driver

    email varchar(255) NOT NULL,                      -- added from Client
    FOREIGN KEY (email) REFERENCES Client             -- added from Client
);


CREATE TABLE Review (                                 --  #5 Client <---> Review
    review_id int,
    message varchar(255),
    rating int check (rating BETWEEN 0 AND 5),
    driver_name varchar(255) NOT NULL,                  -- # 5 added not null from Driver <---> Review

    PRIMARY KEY (review_id, driver_name),
    FOREIGN KEY (driver_name) REFERENCES Driver,

    email varchar(255) NOT NULL,                      -- #6 added from Client
    FOREIGN KEY (email) REFERENCES Client             -- #6 added from Client
);


-- CREATE TABLE CreditCard (  --old                        -- #7 Address <---> Credit Card
--     card_number char(16) PRIMARY KEY,
--
--     city varchar(255) NOT NULL,                         -- added NOT NULL from Address
--     house_number int NOT NULL,                          -- added NOT NULL from Address
--     road_name varchar(255) NOT NULL,                    -- added NOT NULL from Address
--     FOREIGN KEY (city, house_number, road_name)         -- added NOT NULL from Address
--                         REFERENCES Address
-- );






CREATE TABLE CreditCard (                               -- #9 Address <---> Credit Card
    card_number char(16) PRIMARY KEY,

    city varchar(255) NOT NULL,                         -- added NOT NULL from Address in #7
    house_number int NOT NULL,                          -- added NOT NULL from Address in #7
    road_name varchar(255) NOT NULL,                    -- added NOT NULL from Address in #7
    FOREIGN KEY (city, house_number, road_name)         -- added NOT NULL from Address in #7
                        REFERENCES Address,

    email varchar(255) NOT NULL,                      -- #9 added from Client
    FOREIGN KEY (email) REFERENCES Client             -- #9 added from Client
);



CREATE TABLE ClientAddress (                            -- # 10
    email varchar(255),                                 -- added from Client

    city varchar(255),                                  -- added from Address
    house_number int,                                   -- added from Address
    road_name varchar(255),                             -- added from Address

    FOREIGN KEY (email) REFERENCES Client,
    FOREIGN KEY (city, house_number, road_name) REFERENCES Address,

    PRIMARY KEY (email, city, house_number, road_name)
);



CREATE TABLE ModelDriver (                              -- # 11
    model_id int,                                       -- added from Model
    car_id int,                                         -- added from Model

    driver_name varchar(255),                           -- added from Driver

    FOREIGN KEY (car_id, model_id) REFERENCES Model,    -- from Model
    FOREIGN KEY (driver_name) REFERENCES Driver,        -- from Driver

    PRIMARY KEY (car_id, model_id, driver_name)
);
