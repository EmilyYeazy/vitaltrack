import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
import csv

def send_email(to_email, subject, body, attachments=None):
    """
    Send an email with optional attachments using an SMTP server.

    Args:
    - to_email (str): The recipient's email address.
    - subject (str): The email subject.
    - body (str): The email body text.
    - attachments (list): List of file paths to attach.
    """
    from_email = "your_email@gmail.com"
    from_password = "your_password"  # Consider using an app-specific password.

    # Create the email
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attach files if any
    if attachments:
        for attachment in attachments:
            with open(attachment, "rb") as file:
                img = MIMEImage(file.read())
                img.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment)}")
                msg.attach(img)

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, msg.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def weekly_reminder():
    """
    Send weekly reminders to all users.
    """
    users = [
        {"name": "Emily", "email": "emily@example.com"},
        {"name": "John", "email": "john@example.com"}
    ]
    for user in users:
        subject = "Weekly Reminder: Log Your Meals and Exercise!"
        body = f"""
        Hi {user['name']},
        
        This is your weekly reminder to log your meals and exercise in the app. 
        Consistency is the key to reaching your health goals!

        Don't forget to check your progress too!

        Best,
        Your Health Tracker
        """
        send_email(user["email"], subject, body)

def weekly_summary():
    """
    Send weekly summaries with graphs to all users.
    """
    users = [
        {"name": "Emily", "email": "emily@example.com"},
        {"name": "John", "email": "john@example.com"}
    ]
    for user in users:
        # Generate graphs for the user
        exercise_graph_path = f"data/graph/{user['name']}/exercise_data_{user['name']}.png"
        food_graph_path = f"data/graph/{user['name']}/food_data_{user['name']}.png"
        
        # Visualize the exercise and food data and save the graphs
        visualize_exercise_data(user["name"], save=True)
        visualize_food_data(user["name"], save=True)
        
        # Example: Read user's food log data from a CSV file
        with open("data/food_data.csv", "r") as file:
            reader = csv.DictReader(file)
            total_calories = sum(float(row["calories"]) for row in reader if row["user"] == user["name"])
        
        subject = "Weekly Summary: Your Health Progress!"
        body = f"""
        Hi {user['name']},
        
        Here's your weekly summary:
        - Total Calories Logged: {total_calories} kcal

        Please find your weekly health progress graphs attached.

        Keep up the great work, and don't forget to stay consistent!

        Best,
        Your Health Tracker
        """
        
        # Send email with the graphs attached
        send_email(user["email"], subject, body, attachments=[exercise_graph_path, food_graph_path])