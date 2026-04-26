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
            "Staff": "CREATE TABLE IF NOT EXISTS Staff (staff_id INT AUTO_INCREMENT PRIMARY KEY, staff_name VARCHAR(100), staff_address VARCHAR(150), staff_phone VARCHAR(20), staff_email VARCHAR(100), staff_pay_rate DECIMAL(10,2), staff_role VARCHAR(50))",
            "Ingredient": "CREATE TABLE IF NOT EXISTS Ingredients (ingredient_id INT AUTO_INCREMENT PRIMARY KEY, ingredient_name VARCHAR(60), ingredient_unit VARCHAR(20), ingredient_current_qty DECIMAL(10,2), ingredient_reorder_level DECIMAL(10,2))",
            "Menu_Item": "CREATE TABLE IF NOT EXISTS Menu_Item (menu_item_id INT AUTO_INCREMENT PRIMARY KEY, menu_item_name VARCHAR(80), menu_item_price DECIMAL(8,2), menu_item_available BOOLEAN)",
            "Customer_Order": "CREATE TABLE IF NOT EXISTS Customer_Order (order_id INT AUTO_INCREMENT PRIMARY KEY, customer_name VARCHAR(100), customer_phone VARCHAR(20), customer_email VARCHAR(100), order_number VARCHAR(30), order_details TEXT, order_status VARCHAR(30))",
            "Reservation": "CREATE TABLE IF NOT EXISTS Reservation (reservation_id INT AUTO_INCREMENT PRIMARY KEY, customer_name VARCHAR(100), customer_phone VARCHAR(20), customer_email VARCHAR(100), reservation_time VARCHAR(50), party_size INT, reservation_status VARCHAR(30))",
            "Payment": "CREATE TABLE IF NOT EXISTS Payment (payment_id INT AUTO_INCREMENT PRIMARY KEY, payment_type VARCHAR(30), payment_name VARCHAR(100), payment_amount DECIMAL(10,2), payment_date VARCHAR(30))"
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
