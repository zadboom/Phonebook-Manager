import json
import csv
import re


# Load users
def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Save users
def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)


# User authentication
def authenticate_user():
    users = load_users()
    print("Welcome to the Phonebook Manager")
    while True:
        print("1. Login")
        print("2. Register")
        choice = input("Enter your choice (1/2): ").strip()

        if choice == "1":
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            if username in users and users[username] == password:
                print(f"Login successful! Welcome, {username}.")
                return username
            else:
                print("Invalid username or password. Try again.")

        elif choice == "2":
            username = input("Enter a new username: ").strip()
            if username in users:
                print("Username already exists. Try logging in.")
                continue

            password = input("Enter a new password: ").strip()
            users[username] = password
            save_users(users)
            print("Registration successful! You can now log in.")
        else:
            print("Invalid choice. Please select 1 or 2.")


# Load contacts specific to a user
def load_contacts(username):
    try:
        with open(f"{username}_contacts.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Save contacts specific to a user
def save_contacts(username, contacts):
    with open(f"{username}_contacts.json", "w") as file:
        json.dump(contacts, file, indent=4)


# Validate phone numbers (only digits)
def validate_phone_number(phone_number):
    if not phone_number.isdigit():
        print("Error: Phone number should contain only digits.")
        return False
    return True


# Validate email format
def validate_email(email):
    if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Error: Invalid email format.")
        return False
    return True


# Add a new contact
def add_contact(contacts):
    name = input("Enter the contact's name: ").strip()
    if name in contacts:
        print(f"A contact named '{name}' already exists.")
        return

    phone_number = input("Enter the contact's phone number: ").strip()
    if not validate_phone_number(phone_number):
        return

    email = input("Enter the contact's email (optional): ").strip()
    if not validate_email(email):
        return

    contacts[name] = {"Phone": phone_number, "Email": email}
    print(f"Contact '{name}' added successfully!")


# Advanced search
def search_contact(contacts):
    print("Advanced Search Options:")
    print("1. Search by Name")
    print("2. Search by Phone Number")
    print("3. Search by Email")

    choice = input("Enter your choice (1/2/3): ").strip()

    if choice == "1":
        name_query = input("Enter the name to search for (partial or full): ").strip().lower()
        results = {name: details for name, details in contacts.items() if name_query in name.lower()}
    elif choice == "2":
        phone_query = input("Enter the phone number to search for: ").strip()
        results = {name: details for name, details in contacts.items() if details["Phone"] == phone_query}
    elif choice == "3":
        email_query = input("Enter the email to search for: ").strip().lower()
        results = {name: details for name, details in contacts.items() if details["Email"].lower() == email_query}
    else:
        print("Invalid choice. Returning to main menu.")
        return

    if results:
        print("Search Results:")
        for name, details in results.items():
            print(f"Name: {name}, Phone: {details['Phone']}, Email: {details['Email']}")
    else:
        print("No contacts found matching the query.")


# Delete a contact
def delete_contact(contacts):
    name = input("Enter the name of the contact to delete: ").strip()
    if name in contacts:
        del contacts[name]
        print(f"Contact '{name}' deleted successfully!")
    else:
        print(f"No contact found with the name '{name}'.")


# Display all contacts
def display_all_contacts(contacts):
    if not contacts:
        print("No contacts found.")
        return

    print("All Contacts:")
    for name, details in contacts.items():
        print(f"Name: {name}")
        print(f"  Phone: {details['Phone']}")
        print(f"  Email: {details['Email']}")
        print("-" * 30)


# Export contacts to a CSV file
def export_to_csv(username, contacts):
    if not contacts:
        print("No contacts to export.")
        return

    with open(f"{username}_contacts.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Phone", "Email"])
        for name, details in contacts.items():
            writer.writerow([name, details["Phone"], details["Email"]])
    print(f"Contacts exported successfully to '{username}_contacts.csv'.")


# Main menu
def phonebook_manager():
    username = authenticate_user()
    contacts = load_contacts(username)

    while True:
        print("\nPhonebook Manager")
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Delete Contact")
        print("4. Display All Contacts")
        print("5. Export Contacts to CSV")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            search_contact(contacts)
        elif choice == "3":
            delete_contact(contacts)
        elif choice == "4":
            display_all_contacts(contacts)
        elif choice == "5":
            export_to_csv(username, contacts)
        elif choice == "6":
            save_contacts(username, contacts)
            print("Exiting the Phonebook Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


# Run the phonebook manager
if __name__ == "__main__":
    phonebook_manager()
