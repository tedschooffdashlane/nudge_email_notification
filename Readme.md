# Dashlane Weak/Reused/Compromised Password Alert Script

This Python script connects to the Dashlane Teams API, checks each team member’s password health, and sends Gmail alerts to users with weak passwords.

## Features

- Connects to Dashlane Teams API
- Retrieves and checks password health of all accepted users
- Sends personalized email alerts via Gmail to users with weak passwords

## Requirements

- Python 3.6 or higher
- `requests` Python package
- Gmail account with App Password enabled
- Dashlane API Key with appropriate access

## Setup Instructions

1. **Install Python** (https://www.python.org/downloads/)

2. **(Optional)** Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate      # Windows: venv\Scripts\activate
    ```

3. **Install the required Python package**:
    ```bash
    pip install requests
    ```

4. **Enable Gmail App Password**:
    - Go to https://myaccount.google.com/security
    - Enable 2-Step Verification (if not already enabled)
    - Under "App Passwords", generate a new password for "Mail"
    - Save the 16-digit app password — you’ll need it below

5. **Get your Dashlane API key** from your admin or Dashlane API console

6. **Edit the script** and update the following variables:
    ```python
    # Dashlane API
    DASHLANE_API_KEY = "your_dashlane_api_key"

    # Gmail settings
    SENDER_EMAIL = "your_email@gmail.com"
    SENDER_PASSWORD = "your_16_digit_app_password"
    ```

    Line 80 - weak_count = password_health.get("weakPasswords", 0) can be edited to "get" weak/reused/compromised passwords. 

7. **Run the script**:
    ```bash
    python3 dashlane_weak_password_alert.py
    ```


