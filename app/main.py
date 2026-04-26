from os import getenv

from flask import Flask, render_template, request, redirect, flash
import random
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

app.secret_key = "restaurant_project_secret_key"

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PSWD"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT")
    )

@app.route("/")
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM staff")
    staff_list = cursor.fetchall()

    cursor.execute("SELECT * FROM reservation")
    reservation_list = cursor.fetchall()

    cursor.execute("SELECT * FROM customer_order")
    order_list = cursor.fetchall()

    cursor.execute("SELECT * FROM menu_item")
    menu_list = cursor.fetchall()

    cursor.execute("SELECT * FROM ingredient")
    ingredient_list = cursor.fetchall()

    cursor.execute("SELECT * FROM payment")
    payment_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        staff_list=staff_list,
        reservation_list=reservation_list,
        order_list=order_list,
        menu_list=menu_list,
        ingredient_list=ingredient_list,
        payment_list=payment_list
    )

@app.route("/add_staff", methods=["POST"])
def add_staff():
    staff_name = request.form["staff_name"]
    staff_address = request.form["staff_address"]
    staff_phone = request.form["staff_phone"]
    staff_email = request.form["staff_email"]
    staff_pay_rate = request.form["staff_pay_rate"]
    staff_role = request.form["staff_role"]

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO staff 
        (staff_name, staff_address, staff_phone, staff_email, staff_pay_rate, staff_role)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (staff_name, staff_address, staff_phone, staff_email, staff_pay_rate, staff_role)

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")

@app.route("/delete_staff/<int:staff_id>", methods=["POST"])
def delete_staff(staff_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM staff WHERE staff_id = %s", (staff_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")

@app.route("/update_staff/<int:staff_id>", methods=["POST"])
def update_staff(staff_id):
    staff_name = request.form["staff_name"]
    staff_address = request.form["staff_address"]
    staff_phone = request.form["staff_phone"]
    staff_email = request.form["staff_email"]
    staff_pay_rate = request.form["staff_pay_rate"]
    staff_role = request.form["staff_role"]

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE staff
        SET staff_name=%s,
            staff_address=%s,
            staff_phone=%s,
            staff_email=%s,
            staff_pay_rate=%s,
            staff_role=%s
        WHERE staff_id=%s
    """
    values = (staff_name, staff_address, staff_phone, staff_email, staff_pay_rate, staff_role, staff_id)

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")

@app.route("/customer/add_reservation", methods=["POST"])
def customer_add_reservation():
    customer_name = request.form["customer_name"]
    customer_phone = request.form["customer_phone"]
    customer_email = request.form["customer_email"]
    reservation_time = request.form["reservation_time"]
    party_size = request.form["party_size"]
    reservation_status = "Booked"

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO reservation
        (customer_name, customer_phone, customer_email, reservation_time, party_size, reservation_status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (customer_name, customer_phone, customer_email, reservation_time, party_size, reservation_status)

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    flash("Reservation booked successfully! The staff can now view it in the dashboard.")
    return redirect("/customer/reservation")


@app.route("/update_reservation/<int:reservation_id>", methods=["POST"])
def update_reservation(reservation_id):
    customer_name = request.form["customer_name"]
    customer_phone = request.form["customer_phone"]
    customer_email = request.form["customer_email"]
    reservation_time = request.form["reservation_time"]
    party_size = request.form["party_size"]
    reservation_status = request.form["reservation_status"]

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE reservation
        SET customer_name=%s,
            customer_phone=%s,
            customer_email=%s,
            reservation_time=%s,
            party_size=%s,
            reservation_status=%s
        WHERE reservation_id=%s
    """
    values = (
        customer_name,
        customer_phone,
        customer_email,
        reservation_time,
        party_size,
        reservation_status,
        reservation_id,
    )

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")


@app.route("/delete_reservation/<int:reservation_id>", methods=["POST"])
def delete_reservation(reservation_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM reservation WHERE reservation_id = %s", (reservation_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")

@app.route("/customer/add_order", methods=["POST"])
def customer_add_order():
    customer_name = request.form["customer_name"]
    customer_phone = request.form["customer_phone"]
    customer_email = request.form["customer_email"]

    selected_items = request.form.getlist("menu_items")

    if not selected_items:
        flash("Please select at least one menu item before placing your order.")
        return redirect("/customer/order")

    order_number = "ORD" + str(random.randint(10000, 99999))
    order_details = ", ".join(selected_items)
    order_status = "Open"

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO customer_order
        (customer_name, customer_phone, customer_email, order_number, order_details, order_status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (customer_name, customer_phone, customer_email, order_number, order_details, order_status)

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    flash("Order placed successfully! The staff can now view it in the dashboard.")
    return redirect("/customer/order")


@app.route("/update_order/<int:order_id>", methods=["POST"])
def update_order(order_id):
    customer_name = request.form["customer_name"]
    customer_phone = request.form["customer_phone"]
    customer_email = request.form["customer_email"]
    order_number = request.form["order_number"]
    order_details = request.form["order_details"]
    order_status = request.form["order_status"]

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE customer_order
        SET customer_name=%s,
            customer_phone=%s,
            customer_email=%s,
            order_number=%s,
            order_details=%s,
            order_status=%s
        WHERE order_id=%s
    """
    values = (
        customer_name,
        customer_phone,
        customer_email,
        order_number,
        order_details,
        order_status,
        order_id,
    )

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")


@app.route("/delete_order/<int:order_id>", methods=["POST"])
def delete_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM customer_order WHERE order_id = %s", (order_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")

@app.route("/add_menu_item", methods=["POST"])
def add_menu_item():
    menu_item_name = request.form["menu_item_name"]
    menu_item_price = request.form["menu_item_price"]
    menu_item_available = 1 if request.form.get("menu_item_available") == "Available" else 0

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO menu_item
        (menu_item_name, menu_item_price, menu_item_available)
        VALUES (%s, %s, %s)
    """
    values = (menu_item_name, menu_item_price, menu_item_available)

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")


@app.route("/update_menu_item/<int:menu_item_id>", methods=["POST"])
def update_menu_item(menu_item_id):
    menu_item_name = request.form["menu_item_name"]
    menu_item_price = request.form["menu_item_price"]
    menu_item_available = 1 if request.form.get("menu_item_available") == "Available" else 0

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE menu_item
        SET menu_item_name=%s,
            menu_item_price=%s,
            menu_item_available=%s
        WHERE menu_item_id=%s
    """
    values = (menu_item_name, menu_item_price, menu_item_available, menu_item_id)

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")


@app.route("/delete_menu_item/<int:menu_item_id>", methods=["POST"])
def delete_menu_item(menu_item_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM menu_item WHERE menu_item_id = %s", (menu_item_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")

@app.route("/add_ingredient", methods=["POST"])
def add_ingredient():
    ingredient_name = request.form["ingredient_name"]
    ingredient_unit = request.form["ingredient_unit"]
    ingredient_current_qty = request.form["ingredient_current_qty"]
    ingredient_reorder_level = request.form["ingredient_reorder_level"]

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO ingredient
        (ingredient_name, ingredient_unit, ingredient_current_qty, ingredient_reorder_level)
        VALUES (%s, %s, %s, %s)
    """
    values = (ingredient_name, ingredient_unit, ingredient_current_qty, ingredient_reorder_level)

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")


@app.route("/update_ingredient/<int:ingredient_id>", methods=["POST"])
def update_ingredient(ingredient_id):
    ingredient_name = request.form["ingredient_name"]
    ingredient_unit = request.form["ingredient_unit"]
    ingredient_current_qty = request.form["ingredient_current_qty"]
    ingredient_reorder_level = request.form["ingredient_reorder_level"]

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE ingredient
        SET ingredient_name=%s,
            ingredient_unit=%s,
            ingredient_current_qty=%s,
            ingredient_reorder_level=%s
        WHERE ingredient_id=%s
    """
    values = (
        ingredient_name,
        ingredient_unit,
        ingredient_current_qty,
        ingredient_reorder_level,
        ingredient_id,
    )

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")


@app.route("/delete_ingredient/<int:ingredient_id>", methods=["POST"])
def delete_ingredient(ingredient_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM ingredient WHERE ingredient_id = %s", (ingredient_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")

@app.route("/add_payment", methods=["POST"])
def add_payment():
    payment_type = request.form["payment_type"]
    payment_name = request.form["payment_name"]
    payment_amount = request.form["payment_amount"]
    payment_date = request.form["payment_date"]

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO payment
        (payment_type, payment_name, payment_amount, payment_date)
        VALUES (%s, %s, %s, %s)
    """
    values = (payment_type, payment_name, payment_amount, payment_date)

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")

@app.route("/customer")
def customer_home():
    return render_template("customer_home.html")


@app.route("/customer/menu")
def customer_menu():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM menu_item WHERE menu_item_available = 1")
    menu_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("customer_menu.html", menu_list=menu_list)


@app.route("/customer/reservation")
def customer_reservation():
    return render_template("customer_reservation.html")


@app.route("/customer/order")
def customer_order():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM menu_item WHERE menu_item_available = 1")
    menu_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("customer_order.html", menu_list=menu_list)

@app.route("/add_reservation", methods=["POST"])
def add_reservation():
    customer_name = request.form["customer_name"]
    customer_phone = request.form["customer_phone"]
    customer_email = request.form["customer_email"]
    reservation_time = request.form["reservation_time"]
    party_size = request.form["party_size"]
    reservation_status = request.form["reservation_status"]

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO reservation
        (customer_name, customer_phone, customer_email, reservation_time, party_size, reservation_status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (customer_name, customer_phone, customer_email, reservation_time, party_size, reservation_status)

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")

@app.route("/add_order", methods=["POST"])
def add_order():
    customer_name = request.form["customer_name"]
    customer_phone = request.form["customer_phone"]
    customer_email = request.form["customer_email"]
    order_number = request.form["order_number"]
    order_details = request.form["order_details"]
    order_status = request.form["order_status"]

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO customer_order
        (customer_name, customer_phone, customer_email, order_number, order_details, order_status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (customer_name, customer_phone, customer_email, order_number, order_details, order_status)

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)