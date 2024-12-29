import requests
import csv
import matplotlib.pyplot as plt
from datetime import datetime
from config import NUTRITIONIX_APP_ID, NUTRITIONIX_API_KEY, EXERCISE_DB_FILE, EXERCISE_END_POINT

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
    # Log exercise data to a CSV file.
    try:
        # Open the file in append mode
        with open("exercise_data.csv", mode='a', newline='') as file:
            writer = csv.writer(file)  # Create a CSV writer object
            for exercise in exercises:
                # Write a single row of exercise data to the CSV
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Current date and time
                    username,                                      # User's name
                    exercise_input,                                # Raw input from the user
                    exercise['name'],                              # Name of the exercise
                    exercise.get('nf_calories', 0)                # Calories burned (default 0)
                ])
        print("Exercise data logged.")  # Confirm successful logging
    except Exception as e:
        print(f"Error: {e}")  # Print an error message if something goes wrong

import csv
import matplotlib.pyplot as plt

def visualize_exercise_data():
    # Simplified version: Visualize exercise data over time.
    try:
        data = list(csv.reader(open("exercise_data.csv", "r")))  # Read all data at once
        dates = [row[0] for row in data]  # Extract dates
        calories = [int(row[4]) for row in data]  # Extract calorie values as integers

        if dates and calories:
            plt.plot(dates, calories, marker='o')  # Plot data with markers
            plt.xticks(rotation=45, fontsize=8)  # Rotate x-axis labels
            plt.xlabel("Date and Time")
            plt.ylabel("Calories Burned")
            plt.title("Calories Burned Over Time")
            plt.tight_layout()
            plt.show()
        else:
            print("No data to visualize.")
    except FileNotFoundError:
        print("Exercise data file not found.")
    except Exception as e:
        print(f"Error: {e}")