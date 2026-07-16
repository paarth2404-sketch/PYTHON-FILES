import mysql.connector
import datetime

# Connect to the MySQL database
try:
    connect = mysql.connector.connect(host='localhost', user='root', password='admin', database='Meddata')
    cursor = connect.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

# Function to add record in MySQL database
def AddMeddata():
    mnum = int(input('Enter Medicine Number: '))
    name = input("Enter Medicine Name: ")
    typ = input("Enter Medicine Type: ")
    qty = int(input("Enter Quantity: "))
    price = int(input('Enter Price: '))
    exp = input("Enter Expiry date (yyyy-mm-dd): ")
    total = price * qty
    
    detail = (mnum, name, typ, qty, price, total, exp)
    insert = """INSERT INTO Medicine (sno, medicine, typ, quantity, price, total, exp) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(insert, detail)
    connect.commit()
    print("Record inserted successfully into the table.")

# Function to display records
def DisplayMeddata():
    select = "SELECT * FROM Medicine"
    cursor.execute(select)
    rec = cursor.fetchall()
    print('Sr. No.', "\t", "Name", "\t", "Type", "\t", "Quantity", "\t", "Price", "\t", "Total", "\t", "Expiry")
    for row in rec:
        print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[6]}")

# Function to delete a record
def DeleteMeddata():
    name = input("Enter the medicine name to be deleted: ")
    detail = (name,)
    delete = "DELETE FROM Medicine WHERE medicine = %s"
    cursor.execute(delete, detail)
    if cursor.rowcount > 0:
        connect.commit()
        print("Record deleted successfully from the table.")
    else:
        print(f"No medicine found with the name '{name}'.")

# Function to update a record
def UpdateMeddata():
    ans = 'y'
    while ans == 'y':
        print("==========Sub Menu==========")
        print("1) Price")
        print("2) Quantity")
        print("3) Name of the Medicine")
        print("========================================================================")
        ch = int(input("Enter your choice: "))
        name = input("Enter the medicine name: ")
        
        if ch == 1:  # Update price
            p = int(input("Enter the new price of medicine: "))
            detail = (p, name)
            update = "UPDATE Medicine SET price = %s WHERE medicine = %s"
            cursor.execute(update, detail)
            if cursor.rowcount > 0:
                connect.commit()
                print("Price updated successfully.")
            else:
                print(f"No medicine found with the name '{name}'.")

        elif ch == 2:  # Update quantity
            q = int(input("Enter the new quantity of medicine: "))
            detail2 = (q, name)
            update = "UPDATE Medicine SET quantity = %s WHERE medicine = %s"
            cursor.execute(update, detail2)
            if cursor.rowcount > 0:
                connect.commit()
                print("Quantity updated successfully.")
            else:
                print(f"No medicine found with the name '{name}'.")

        elif ch == 3:  # Update name
            name2 = input("Enter the new name of medicine: ")
            detail = (name2, name)
            update = "UPDATE Medicine SET medicine = %s WHERE medicine = %s"
            cursor.execute(update, detail)
            if cursor.rowcount > 0:
                connect.commit()
                print("Name updated successfully.")
            else:
                print(f"No medicine found with the name '{name}'.")

        ans2 = input("Do you want to edit more records? (y/n): ")
        if ans2 != 'y':
            break
    print("Record updated successfully into the table.")

# Function to check expired medicines
def exp_Meddata():
    exp_date_str = input('Enter the date to check expiry (YYYY-MM-DD): ')

    try:
        exp_date_obj = datetime.datetime.strptime(exp_date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    query = 'SELECT * FROM Medicine WHERE exp <= %s'
    cursor.execute(query, (exp_date_obj,))
    records = cursor.fetchall()
    
    if not records:
        print("No expired medicines found.")
    else:
        print('Sr. No.', "\t", 'Name', "\t", "Type", "\t", "Quantity", "\t", "Price", "\t", "Total", "\t", "Expiry")
        for row in records:
            print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[6]}")

# Function to search for a medicine by name
def SearchMeddata():
    # Prompt user for medicine name
    name = input("Enter the medicine name to search for: ")

    # Query to search for medicine by name
    search_query = "SELECT * FROM Medicine WHERE medicine LIKE %s"
    search_value = ("%"+name+"%",)  # Using LIKE for partial matches (case insensitive)

    try:
        cursor.execute(search_query, search_value)
        records = cursor.fetchall()

        if records:
            # Displaying the search results
            print('Sr. No.', "\t", 'Name', "\t", 'Type', "\t", 'Quantity', "\t", 'Price', "\t", 'Total', "\t", 'Expiry')
            for row in records:
                print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[6]}")
        else:
            print(f"No records found for '{name}'.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to sell medicine
def SellMeddata():
    # Prompt the user to enter the medicine details
    name = input("Enter the medicine name to sell: ")
    qty_to_sell = int(input("Enter the quantity to sell: "))
    
    # Check if the medicine exists and get its current stock and price
    query = "SELECT sno, medicine, price, quantity FROM Medicine WHERE medicine = %s"
    cursor.execute(query, (name,))
    medicine = cursor.fetchone()

    if medicine:
        medicine_id, medicine_name, price_per_unit, current_qty = medicine
        if qty_to_sell <= current_qty:
            # Calculate the total sale amount
            total_amount = price_per_unit * qty_to_sell
            sale_date = datetime.datetime.now()

            # Insert the sale into the Sales table
            sale_query = """INSERT INTO Sales (medicine_id, medicine_name, quantity, price_per_unit, total_amount, sale_date)
                            VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sale_query, (medicine_id, medicine_name, qty_to_sell, price_per_unit, total_amount, sale_date))

            # Update the stock in the Medicine table
            new_qty = current_qty - qty_to_sell
            update_query = "UPDATE Medicine SET quantity = %s WHERE sno = %s"
            cursor.execute(update_query, (new_qty, medicine_id))

            connect.commit()
            print(f"Sale successful! Total sale amount: {total_amount}.")

        else:
            print("Insufficient stock to sell the requested quantity.")
    else:
        print(f"No medicine found with the name '{name}'.")

# Main menu loop
while True:
    print("""
          1) ADD MEDICINE
          2) DETAILS OF STOCK
          3) DELETE MEDICINE
          4) EDIT MEDICINE DETAILS
          5) Show expired medicine
          6) SEARCH MEDICINE BY NAME
          7) SELL MEDICINE
          8) EXIT
          """)
    try:
        choice = int(input("Enter your choice: "))
        if choice not in [1, 2, 3, 4, 5, 6, 7, 8]:
            print("Invalid choice! Please choose a valid option between 1 and 8.")
            continue
    except ValueError:
        print("Invalid input! Please enter a number between 1 and 8.")
        continue

    if choice == 1:
        AddMeddata()
    elif choice == 2:
        DisplayMeddata()
    elif choice == 3:
        DeleteMeddata()
    elif choice == 4:
        UpdateMeddata()
    elif choice == 5:
        exp_Meddata()
    elif choice == 6:
        SearchMeddata()  # Calling the SearchMeddata function
    elif choice == 7:
        SellMeddata()  # Selling medicine functionality
    elif choice == 8:
        print("Thank you for using our program.")
        break  # Exit the loop and terminate the program

    # Prompt user to continue or exit
    ans = input("Do you want to continue? (y/n): ").lower()
    if ans != 'y':
        print("Exiting the program. Thank you for using it!")
        break  # Exit the loop if user doesn't want to continue
