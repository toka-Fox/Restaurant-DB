# Set up the MySQL database here
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def init_restaurantdb():
    try:
        conn = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PSWD")
        )

        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv("DB_NAME")}")
        cursor.execute(f"USE {os.getenv("DB_NAME")}")

        tables = {
            "Staff": "CREATE TABLE IF NOT EXISTS Staff (Emp_ID INT PRIMARY KEY AUTO_INCREMENT, Emp_fName VARCHAR(15), Emp_lName VARCHAR(20), Emp_Role VARCHAR(20), Emp_Phone INT, Emp_Email VARCHAR(25), Emp_Address VARCHAR(40), Emp_HourlyRate DECIMAL(5,2), Emp_IsActive BOOL DEFAULT 1)",
            "Customer": "CREATE TABLE IF NOT EXISTS Customer (Ctmr_ID INT PRIMARY KEY AUTO_INCREMENT, Ctmr_fName VARCHAR(15), Ctmr_lName VARCHAR(20), Ctmr_Phone INT, Ctmr_Email VARCHAR(25))",
            "Tables": "CREATE TABLE IF NOT EXISTS Tables (Table_ID INT PRIMARY KEY AUTO_INCREMENT, Table_Capacity INT, Table_Status VARCHAR(10) DEFAULT 'EMPTY')",
            "Assignment": "CREATE TABLE IF NOT EXISTS Assignment (Assignment_ID INT PRIMARY KEY AUTO_INCREMENT, Table_ID INT, Emp_ID INT, FOREIGN KEY (Table_ID) REFERENCES Tables(Table_ID), FOREIGN KEY (Emp_ID) REFERENCES Staff(Emp_ID))",
            "Reservation": "CREATE TABLE IF NOT EXISTS Reservation (Resv_ID INT PRIMARY KEY AUTO_INCREMENT, Ctmr_ID INT, Table_ID INT, Resv_DateTime DATETIME, Resv_Size INT, Resv_Status VARCHAR(10) DEFAULT 'Active', FOREIGN KEY (Ctmr_ID) REFERENCES Customer(Ctmr_ID), FOREIGN KEY (Table_ID) REFERENCES Tables(Table_ID))",
            "Orders": "CREATE TABLE IF NOT EXISTS Orders (Order_ID INT PRIMARY KEY AUTO_INCREMENT, Ctmr_ID INT, Table_ID INT, Emp_ID INT, Order_Type VARCHAR(10) DEFAULT 'HERE', Order_Status VARCHAR(10) DEFAULT 'Pending', FOREIGN KEY (Ctmr_ID) REFERENCES Customer(Ctmr_ID), FOREIGN KEY (Table_ID) REFERENCES Tables(Table_ID), FOREIGN KEY (Emp_ID) REFERENCES Staff(Emp_ID))",
            "Stock": "CREATE TABLE IF NOT EXISTS Ingredient (Stock_ID INT PRIMARY KEY AUTO_INCREMENT, Stock_Name VARCHAR(20), Stock_Amount INT)",
            "Category": "CREATE TABLE IF NOT EXISTS Category (Cat_ID INT PRIMARY KEY AUTO_INCREMENT, Cat_Name VARCHAR(20))",
            "Menu": "CREATE TABLE IF NOT EXISTS Menu (Menu_ItemID INT PRIMARY KEY AUTO_INCREMENT, Menu_ItemName VARCHAR(20), Cat_ID INT, Menu_ItemDesc VARCHAR(100), Menu_ItemPrice DECIMAL(5,2), FOREIGN KEY (Cat_ID) REFERENCES Category(Cat_ID))",
            "Payment": "CREATE TABLE IF NOT EXISTS Payment (Pay_ID INT PRIMARY KEY AUTO_INCREMENT, Order_ID INT, Pay_Due DECIMAL(7,2), Pay_Tip DECIMAL(5,2) DEFAULT (Pay_Due * 0.20), Pay_Method VARCHAR(10), FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID))"
        }

        for name, dbc in tables.items():
            cursor.execute(dbc)
            print(f"{name} table verified.")

        conn.commit()
        print("Database finished.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    init_restaurantdb()
