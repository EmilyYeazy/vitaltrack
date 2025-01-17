import csv
from datetime import datetime

def register_user(username, password, height, weight):
    # Ensure no field is empty
    if not username or not password or not height or not weight:
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
    file_exists = True
    try:
        with open('data/user.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == username:
                    user_exists = True
                    break
    except FileNotFoundError:
        # If file does not exist, we can create it with headers
        print("File not found. Creating a new file.")
        file_exists = False

    if user_exists:
        print("User already exists!")
        return False 

    # If user does not exist, append new user data to the CSV file
    with open('data/user.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["username", "password", "height", "weight", "registration_date"])
        writer.writerow([username, password, height, weight, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

    print("Registration successful!")
    return True

def login_user(username, password):
    # Open the data/user.csv file and check for the entered username and password
    with open('data/user.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:  # Skip empty rows
                continue
            if row[0].strip().lower() == username.strip().lower() and row[1].strip() == password.strip():
                print(f"Login successful! Welcome {username}!")
                return True
    print("Invalid username or password!")
    return False

def update_settings(username, new_password):
    users_updated = False

    # Read current users' data from the CSV file
    try:
        with open('data/user.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            users = list(reader)
    except FileNotFoundError:
        print("Error: user.csv not found.")
        return False

    # Skip the header row when searching for the user
    header = users[0]
    user_rows = users[1:]

    # Update the password for all rows with the matching username
    for row in user_rows:
        if row[0] == username:
            row[1] = new_password
            users_updated = True

    if users_updated:
        # Write updated data back to the CSV file
        with open('data/user.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Write the header row first
            writer.writerows(user_rows)  # Save all user data with the updates
        print(f"Password updated for all occurrences of username '{username}'!")
        return True
    else:
        print(f"User {username} not found!")
        return False

def update_data(username, new_weight, new_height):
    users_updated = False

    # Read current users' data from the CSV file
    with open('data/user.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        users = list(reader)

    # Search for the user and update height and weight
    for row in users:
        if row[0] == username:
            row[3] = new_height
            row[4] = new_weight
            users_updated = True
            break

    if users_updated:
        # Append the updated user's data as a new line (username, password, email, height, weight, registration_date)
        with open('data/user.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([username, row[1], new_height, new_weight, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        return True
    else:
        return False