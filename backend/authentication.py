import csv

import csv

import csv

# Registration function
import csv

# Registration function
import csv

# Registration function
def register_user(username, password, height, weight, email):
    # Ensure no field is empty
    if not username or not password or not height or not weight or not email:
        print("Please fill in all fields!")
        return False

    # Check if height and weight are numeric
    try:
        height = float(height)
        weight = float(weight)
    except ValueError:
        print("Height and Weight must be numeric values.")
        return False

    # Open the data/user.csv file to check if the username already exists
    user_exists = False
    try:
        with open('data/user.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username:
                    user_exists = True
                    break  # Exit the loop early if user is found
    except FileNotFoundError:
        # If file does not exist, we can create it with headers
        print("File not found. Creating a new file.")

    if user_exists:
        print("User already exists!")
        return False  # Return False if user already exists

    # If user does not exist, append new user data to the CSV file
    with open('data/user.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Debugging: Print data before writing
        print(f"Writing to file: {username}, {password}, {email}, {height}, {weight}")
        writer.writerow([username, password, email, height, weight])

        print(f"User {username} registered successfully!")
        return True  # Return True if registration is successful

def login_user(username, password):
    # Open the data/user.csv file and check for the entered username and password
    with open('data/user.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            print(f"Checking: Username: '{row[0]}', Password: '{row[1]}'")  # Debugging line
            if row[0].strip() == username.strip() and row[1].strip() == password.strip():
                print(f"Login successful! Welcome {username}!")
                return True

    print("Invalid username or password!")
    return False

def update_user(username, new_height, new_weight):
    users_updated = False

    # Read current users' data from the CSV file
    with open('data/user.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        users = list(reader)

    # Search for the user and update height and weight
    for row in users:
        if row[0] == username:  # If the username matches
            row[3] = new_height  # Update height (index 3)
            row[4] = new_weight   # Update weight (index 4)
            users_updated = True
            break

    if users_updated:
        # Write updated data back to the CSV file
        with open('data/user.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(users)  # Save all user data with the update
        print(f"User {username}'s details updated successfully!")
        return True
    else:
        print(f"User {username} not found!")
        return False