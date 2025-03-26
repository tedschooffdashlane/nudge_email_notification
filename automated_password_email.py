import json
import requests
import smtplib
from email.mime.text import MIMEText

# Dashlane API Endpoint
DASHLANE_API_URL = "https://api.dashlane.com/public/teams/Members"
DASHLANE_API_KEY = "DLP_ac645e35-97db-491b-b8c3-064cc2159833_9DF2Z6QX3PY80K429NQJX4E9X3MFKQS3_cLj7hoptx7gk6JBhpGgrsgrgR3jQk8nYvECnfYWAj87ECGOhf4UhWOAeb3qfiiJt"

# Email settings
SENDER_EMAIL = "schoofft@gmail.com"         # Replace with your sender email
SENDER_PASSWORD = "twnrhsewdnmhceni"         # Use app password for Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def get_dashlane_members():
    """Fetches member data from Dashlane API and prints response for debugging."""
    headers = {
        "Authorization": f"Bearer {DASHLANE_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(DASHLANE_API_URL, headers=headers, json={})
        response_text = response.text
        print(f"Raw API Response:\n{response_text}")

        if response.status_code == 200:
            try:
                response_data = response.json()
                members = response_data.get("data", {}).get("members", [])
                print(f"Successfully retrieved {len(members)} members from Dashlane.")
                return members
            except json.JSONDecodeError:
                print("Failed to decode JSON. Response might not be in expected format.")
        else:
            print(f"API Error {response.status_code}: {response_text}")

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")

    return []


def alert_user_via_email(email, weak_count):
    """Sends an email alert to the user about weak passwords."""
    subject = "Dashlane Alert: Weak Passwords Detected"
    body = f"""
Hi,

Our system has detected that {weak_count} of your saved passwords in Dashlane are marked as weak.

Please log in to your Dashlane account and update those passwords as soon as possible.
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, msg.as_string())
            print(f"Alert sent to {email}")
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")


def find_and_alert_weak_users(members):
    """Find users with weak passwords and send them email alerts."""
    weak_users = []

    for user in members:
        if user.get("status") != "accepted":
            continue

        password_health = user.get("passwordHealth", {})
        weak_count = password_health.get("weakPasswords", 0)

        if weak_count > 0:
            email = user.get("email", "N/A")
            print(f"Weak Passwords: {email} - {weak_count} weak password(s)")
            alert_user_via_email(email, weak_count)
            weak_users.append(user)

    if not weak_users:
        print("No users with weak passwords found.")

    return weak_users


if __name__ == "__main__":
    members = get_dashlane_members()
    if members:
        find_and_alert_weak_users(members)
