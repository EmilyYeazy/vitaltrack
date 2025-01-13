from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label 
from kivy.uix.button import Button  
from kivy.uix.scrollview import ScrollView 
from kivy.uix.spinner import Spinner
from kivy.uix.togglebutton import ToggleButton

from backend.authentication import register_user, login_user, update_data, update_settings
from backend.diet import log_food, get_food_info
from backend.exercise import get_exercise_info, log_to_csv
from backend.graph import load_data_from_csv, plot_calories, plot_micronutrient_distribution, plot_weight, plot_bmi

class vitaltrack(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(DietScreen(name="diet_screen"))
        sm.add_widget(ExerciseScreen(name="exercise_screen"))
        sm.add_widget(UpdateScreen(name="update_screen"))
        sm.add_widget(UserSettingsUpdateScreen(name="user_settings_update_screen"))
        sm.add_widget(BodyDataUpdateScreen(name="body_data_update_screen"))
        sm.add_widget(SelectGraphScreen(name="select_graph"))
        sm.add_widget(GenerateGraphScreen(name="generate_graph"))
        sm.current = 'register'  # Starts with register screen
        return sm

class RegisterScreen(Screen):
    def register(self):
        # Ensure all fields are accessible via ids
        username = self.ids.username.text.strip()  # Strip extra spaces
        password = self.ids.password.text.strip()
        height = self.ids.height.text.strip()
        weight = self.ids.weight.text.strip()

        # Call the register_user function with the gathered data
        if not register_user(username, password, height, weight):
            # If the user already exists, the register_user function will return False
            self.ids.register_status.text = "User already exists! Proceed to Login!"  # Show message in the register_status label
            return
        
        # If registration is successful, switch to the login screen
        self.manager.current = "login"

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def login(self):
        # Retrieve input from text fields in the UI
        username = self.ids.username.text.strip()  # Trim whitespace
        password = self.ids.password.text.strip()  # Trim whitespace

        # Debugging: Print captured username and password
        print(f"Attempting login with Username: '{username}', Password: '{password}'")

        if not username or not password:
            self.ids.login_status.text = "Please fill in both fields."
            return

        if login_user(username, password):  # Call the login_user function
            # Store the username globally in the app instance
            app = App.get_running_app()
            app.username = username  # Set the username globally for session tracking

            # Get the DashboardScreen and pass the username
            dashboard_screen = self.manager.get_screen("dashboard")
            dashboard_screen.set_username(username)  # Set the username in DashboardScreen

            # Navigate to the dashboard on success
            self.manager.current = "dashboard"
        else:
            # Update the status label to show invalid credentials
            self.ids.login_status.text = "Invalid credentials. Try again!"

    def go_to_register(self):
        # Navigate to the registration screen
        self.manager.current = "register"

class DashboardScreen(Screen):
    def set_username(self, username):
        self.username = username  # Store the username for later use

    def go_to_diet(self):
        # Navigate to the Diet screen
        self.manager.current = "diet_screen"

    def go_to_exercise(self):
        # Navigate to the Exercise screen
        self.manager.current = "exercise_screen"
    
    def update_dashboard(self):
        self.manager.current = "update_screen"

    def go_to_graph(self):
        self.manager.current = 'select_graph'

    def close(self):
        # Close the app
        App.get_running_app().stop()

class DietScreen(Screen):
    def on_enter(self):
        # Reset the food log input field when entering the screen
        self.ids.food_input.text = ''
        self.ids.food_info.text = ''  # Clear the food info label
        self.ids.success_message.text = ''  # Clear any success/error messages

    def get_food_info(self, food_name):
        food_data = get_food_info(food_name)

        if food_data:
            self.ids.food_info.text = f"Food: {food_data['name']}\n" \
                                      f"Calories: {food_data['calories']} kcal\n" \
                                      f"Carbs: {food_data['carbs']} g\n" \
                                      f"Protein: {food_data['protein']} g\n" \
                                      f"Fats: {food_data['fats']} g"
        else:
            self.ids.food_info.text = "Nutritional info not found."

    def log_food(self, food_item):
        if food_item:
            food_data = get_food_info(food_item)
            if food_data:
                log_food(self.manager.get_screen("dashboard").username, food_data)
                self.ids.success_message.text = "Food logged successfully!"
            else:
                self.ids.success_message.text = "Food data not found."
        else:
            self.ids.success_message.text = "Please enter a food item."

class ExerciseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        # Clear the exercise input and results when entering the screen
        self.ids.exercise_input.text = ""  # Clear the input field
        self.ids.exercise_info.text = ""  # Clear the exercise details display
        self.ids.success_message.text = ""  # Clear any success/failure messages

    def get_exercise_info(self, exercise_input):
        # Fetch exercise data from the Nutritionix API
        exercises = get_exercise_info(exercise_input)

        if exercises:
            # Display the first exercise's details (you can extend to multiple if needed)
            exercise_details = "\n".join(
                [f"Exercise: {exercise['name']}\nCalories Burned: {exercise.get('nf_calories', 0)} kcal"
                 for exercise in exercises]
            )
            self.ids.exercise_info.text = exercise_details
        else:
            self.ids.exercise_info.text = "Exercise info not found. Please check your input."

    def log_exercise(self, exercise_input):
        username = self.manager.get_screen("dashboard").username  # Get the username
        exercises = get_exercise_info(exercise_input)

        if exercises:
            log_to_csv(username, exercise_input, exercises)  # Log to CSV
            self.ids.success_message.text = "Exercise logged successfully!"
        else:
            self.ids.success_message.text = "Failed to log exercise. Please try again."

class UpdateScreen(Screen):
    def go_to_user_settings_update(self):
        """Navigate to User Settings Update page."""
        user_settings_update_screen = self.manager.get_screen("user_settings_update_screen")
        user_settings_update_screen.username = self.manager.get_screen("dashboard").username
        self.manager.current = "user_settings_update_screen"

    def go_to_body_data_update(self):
        """Navigate to Body Data Update page."""
        self.manager.current = "body_data_update_screen"

    def back_to_dashboard(self):
        """Return to the Dashboard page."""
        self.manager.current = "dashboard"

class UserSettingsUpdateScreen(Screen):
    def on_enter(self):
        """Clear input fields when entering the screen."""
        self.ids.password_input.text = ""

    def save_user_settings(self):
        # Get the input value for password from the text field
        password = self.ids.password_input.text

        # Retrieve the username directly (passed from DashboardScreen)
        username = self.username

        # Call the update_settings function to save the new settings
        if password:
            success = update_settings(username, password)
            if success:
                print(f"Settings for {username} updated successfully.")
                self.manager.current = "update_screen"  # Navigate back to the Update screen
            else:
                print(f"Update failed. User {username} not found.")
        else:
            print("Please fill in the password.")
    
    def back_to_update_screen(self):
        """Go back to the Update Screen."""
        self.manager.current = "update_screen"

class BodyDataUpdateScreen(Screen):
    def on_enter(self):
        self.ids.height_input.text = "" 
        self.ids.weight_input.text = ""
        self.username = self.manager.get_screen("dashboard").username

    def save_body_data(self):
        height = self.ids.height_input.text
        weight = self.ids.weight_input.text
        username = self.username

        if height and weight:  # Ensure height and weight are provided
            # Ensure that we are passing the correct values in the correct order
            success = update_data(username, weight, height)  # weight first, height second
            if success:
                print(f"User {username}'s body data updated successfully!")
                self.manager.current = "update_screen"
            else:
                print(f"Failed to update data for {username}.")
        else:
            print("Please fill in both height and weight.")
        
    def back_to_update_screen(self):
        self.manager.current = "update_screen"

class SelectGraphScreen(Screen):
    def __init__(self, **kwargs):
        super(SelectGraphScreen, self).__init__(**kwargs)
        self.graph_type = None  # Initialize the graph type as None

    def select_graph(self, graph_type):
        """Handle graph type selection and transition to the next screen."""
        self.graph_type = graph_type

        # Pass the selected graph type and username to the GenerateGraphScreen
        generate_graph_screen = self.manager.get_screen('generate_graph')
        generate_graph_screen.graph_type = graph_type
        generate_graph_screen.username = App.get_running_app().username

        # Switch to the GenerateGraphScreen
        self.manager.current = 'generate_graph'

class GenerateGraphScreen(Screen):
    def __init__(self, **kwargs):
        super(GenerateGraphScreen, self).__init__(**kwargs)
        self.graph_type = None  # Initialize graph_type as None
        self.username = None  # Initialize username as None

    def on_enter(self):
        # Ensure username is set before proceeding
        if not self.username:
            print("Error: Username is not set!")
            return

        # Get the selected graph type from SelectGraphScreen
        self.graph_type = self.manager.get_screen('select_graph').graph_type

        if self.graph_type is None:
            print("Error: Graph type is not set!")
            return

        # Log the columns of the nutrition data to check if Carbs, Protein, Fats exist
        try:
            nutrition_data, _, _, _ = load_data_from_csv(self.username)
        except Exception as e:
            print(f"Error loading nutrition data: {e}")

    def generate_graph(self):
        if not self.username:
            print("Error: Username is not set!")
            return
                
        try:
            nutrition_data, exercise_data, height_data, weight_data = load_data_from_csv(self.username)
        except Exception as e:
            print(f"Error loading data for user {self.username}: {e}")
            return
                
        # Generate the selected graph
        if self.graph_type == 'Calories':
            plot_calories(self.username, nutrition_data, exercise_data)
        elif self.graph_type == 'Micronutrient':
            plot_micronutrient_distribution(nutrition_data, self.username)
        elif self.graph_type == 'Weight':
            plot_weight(self.username,weight_data)
        elif self.graph_type == 'BMI':
            plot_bmi(self.username, weight_data,height_data)
        else:
            print("Invalid graph type selected")

if __name__ == "__main__":
    vitaltrack().run()