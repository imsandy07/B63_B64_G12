DROP DATABASE IF EXISTS sales_db;
CREATE DATABASE IF NOT EXISTS sales_db;
USE sales_db;


CREATE TABLE ImportedFiles (
	fileName	VARCHAR(20) PRIMARY KEY
);
CREATE TABLE Region (
	`code`	CHAR(1) PRIMARY KEY,
	`name`	VARCHAR(20) NOT NULL
);
CREATE TABLE Sales (
	ID	INTEGER PRIMARY KEY AUTO_INCREMENT,
	amount	REAL NOT NULL DEFAULT 0.0,
	salesDate	CHAR(10) NOT NULL,
	region	CHAR(1) NOT NULL
);
CREATE TABLE sqlite_sequence(
	`name` VARCHAR(5),
	`seq` INTEGER
);

INSERT INTO ImportedFiles 
VALUE("sales_q1_2021_w.csv");
INSERT INTO Region
VALUE("w", "West"), 
	 ("m", "Mountain"), 
     ("c", "Central"), 
     ("e", "East");
INSERT INTO Sales
VALUES(1, 23456.0, "2021-12-22", "w"),
	  (2, 12365.0, "2021-09-09", "e"),
      (3, 23757.0, "2020-11-11", "e"),
      (4, 12549.0, "2020-12-12", "m"),
      (5, 39393.0, "2021-02-02", "w");
INSERT INTO sqlite_sequence
VALUES("Sales", 6);





