import requests
import csv
import matplotlib.pyplot as plt
from datetime import datetime
from config import config

NUTRITIONIX_APP_ID = Config.NUTRITIONIX_APP_ID
NUTRITIONIX_API_KEY = Config.NUTRITIONIX_API_KEY
EXERCISE_DB_FILE = Config.EXERCISE_DB_FILE
EXERCISE_END_POINT = Config.EXERCISE_END_POINT

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
    # Log exercise data to a CSV file, associating it with the username.
    try:
        # Open the file in append mode with open("data/exercise_data.csv", mode='a', newline='') as file:
            writer = csv.writer(file)  # Create a CSV writer object
            for exercise in exercises:
                # Write a single row of exercise data to the CSV
                writer.writerow([
                    username,                                      # User's name
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Current date and time
                    exercise_input,                                # Raw input from the user
                    exercise['name'],                              # Name of the exercise
                    exercise.get('nf_calories', 0)                 # Calories burned (default 0)
                ])
        print(f"Exercise data logged for user {username}.")  # Confirm successful logging
    except Exception as e:
        print(f"Error: {e}")  # Print an error message if something goes wrong

def visualize_exercise_data(username):
    """Visualize exercise data (calories burned) over time for a specific user."""
    dates = []
    calories = []

    try:
        # Read all the data from the CSV file
        with open("data/exercise_data.csv", mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username:  # Only process data for the specific user
                    dates.append(row[1])  # Timestamp
                    calories.append(int(row[4]))  # Calories burned

        # If we have data, plot it
        if dates and calories:
            plt.plot(dates, calories, marker='o', color='blue')  # Simple line plot
            plt.xticks(rotation=45, fontsize=8)  # Rotate x-axis labels
            plt.xlabel('Date and Time')  # Label x-axis
            plt.ylabel('Calories Burned')  # Label y-axis
            plt.title(f'Calories Burned Over Time for {username}')  # Title
            plt.tight_layout()  # Adjust the layout to fit labels
            plt.show()  # Show the plot
        else:
            print(f"No exercise data available for user {username}.")  # No data available for the user

    except FileNotFoundError:
        print("Exercise data file not found.")
    except Exception as e:
        print(f"Error: {e}")