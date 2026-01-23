import json
import os

PROFILE_FILE = "my_profile.json"

def load_profile():
    """Loads user profile from local JSON file."""
    if not os.path.exists(PROFILE_FILE):
        return {}
    try:
        with open(PROFILE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_profile(data):
    """Saves user profile to local JSON file."""
    try:
        with open(PROFILE_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving profile: {e}")
        return False
