from backend import (
    register_user,
    login_user,
    update_user,
    get_food_info,
    log_food,
    visualize_exercise_data,
    visualize_food_data,
    weekly_reminder,
    weekly_summary,
)

def main():
    print("Welcome to the Health Tracker App!")
    while True:
        print("\n1. Register User")
        print("2. Login User")
        print("3. Update User Info")
        print("4. Log Food Intake")
        print("5. Log Exercise")
        print("6. Visualize Exercise Data")
        print("7. Visualize Food Data")
        print("8. Send Weekly Reminder")
        print("9. Send Weekly Summary")
        print("0. Exit")

        choice = input("Enter the number of your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            height = input("Enter height (in cm): ")
            weight = input("Enter weight (in kg): ")
            email = input("Enter email: ")
            register_user(username, password, height, weight, email)

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            login_user(username, password)

        elif choice == "3":
            username = input("Enter username: ")
            new_height = input("Enter new height (in cm): ")
            new_weight = input("Enter new weight (in kg): ")
            update_user(username, new_height, new_weight)

        elif choice == "4":
            username = input("Enter your username: ")
            food_item = input("Enter the food item: ")
            food_data = get_food_info(food_item)
            if food_data:
                log_food(username, food_data)
            else:
                print("Food data not found.")

        elif choice == "5":
            print("Exercise logging is not yet implemented.")

        elif choice == "6":
            username = input("Enter your username: ")
            visualize_exercise_data(username)

        elif choice == "7":
            username = input("Enter your username: ")
            visualize_food_data(username)

        elif choice == "8":
            weekly_reminder()

        elif choice == "9":
            weekly_summary()

        elif choice == "0":
            print("Exiting the app. Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()