import firebase_admin
from firebase_admin import credentials, firestore, auth
from flask import Flask, request, jsonify

# Initialize Firebase Admin SDK
cred = credentials.Certificate("functions/key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
app = Flask(__name__)


def create_user(email, password, first_name, last_name):
    try:
        # Create user in Firebase Authentication
        user = auth.create_user(
            email=email,
            password=password
        )

        # Store user data in Firestore
        user_ref = db.collection("users").document(user.uid)
        user_ref.set({
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "createdAt": firestore.SERVER_TIMESTAMP
        })

        print(f"User created and data stored in Firestore: {user.uid}")
    except Exception as e:
        print(f"Error creating user: {e}")


# Example usage
create_user("user@example.com", "password123", "John", "Doe")
