import requests
import csv
import matplotlib.pyplot as plt
from datetime import datetime
from config import config
import os

NUTRITIONIX_APP_ID = config.NUTRITIONIX_APP_ID
NUTRITIONIX_API_KEY = config.NUTRITIONIX_API_KEY
NUTRITION_DB_FILE = config.NUTRITION_DB_FILE
NUTRITION_END_POINT = config.NUTRITION_END_POINT

def get_food_info(food_item):
    """
    Get nutritional information for the given food item using the Nutritionix API.
    """
    url = f"https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "query": food_item
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad HTTP response
        data = response.json()
        if 'foods' in data and len(data['foods']) > 0:
            food = data['foods'][0]
            return {
                'name': food['food_name'],
                'calories': food.get('nf_calories', 0),
                'carbs': food.get('nf_total_carbohydrate', 0),
                'protein': food.get('nf_protein', 0),
                'fats': food.get('nf_total_fat', 0)
            }
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching food data: {e}")
        return None


def log_food(username, food_data):
    """
    Log food data to CSV, associated with a specific user.
    """
    if food_data:
        file_path = "data/nutrition_data.csv"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Open the file in append mode
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)

            # If the file is empty, write the header
            if file.tell() == 0:
                writer.writerow(["Date", "Food", "Calories", "Carbs", "Protein", "Fats", "Username"])

            # Write the food data with the correct column order: Date, Food, Calories, Carbs, Protein, Fats, Username
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Date
                food_data['name'],  # Food
                food_data['calories'],  # Calories
                food_data['carbs'],  # Carbs
                food_data['protein'],  # Protein
                food_data['fats'],  # Fats
                username  # Username
            ])
        print(f"Food data logged for user {username}.")

def visualize_food_data(username, save=False):
    """
    Visualize food data (calories) over time for a specific user.
    """
    dates, calories = [], []

    try:
        with open("data/food_data.csv", mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username:
                    dates.append(row[1])
                    calories.append(float(row[3]))

        if dates and calories:
            plt.plot(dates, calories, marker='o', color='green')
            plt.xticks(rotation=45, fontsize=8)
            plt.xlabel('Date and Time')
            plt.ylabel('Calories')
            plt.title(f'Calories Consumed Over Time for {username}')

            if save:
                save_dir = f"data/graph/{username}"
                os.makedirs(save_dir, exist_ok=True)
                plt.savefig(f"{save_dir}/food_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                print(f"Graph saved for user {username}.")
            else:
                plt.show()

    except FileNotFoundError:
        print("Food data file not found.")
    except Exception as e:
        print(f"Error visualizing data: {e}")