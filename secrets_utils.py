import json
import os

SECRETS_FILE = "secrets_store.json"

def load_secrets():
    """Loads secrets from the local JSON file."""
    if not os.path.exists(SECRETS_FILE):
        return {"openai_keys": [], "gemini_keys": []}
    try:
        with open(SECRETS_FILE, "r") as f:
            return json.load(f)
    except:
        return {"openai_keys": [], "gemini_keys": []}

def save_secret(provider, key):
    """
    Saves a new key to the store if it doesn't already exist.
    provider: 'OpenAI' or 'Gemini'
    """
    if not key or not key.strip():
        return

    data = load_secrets()
    
    key_list_name = "openai_keys" if provider == "OpenAI" else "gemini_keys"
    
    if key not in data[key_list_name]:
        data[key_list_name].append(key)
        try:
            with open(SECRETS_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving secret: {e}")

def mask_key(key):
    """Returns a masked version of the key for display."""
    if len(key) < 8:
        return "****" + key[-2:]
    return f"Saved Key (Ends in ...{key[-4:]})"
