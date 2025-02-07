CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Email VARCHAR(100),
    DateOfBirth DATE,
    RegistrationDate TIMESTAMP
);

INSERT INTO Customers (CustomerID, FirstName, LastName, Email, DateOfBirth, RegistrationDate)
VALUES
(1, 'John', 'Doe', 'john.doe@example.com', '1985-07-12', '2023-01-15 08:00:00'),
(2, 'Jane', 'Smith', 'jane.smith@example.com', '1990-03-24', '2023-01-18 09:30:00'),
(3, 'Emily', 'Jones', 'emily.jones@example.com', '1982-06-30', '2023-02-20 14:22:00'),
(4, 'Michael', 'Brown', 'michael.brown@example.com', '1975-11-05', '2023-03-02 16:00:00'),
(5, 'Sarah', 'White', 'sarah.white@example.com', '1995-12-15', '2023-04-10 10:45:00');

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate TIMESTAMP,
    OrderAmount DECIMAL(10, 2),
    Status VARCHAR(50),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

INSERT INTO Orders (OrderID, CustomerID, OrderDate, OrderAmount, Status)
VALUES
(1, 1, '2023-01-20 10:00:00', 150.00, 'Completed'),
(2, 2, '2023-02-25 11:30:00', 250.00, 'Pending'),
(3, 3, '2023-03-05 15:45:00', 100.00, 'Shipped'),
(4, 1, '2023-04-10 12:00:00', 200.00, 'Cancelled'),
(5, 4, '2023-05-15 09:15:00', 450.00, 'Completed');

CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(100),
    Price DECIMAL(10, 2)
);

INSERT INTO Products (ProductID, ProductName, Category, Price)
VALUES
(1, 'Laptop', 'Electronics', 1200.00),
(2, 'Smartphone', 'Electronics', 800.00),
(3, 'T-shirt', 'Clothing', 25.00),
(4, 'Coffee Maker', 'Appliances', 150.00),
(5, 'Headphones', 'Electronics', 100.00);