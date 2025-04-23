-- Rule 1: Strong Entities
CREATE TABLE Car {
	carid integer,
	brand varchar[30],
	PRIMARY KEY(carid)
};

CREATE TABLE Managers {
	ssn varchar[11],
	name varchar[255],
	email varchar[255],
	PRIMARY KEY(ssn)
};

CREATE TABLE Rent {
	rentid integer,
	rent_date date,
	PRIMARY KEY(rentid),
};

CREATE TABLE Client {
	email varchar[255],
	name varchar[255],
	PRIMARY KEY(email)
};

CREATE TABLE Address {
	city varchar[255],
	addr_num integer,
	roadname varchar[255],
	PRIMARY KEY(city, addr_num, roadname)
};

CREATE TABLE Driver {
	name varchar[255],
	PRIMARY KEY(name)
};

CREATE TABLE Credit_Card {
	cc_number int,
	PRIMARY KEY(cc_number)
};

-- Rule 2: Weak Entities
CREATE TABLE Model {
	carid integer,
	name varchar[255],
	rentid integer,
	modelid integer,
	color varchar[10],
	year integer,
	transmission varchar[30],
	PRIMARY KEY(carid, modelid, rentid, name),
	FOREIGN KEY(carid) REFERENCES Car,
	FOREIGN KEY(rentid) REFERENCES Rent,
	FOREIGN KEY(name) REFERENCES Driver
};

CREATE TABLE Review {
	name varchar[255],
	email varchar[255],
	reviewid integer,
	rating varchar[255],
	message varchar[255],
	PRIMARY KEY(name, email, reviewid),
	FOREIGN KEY(name) REFERENCES Driver,
	FOREIGN KEY(email) REFERENCES Client
};

-- Rule 3: 1-1 Relationships
-- No 1-1 Relationships found...

--Rule 4: 1-N Relationships
CREATE TABLE books {
	email 
	
	
