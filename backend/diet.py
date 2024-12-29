import requests
import csv
import matplotlib.pyplot as plt
from datetime import datetime
from config import NUTRITION_API_KEY

import requests

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

def log_food(food_data):
    # Log food data to CSV.
    if food_data:  # Check if food_data is not empty
        # Open the file in append mode
        with open("data/food_data.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            # Write the food data in a new row
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Current timestamp
                food_data['name'],  # Food name
                food_data['calories'],  # Calories
                food_data['carbs'],  # Carbs
                food_data['protein'],  # Protein
                food_data['fats']  # Fats
            ])
        print("Food data logged.")

def visualize_food_data():
    """Visualize food data (calories) over time."""
    dates = []
    calories = []

    # Open the CSV file and read it
    try:
        with open("data/food_data.csv", mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Assuming the timestamp is in the first column and calories are in the third column
                dates.append(row[0])  # Timestamp
                calories.append(int(row[2]))  # Calories

        # If we have data, plot it
        if dates and calories:
            plt.plot(dates, calories, marker='o', color='green')  # Simple line plot
            plt.xticks(rotation=45, fontsize=8)  # Rotate x-axis labels for readability
            plt.xlabel('Date and Time')  # Label x-axis
            plt.ylabel('Calories')  # Label y-axis
            plt.title('Calories Consumed Over Time')  # Title
            plt.show()  # Show the plot

        else:
            print("No data to visualize.")  # No data available

    except FileNotFoundError:
        print("Food data file not found.")  # Handle the case where the file doesn't exist

    except Exception as e:
        print(f"Error visualizing data: {e}")  # Catch any other errors