from controllers.pictures_controller import addmessage, test2


# The Firebase Admin SDK to access Cloud Firestore.
from firebase_admin import initialize_app, firestore
import google.cloud.firestore

app = initialize_app()

def test():
    addmessage()

def test2():
    test2()