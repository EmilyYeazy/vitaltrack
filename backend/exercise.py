import requests
import csv
import matplotlib.pyplot as plt
from datetime import datetime
from config import config
import os

NUTRITIONIX_APP_ID = config.NUTRITIONIX_APP_ID
NUTRITIONIX_API_KEY = config.NUTRITIONIX_API_KEY
EXERCISE_DB_FILE = config.EXERCISE_DB_FILE
EXERCISE_END_POINT = config.EXERCISE_END_POINT

def get_exercise_info(exercise_input):
    # Fetch exercise data from the Nutritionix API.
    try:
        response = requests.post(
            EXERCISE_END_POINT, 
            headers={'x-app-id': NUTRITIONIX_APP_ID, 'x-app-key': NUTRITIONIX_API_KEY}, 
            json={"query": exercise_input}
        )
        return response.json().get('exercises', [])
    except:
        print("Failed to fetch exercise data.")
        return []

def log_to_csv(username, exercise_input, exercises):
    """
    Log exercise data to CSV, associated with a specific user.
    """
    if exercises:
        file_path = "data/exercise_data.csv"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Open the file in append mode
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)

            # If the file is empty, write the header
            if file.tell() == 0:
                writer.writerow(["Date", "Exercise Input", "Exercise Name", "Calories Burned", "Username"])

            # Write the exercise data with the correct column order: Date, Exercise Input, Exercise Name, Calories, Username
            for exercise in exercises:
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Date
                    exercise_input,  # Exercise Input
                    exercise['name'],  # Exercise Name
                    exercise.get('nf_calories', 0),  # Calories Burned
                    username  # Username
                ])
        print(f"Exercise data logged for user {username}.")