import sys
import os
import asyncio
import json

# Add the project root and the modules directory to the Python path
# so we can import the Qobuz module components
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'modules'))

try:
    # Import just the Qobuz API class
    from qobuz.qobuz_api import Qobuz
except ImportError as e:
    print(f"Error importing Qobuz module. Make sure it's in modules/qobuz/: {e}")
    sys.exit(1)

# Define a simple local exception for the test
class TestQobuzError(Exception):
    pass

# --- Function to load credentials from settings.json ---
def load_credentials_from_settings():
    settings_path = os.path.join(project_root, 'config', 'settings.json')
    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)

        qobuz_settings = settings.get('modules', {}).get('qobuz')
        if not qobuz_settings:
            print(f"Error: 'qobuz' module settings not found in {settings_path}")
            return None

        credentials = {
            "app_id": qobuz_settings.get('app_id'),
            "app_secret": qobuz_settings.get('app_secret'),
            "email": qobuz_settings.get('username'), # Note: key is 'username' in settings
            "password": qobuz_settings.get('password')
        }

        # Check if any essential credential is empty or None
        if not all(credentials.values()):
            missing = [k for k, v in credentials.items() if not v]
            print(f"Error: Missing credentials in qobuz settings ({settings_path}): {', '.join(missing)}")
            return None
        
        # Specifically check if placeholders are still present (optional but good practice)
        if credentials["app_id"] == "YOUR_APP_ID" or \
           credentials["app_secret"] == "YOUR_APP_SECRET" or \
           credentials["email"] == "YOUR_QOBUZ_EMAIL" or \
           credentials["password"] == "YOUR_QOBUZ_PASSWORD":
            print(f"Error: Placeholder credentials found in {settings_path}. Please fill them in.")
            return None


        return credentials

    except FileNotFoundError:
        print(f"Error: Settings file not found at {settings_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not parse JSON from {settings_path}")
        return None
    except Exception as e:
        print(f"Error loading settings: {e}")
        return None
# --- End of function ---

async def run_login_test():
    # --- Load credentials from settings file ---
    credentials = load_credentials_from_settings()
    if not credentials:
        return # Error message already printed by load_credentials_from_settings

    app_id = credentials["app_id"]
    app_secret = credentials["app_secret"]
    email = credentials["email"]
    password = credentials["password"]
    # --- End of loading credentials ---

    print(f"Attempting to log in to Qobuz as {email}...")

    # Define a simple error handler function (using the local exception)
    # The Qobuz API seems to expect a callable that it can raise.
    # We don't need the handle_error function here anymore.

    try:
        # Instantiate the Qobuz API client, passing our local exception class
        # It will be raised by the Qobuz class on errors.
        qobuz_client = Qobuz(app_id, app_secret, TestQobuzError) # Pass the exception class directly

        # Attempt login
        print("Calling login method...")
        # Use asyncio.to_thread since qobuz_api.login uses synchronous requests
        token = await asyncio.to_thread(qobuz_client.login, email, password)

        if token:
            print("\n--- Login Successful! ---")
            print(f"Received Auth Token (truncated): {token[:10]}...")
        else:
            # This case might not be reachable if errors always raise exceptions
            print("\n--- Login Failed (No token received and no exception raised) ---")

    # Catch the local exception class that Qobuz API will raise
    except TestQobuzError as e:
        print(f"\n--- Login Failed (TestQobuzError): {e} ---")
    except Exception as e:
        print(f"\n--- Login Failed (Unexpected Error): {type(e).__name__} - {e} ---")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run_login_test()) 