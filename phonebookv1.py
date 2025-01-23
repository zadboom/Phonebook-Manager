import sqlite3
import os
import csv

# Database setup
db_name = "phonebook.db"

def initialize_db():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        name TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        email TEXT,
                        FOREIGN KEY (user_id) REFERENCES users (id))''')

    connection.commit()
    connection.close()

# User authentication
def register():
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        connection.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists. Please try again.")
    finally:
        connection.close()

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    connection.close()

    if user:
        print("Login successful!")
        return user[0]
    else:
        print("Invalid credentials. Please try again.")
        return None

# Contact management
def add_contact(user_id):
    name = input("Enter contact name: ")
    phone = input("Enter phone number: ")
    email = input("Enter email (optional): ")

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("INSERT INTO contacts (user_id, name, phone, email) VALUES (?, ?, ?, ?)", (user_id, name, phone, email))
    connection.commit()
    connection.close()

    print("Contact added successfully!")

def view_contacts(user_id):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("SELECT name, phone, email FROM contacts WHERE user_id = ?", (user_id,))
    contacts = cursor.fetchall()

    connection.close()

    if contacts:
        print("Your contacts:")
        for contact in contacts:
            print(f"Name: {contact[0]}, Phone: {contact[1]}, Email: {contact[2]}")
    else:
        print("No contacts found.")

def delete_contact(user_id):
    name = input("Enter the name of the contact to delete: ")

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM contacts WHERE user_id = ? AND name = ?", (user_id, name))
    connection.commit()
    connection.close()

    print("Contact deleted successfully!")

# Export contacts to CSV
def export_to_csv(user_id):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("SELECT name, phone, email FROM contacts WHERE user_id = ?", (user_id,))
    contacts = cursor.fetchall()

    connection.close()

    if contacts:
        file_name = f"user_{user_id}_contacts.csv"
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Phone", "Email"])
            writer.writerows(contacts)
        print(f"Contacts exported successfully to {file_name}!")
    else:
        print("No contacts to export.")

# Main application
def main():
    initialize_db()

    print("Welcome to the Phonebook App!")
    print("1. Register")
    print("2. Login")
    choice = input("Choose an option (1 or 2): ")

    if choice == "1":
        register()
    elif choice == "2":
        user_id = login()
        if user_id:
            while True:
                print("\nPhonebook Menu")
                print("1. Add Contact")
                print("2. View Contacts")
                print("3. Delete Contact")
                print("4. Export Contacts to CSV")
                print("5. Logout")
                option = input("Choose an option: ")

                if option == "1":
                    add_contact(user_id)
                elif option == "2":
                    view_contacts(user_id)
                elif option == "3":
                    delete_contact(user_id)
                elif option == "4":
                    export_to_csv(user_id)
                elif option == "5":
                    print("Logged out successfully. Goodbye!")
                    break
                else:
                    print("Invalid option. Please try again.")
    else:
        print("Invalid choice. Please restart the application.")

if __name__ == "__main__":
    main()
