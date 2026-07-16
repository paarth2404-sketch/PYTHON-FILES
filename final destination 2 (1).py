import mysql.connector

# Function to create the database
def create_database_airline():
    try:
        mycon = mysql.connector.connect(host='localhost', user='root', password='BVM')
        cursor = mycon.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS airline")
        print("Database 'airline' created successfully!")
        mycon.close()
    except mysql.connector.Error as e:
        print(f"Error creating database: {e}")

# Function to establish a connection to the MySQL database
def connection():
    try:
        mycon = mysql.connector.connect(
            host='localhost', user='root', password='BVM', database='airline'
        )
        if mycon.is_connected():
            return mycon
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Function to create tables
def create_tables():
    try:
        mycon = connection()
        if mycon:
            cursor = mycon.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS airline_info (
                    name VARCHAR(100),
                    phno VARCHAR(15) PRIMARY KEY,
                    gender VARCHAR(50),
                    from_f VARCHAR(100),
                    to_t VARCHAR(100),
                    date_d VARCHAR(20),
                    price INT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_accounts (
                    fname VARCHAR(100),
                    lname VARCHAR(100),
                    user_name VARCHAR(100) PRIMARY KEY,
                    password VARCHAR(100),
                    phno VARCHAR(15),
                    gender VARCHAR(50),
                    dob VARCHAR(20)
                )
            """)
            print("Tables 'airline_info' and 'user_accounts' created successfully!")
            mycon.close()
    except mysql.connector.Error as e:
        print(f"Error creating tables: {e}")

# Function to handle user sign-up
def sign_up():
    try:
        mycon = connection()
        if mycon:
            cursor = mycon.cursor()
            fname = input("First Name: ")
            lname = input("Last Name: ")
            user_name = input("Username: ")
            password = input("Password: ")
            confirm_password = input("Re-enter Password: ")
            phno = input("Phone Number: ")
            print("Gender options: M=Male, F=Female, N=Not to Mention")
            gender = input("Enter your gender: ").upper()
            dob = input("Enter your Date of Birth (DD-MM-YYYY): ")

            # Validate password confirmation
            if password != confirm_password:
                print("Passwords do not match!")
                return False

            # Normalize gender input
            valid_genders = {"M": "Male", "F": "Female", "N": "Not to Mention"}
            gender = valid_genders.get(gender, "Not to Mention")

            # Insert user details into the database
            query = """
            INSERT INTO user_accounts (fname, lname, user_name, password, phno, gender, dob)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (fname, lname, user_name, password, phno, gender, dob))
            mycon.commit()
            print(f"Welcome, {fname} {lname}! Your account has been created.")
            mycon.close()
            return True
    except mysql.connector.Error as e:
        print(f"Error signing up: {e}")
        return False

# Function to handle user sign-in
def sign_in():
    try:
        mycon = connection()
        if mycon:
            cursor = mycon.cursor()
            user_name = input("Username: ")
            password = input("Password: ")

            # Query to fetch user details
            query = "SELECT fname, lname FROM user_accounts WHERE user_name = %s AND password = %s"
            cursor.execute(query, (user_name, password))
            user_data = cursor.fetchone()

            if user_data:
                fname, lname = user_data
                print(f"Welcome back, {fname} {lname}!")
                return True
            else:
                print("Invalid username or password.")
            mycon.close()
            return False
    except mysql.connector.Error as e:
        print(f"Error signing in: {e}")
        return False

# Function to book a ticket
def ticket_booking():
    try:
        mycon = connection()
        if mycon:
            cursor = mycon.cursor()
            name = input("Enter your name: ")
            phno = input("Enter your phone number: ")
            print("Gender options: M=Male, F=Female, N=Not to Mention")
            gender = input("Enter your gender: ").upper()
            from_f = input("Enter your starting point: ")
            to_t = input("Enter your destination: ")
            date = input("Enter the travel date (DD/MM/YYYY): ")

            # Set the price to 1500
            price_per_ticket = 1500

            # Ask for the number of tickets
            num_tickets = int(input("Enter the number of tickets you want to book: "))

            # Calculate the total price
            total_price = price_per_ticket * num_tickets
            print(f"Total price for {num_tickets} tickets: Rs. {total_price}")

            # Normalize gender input
            valid_genders = {"M": "Male", "F": "Female", "N": "Not to Mention"}
            gender = valid_genders.get(gender, "Not to Mention")

            # Insert ticket details into the database
            query = """
            INSERT INTO airline_info (name, phno, gender, from_f, to_t, date_d, price)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            for _ in range(num_tickets):  # Insert the number of tickets into the database
                cursor.execute(query, (name, phno, gender, from_f, to_t, date, price_per_ticket))

            mycon.commit()
            print(f"{num_tickets} ticket(s) booked successfully!")
    except mysql.connector.Error as e:
        print(f"Error booking ticket: {e}")
    finally:
        if mycon:
            mycon.close()

# Function to check a booked ticket
def ticket_checking():
    try:
        mycon = connection()
        if mycon:
            cursor = mycon.cursor()
            phno = input("Enter your phone number: ")
            query = "SELECT * FROM airline_info WHERE phno = %s"
            cursor.execute(query, (phno,))
            ticket = cursor.fetchone()

            if ticket:
                fields = ["Name", "Phone Number", "Gender", "From", "To", "Date", "Price"]
                for field, value in zip(fields, ticket):
                    print(f"{field}: {value}")
            else:
                print("No ticket found for the given phone number.")
            mycon.close()
    except mysql.connector.Error as e:
        print(f"Error checking ticket: {e}")

# Function to cancel a ticket
def ticket_cancelling():
    try:
        mycon = connection()
        if mycon:
            cursor = mycon.cursor()
            phno = input("Enter your phone number: ")
            query = "SELECT * FROM airline_info WHERE phno = %s"
            cursor.execute(query, (phno,))
            ticket = cursor.fetchone()

            if ticket:
                query = "DELETE FROM airline_info WHERE phno = %s"
                cursor.execute(query, (phno,))
                mycon.commit()
                print("Ticket cancelled successfully!")
            else:
                print("No ticket found for cancellation.")
            mycon.close()
    except mysql.connector.Error as e:
        print(f"Error cancelling ticket: {e}")

# Function to calculate the total price of all tickets booked by a user
def check_total_price():
    try:
        mycon = connection()
        if mycon:
            cursor = mycon.cursor()
            phno = input("Enter your phone number to check total ticket price: ")
            
            # Query to sum up the ticket prices for the given phone number
            query = "SELECT SUM(price) FROM airline_info WHERE phno = %s"
            cursor.execute(query, (phno,))
            total_price = cursor.fetchone()[0]

            if total_price is None:
                print("No tickets found for the given phone number.")
            else:
                print(f"The total price of all tickets booked: Rs. {total_price}")
            mycon.close()
    except mysql.connector.Error as e:
        print(f"Error checking total price: {e}")

# Main menu
def menu():
    while True:
        print("=" * 50)
        print("WELCOME TO THE AIRLINE RESERVATION SYSTEM")
        print("=" * 50)
        print("1. Sign Up")
        print("2. Sign In")
        print("3. Book Ticket")
        print("4. Check Ticket")
        print("5. Cancel Ticket")
        print("6. Check Total Price of Tickets")
        print("7. Exit")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            sign_up()
        elif choice == "2":
            if sign_in():
                print("Sign-in successful!")
        elif choice == "3":
            ticket_booking()
        elif choice == "4":
            ticket_checking()
        elif choice == "5":
            ticket_cancelling()
        elif choice == "6":
            check_total_price()
        elif choice == "7":
            print("Thank you for using the Airline Reservation System! Goodbye.")
            break
        else:
            print("Invalid choice. Please try again.")

# Initialize the database and tables, then run the menu
create_database_airline()
create_tables()
menu()
