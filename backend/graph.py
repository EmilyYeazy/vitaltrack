import matplotlib.pyplot as plt
import pandas as pd
import csv, logging
from datetime import datetime

matplotlib_logger = logging.getLogger('matplotlib')
matplotlib_logger.setLevel(logging.WARNING)

plt.rcParams['font.family'] = 'Arial'

def load_data_from_csv(username):
    # Load nutrition data
    nutrition_data = pd.read_csv('data/nutrition_data.csv')
    nutrition_data = nutrition_data[nutrition_data['Username'].str.strip().str.lower() == username.strip().lower()]

    # Load exercise data
    exercise_data = pd.read_csv('data/exercise_data.csv')
    exercise_data = exercise_data[exercise_data['Username'].str.strip().str.lower() == username.strip().lower()]

    # Clean and process exercise data
    exercise_data.columns = exercise_data.columns.str.strip()
    exercise_data['Calories Burned'] = pd.to_numeric(exercise_data['Calories Burned'], errors='coerce')

    # Get height and weight from the user.csv file
    try:
        user_data = pd.read_csv('data/user.csv')  # Load the user.csv file
        user_data = user_data[user_data['username'].str.strip().str.lower() == username.strip().lower()] 
        weight_data = user_data[['registration_date', 'weight']] if not user_data.empty else None
        height_data = user_data[['registration_date', 'height']] if not user_data.empty else None
    except FileNotFoundError:
        weight_data, height_data = None, None

    return nutrition_data, exercise_data, height_data, weight_data

def plot_calories(username, nutrition_data, exercise_data):
    # Ensure correct column names exist in the DataFrames
    if 'Date' not in nutrition_data.columns or 'Calories' not in nutrition_data.columns:
        print("Error: Nutrition data is missing required columns.")
        return None

    if 'Date' not in exercise_data.columns or 'Calories Burned' not in exercise_data.columns:
        print("Error: Exercise data is missing required columns.")
        return None

    # Filter data for the specific user
    user_nutrition_data = nutrition_data[nutrition_data['Username'] == username]
    user_exercise_data = exercise_data[exercise_data['Username'] == username]

    if user_nutrition_data.empty and user_exercise_data.empty:
        print(f"No data available for {username}.")
        return None

    # Convert 'Date' column to datetime and strip the time part
    user_nutrition_data['Date'] = pd.to_datetime(user_nutrition_data['Date']).dt.date
    user_exercise_data['Date'] = pd.to_datetime(user_exercise_data['Date']).dt.date

    # Group and aggregate data by date
    user_nutrition_data_grouped = user_nutrition_data.groupby('Date')['Calories'].sum()
    user_exercise_data_grouped = user_exercise_data.groupby('Date')['Calories Burned'].sum()

    # Combine both datasets into a single DataFrame
    combined_data = pd.DataFrame({
        'Calories Consumed': user_nutrition_data_grouped,
        'Calories Burned': user_exercise_data_grouped
    }).fillna(0)

    plt.figure(figsize=(10, 6))
    plt.plot(combined_data.index, combined_data['Calories Consumed'], label="Calories Consumed", color="blue", marker="o")
    plt.plot(combined_data.index, combined_data['Calories Burned'], label="Calories Burned", color="red", marker="o")

    plt.title(f"Calories Consumed vs. Burned for {username}", fontsize=14)
    plt.xlabel("Date")
    plt.ylabel("Calories")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show the plot
    plt.show()

def plot_micronutrient_distribution(nutrition_data, username=None):
    # Check for username
    if username:
        user_nutrition_data = nutrition_data[nutrition_data['Username'] == username]
    else:
        user_nutrition_data = nutrition_data

    # Check for nutrition data
    if user_nutrition_data.empty:
        print(f"No nutrition data available for {username if username else 'the user'}.")
        return

    if 'Carbs' not in user_nutrition_data.columns or 'Protein' not in user_nutrition_data.columns or 'Fats' not in user_nutrition_data.columns:
        print("Error: Missing macronutrient columns.")
        return

    total_carbs = user_nutrition_data['Carbs'].sum()
    total_protein = user_nutrition_data['Protein'].sum()
    total_fats = user_nutrition_data['Fats'].sum()

    macronutrients = ['Carbs', 'Protein', 'Fats']
    values = [total_carbs, total_protein, total_fats]

    plt.figure(figsize=(8, 8))
    plt.pie(values, labels=macronutrients, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])

    if username:
        plt.title(f"Macronutrient Distribution for {username}")
    else:
        plt.title("Macronutrient Distribution")

    plt.axis('equal')

    # Plot the Graph
    plt.show()

def plot_weight(username, weight_data):
    if weight_data is None or 'registration_date' not in weight_data or 'weight' not in weight_data:
        print("Error: Missing data for weight or registration date.")
        return None

    # Sort by registration date to ensure proper plotting
    data = pd.DataFrame({
        'registration_date': weight_data['registration_date'],
        'weight': weight_data['weight']
    })

    # Convert 'registration_date' column to datetime
    data['registration_date'] = pd.to_datetime(data['registration_date'])

    # Sort by registration date
    data = data.sort_values(by='registration_date')

    # Plot weight data
    plt.figure(figsize=(10, 6))
    plt.plot(data['registration_date'], data['weight'], label=f"Weight ({username})", color="green", marker="o")

    plt.title(f"Weight Change Over Time for {username}", fontsize=14)
    plt.xlabel("Time")
    plt.ylabel("Weight (kg)")
    plt.xticks(rotation=45) 
    plt.legend()

    plt.tight_layout()
    plt.show()
    
def calculate_bmi(weight, height):
    if height == 0:
        return 0 
    height_in_meters = height / 100 
    return weight / (height_in_meters ** 2) 

def plot_bmi(username, weight_data, height_data):
    nutrition_data, exercise_data, height, weight = load_data_from_csv(username=username)

    if height is None or weight_data is None or height_data is None:
        print("Unable to calculate BMI due to missing data.")
        return

    # Ensure that weight_data and height_data are populated correctly
    # Assuming weight_data and height_data are pandas DataFrames containing 'registration_date' and 'weight'/'height'
    if len(weight_data) != len(height_data):
        print("Weight data and height data lengths do not match.")
        return

    bmi_data = []
    for i in range(len(weight_data)):
        weight = weight_data.iloc[i]['weight']
        height = height_data.iloc[i]['height']
        bmi = calculate_bmi(weight, height)
        bmi_data.append(bmi)

    # Plotting the BMI over time (based on registration_date)
    plt.figure(figsize=(10, 5))
    plt.plot(weight_data['registration_date'], bmi_data, marker='o', color='b', label='BMI')
    plt.xlabel('Time')
    plt.ylabel('BMI')
    plt.title(f'BMI for {username}')
    plt.legend()
    plt.grid(True)

    plt.show()