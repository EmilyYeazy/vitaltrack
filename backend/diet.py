import requests
import csv
import matplotlib.pyplot as plt
from datetime import datetime
from config import Config

NUTRITIONIX_APP_ID = Config.NUTRITIONIX_APP_ID
NUTRITIONIX_API_KEY = Config.NUTRITIONIX_API_KEY
EXERCISE_DB_FILE = Config.NUTRITION_DB_FILE
EXERCISE_END_POINT = Config.NUTRITION_END_POINT

def get_food_info(food_item):
    # Get nutritional information for the given food item.
    url = f"https://api.nutritionix.com/v1_1/search/{food_item}?key={NUTRITION_API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()
        if 'hits' in data and data['hits']:
            food = data['hits'][0]['fields']
            return {
                'name': food['item_name'],
                'calories': food.get('nf_calories', 0),
                'carbs': food.get('nf_total_carbohydrate', 0),
                'protein': food.get('nf_protein', 0),
                'fats': food.get('nf_total_fat', 0)
            }
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def log_food(username, food_data):
    """Log food data to CSV, associated with the specific user."""
    if food_data:  # Check if food_data is not empty
        # Open the file in append mode
        with open("data/food_data.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            # Write the food data in a new row, including the username
            writer.writerow([
                username,  # User's username
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Current timestamp
                food_data['name'],  # Food name
                food_data['calories'],  # Calories
                food_data['carbs'],  # Carbs
                food_data['protein'],  # Protein
                food_data['fats']  # Fats
            ])
        print(f"Food data logged for user {username}.")

def visualize_food_data(username, save=False):
    """Visualize food data (calories) over time for a specific user."""
    dates = []
    calories = []

    # Open the CSV file and read it
    try:
        with open("data/food_data.csv", mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Assuming the username is in the first column, timestamp is second, and calories is third
                if row[0] == username:  # Check if the row corresponds to the user
                    dates.append(row[1])  # Timestamp
                    calories.append(int(row[3]))  # Calories

        # If we have data, plot it
        if dates and calories:
            plt.plot(dates, calories, marker='o', color='green')  # Simple line plot
            plt.xticks(rotation=45, fontsize=8)  # Rotate x-axis labels for readability
            plt.xlabel('Date and Time')  # Label x-axis
            plt.ylabel('Calories')  # Label y-axis
            plt.title(f'Calories Consumed Over Time for {username}')  # Title
            
            if save:
                # Create the directory for saving images if it doesn't exist
                save_dir = f"data/graph/{username}"
                os.makedirs(save_dir, exist_ok=True)
                plt.savefig(f"{save_dir}/food_data_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                print(f"Food graph saved for {username}.")
            else:
                plt.show()  # Show the plot

    except FileNotFoundError:
        print("Food data file not found.")  # Handle the case where the file doesn't exist

    except Exception as e:
        print(f"Error visualizing data: {e}")  # Catch any other errors