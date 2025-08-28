DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS customers;

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE admins (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE customers (
    CustomerId INTEGER PRIMARY KEY,
    CreditScore INTEGER,
    Geography TEXT,
    Gender TEXT,
    Age INTEGER,
    Tenure INTEGER,
    Balance REAL,
    NumOfProducts INTEGER,
    HasCrCard INTEGER,
    IsActiveMember INTEGER,
    EstimatedSalary REAL,
    Exited INTEGER
);
