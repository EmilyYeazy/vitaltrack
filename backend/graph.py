import matplotlib.pyplot as plt
import pandas as pd
import csv
from datetime import datetime
import os

def load_data_from_csv(username):
    # Load nutrition data
    nutrition_data = pd.read_csv('data/nutrition_data.csv')
    nutrition_data = nutrition_data[nutrition_data['Username'].str.strip().str.lower() == username.strip().lower()]

    # Load exercise data
    exercise_data = pd.read_csv('data/exercise_data.csv')
    exercise_data = exercise_data[exercise_data['Username'].str.strip().str.lower() == username.strip().lower()]

    # Get height and weight from the user.csv file
    try:
        user_data = pd.read_csv('data/user.csv')  # Load the user.csv file
        user_data = user_data[user_data['username'].str.strip().str.lower() == username.strip().lower()]  # Use 'username' for comparison
        weight = user_data['weight'].iloc[-1] if not user_data.empty else None  # Use 'weight' column
        height = user_data['height'].iloc[0] if not user_data.empty else None  # Use 'height' column
    except FileNotFoundError:
        weight, height = None, None

    return nutrition_data, exercise_data, height, weight

def save_graph(plt, filename):
    # Ensure the 'data/graph' folder exists, create it if not
    if not os.path.exists('data/graph'):
        os.makedirs('data/graph')
    
    # Save the figure to 'data/graph' folder
    file_path = f"data/graph/{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(file_path)
    print(f"Graph saved as {file_path}")

def plot_calories(username, nutrition_data, exercise_data, save=False):
    user_nutrition_data = nutrition_data[nutrition_data['Username'] == username]
    user_exercise_data = exercise_data[exercise_data['Username'] == username]

    if user_nutrition_data.empty and user_exercise_data.empty:
        print(f"No data available for {username}.")
        return

    user_nutrition_data_grouped = user_nutrition_data.groupby('Date')['Calories'].sum()
    user_exercise_data_grouped = user_exercise_data.groupby('Date')['Calories_Burned'].sum()

    combined_data = pd.DataFrame({
        'Calories_Consumed': user_nutrition_data_grouped,
        'Calories_Burned': user_exercise_data_grouped
    }).fillna(0)

    plt.figure(figsize=(10, 6))
    plt.plot(combined_data.index, combined_data['Calories_Consumed'], label="Calories Consumed", color="blue", marker="o")
    plt.plot(combined_data.index, combined_data['Calories_Burned'], label="Calories Burned", color="red", marker="o")

    plt.title(f"Calories Consumed vs. Burned for {username}", fontsize=14)
    plt.xlabel("Date")
    plt.ylabel("Calories")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    if save:
        save_graph(plt, f"calories_{username}")
    else:
        plt.show()

def plot_macronutrient_distribution(nutrition_data, username=None, save=False):
    if username:
        user_nutrition_data = nutrition_data[nutrition_data['Username'] == username]
    else:
        user_nutrition_data = nutrition_data

    if user_nutrition_data.empty:
        print(f"No nutrition data available for {username if username else 'the user'}.")
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

    if save:
        save_graph(plt, f"macronutrients_{username}")
    else:
        plt.show()

def plot_weight(username, save=False):
    nutrition_data, exercise_data, height, weight = load_data_from_csv(username=username)

    if weight is None:
        print("No weight data available for the user.")
        return

    weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
    weight_data = [weight] * len(weeks)

    df = pd.DataFrame({
        "Week": weeks,
        "Weight": weight_data
    })

    plt.figure(figsize=(10, 6))
    plt.plot(df['Week'], df['Weight'], label=f"Weight ({username})", color="green", marker="o")

    plt.title(f"Weekly Weight Change for {username}", fontsize=14)
    plt.xlabel("Week")
    plt.ylabel("Weight (kg)")
    plt.legend()
    plt.tight_layout()

    if save:
        save_graph(plt, f"weight_{username}")
    else:
        plt.show()

def calculate_bmi(weight, height):
    if height == 0:
        return 0  # Avoid division by zero if height is not available
    return weight / (height ** 2)

def plot_bmi(username, weight_data, save=False):
    nutrition_data, exercise_data, height, weight = load_data_from_csv(username=username)

    if height is None or weight is None:
        print("Unable to calculate BMI due to missing data.")
        return

    bmi_data = [calculate_bmi(weight, height) for weight in weight_data]

    plt.figure(figsize=(10, 5))
    plt.plot(range(len(bmi_data)), bmi_data, marker='o', color='b', label='BMI')
    plt.xlabel('Weeks')
    plt.ylabel('BMI')
    plt.title(f'BMI for {username}')
    plt.legend()
    plt.grid(True)

    if save:
        save_graph(plt, f"bmi_{username}")
    else:
        plt.show()