from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

# Assuming your backend functions are correct
from backend.authentication import register_user, login_user
from backend.diet import log_food, get_food_info

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = ""  # Define password attribute for binding

    def login(self):
        if login_user(self.ids.username.text, self.password):  # Use self.password here
            self.manager.current = "dashboard"
        else:
            self.ids.login_status.text = "Invalid credentials. Try again!"

class RegisterScreen(Screen):
    def register(self):
        # Ensure all fields are accessible via ids
        username = self.ids.username.text.strip()  # Strip extra spaces
        password = self.ids.password.text.strip()
        height = self.ids.height.text.strip()
        weight = self.ids.weight.text.strip()
        email = self.ids.email.text.strip()
        
        # Call the register_user function with the gathered data
        if register_user(username, password, height, weight, email):
            self.manager.current = "login"  # Switch to login screen if registration is successful
        else:
            print("Registration failed. Please try again.")

class DashboardScreen(Screen):
    def log_food_intake(self, food_item):
        food_data = get_food_info(food_item)
        if food_data:
            log_food(self.ids.username.text, food_data)
            self.ids.food_status.text = "Food logged successfully!"
        else:
            self.ids.food_status.text = "Food data not found."

class vitaltrack(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.current = 'register'  # Starts with register screen
        return sm

if __name__ == "__main__":
    vitaltrack().run()