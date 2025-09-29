import os
import json
import base64
import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    """Initialize Firebase with credentials from environment variable"""
    try:
        # Get the Firebase credentials from environment variable
        firebase_credentials = os.environ.get('FIREBASE_CREDENTIALS')
        
        if not firebase_credentials:
            # If not in environment, try to use local file
            cred = credentials.Certificate('firebase-key.json')
        else:
            # Decode the base64 string and create a temporary credential file
            decoded_credentials = base64.b64decode(firebase_credentials)
            cred_dict = json.loads(decoded_credentials)
            cred = credentials.Certificate(cred_dict)
        
        # Initialize Firebase app
        firebase_admin.initialize_app(cred)
        print("✅ Firebase initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing Firebase: {str(e)}")
        raise e
