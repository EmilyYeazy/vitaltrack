import os
from dotenv import load_dotenv

load_dotenv('password.env')

class Config:
    NUTRITIONIX_APP_ID = os.getenv('NUTRITIONIX_APP_ID')
    NUTRITIONIX_API_KEY = os.getenv('NUTRITIONIX_API_KEY')

    EXERCISE_END_POINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
    EXERCISE_DB_FILE = "data/exercise_data.csv"

    NUTRITION_END_POINT = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    NUTRITION_DB_FILE = "data/nutrition_data.csv"

    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

import os
from dotenv import load_dotenv

load_dotenv('password.env')

# Debugging to check if the environment variables are loaded
print("NUTRITIONIX_APP_ID:", os.getenv('NUTRITIONIX_APP_ID'))
print("NUTRITIONIX_API_KEY:", os.getenv('NUTRITIONIX_API_KEY'))
print("SENDER_EMAIL:", os.getenv('SENDER_EMAIL'))
print("SENDER_PASSWORD:", os.getenv('SENDER_PASSWORD'))