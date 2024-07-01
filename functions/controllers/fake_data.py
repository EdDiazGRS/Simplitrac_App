from google.cloud import firestore
from faker import Faker
import uuid
import random

# Initialize Firestore and Faker
db = firestore.Client()
fake = Faker()

# Reference to your Firestore collection
users_collection_ref = db.collection('User')

def generate_fake_user():
    """Generate a fake user document with sub-collections"""
    user_id = str(uuid.uuid4())
    created_at = firestore.SERVER_TIMESTAMP
    last_login = firestore.SERVER_TIMESTAMP

    user_data = {
        "user_id": user_id,
        "google_id": fake.uuid4(),
        "email": fake.email(),
        "f_name": fake.first_name(),
        "l_name": fake.last_name(),
        "created_at": created_at,
        "last_login": last_login,
        "admin": fake.boolean(),
        "picture": None,
        "coordinates": None
    }
    return user_data

def import_fake_data_to_firestore(num_users=5):
    """Import a specified number of fake users into Firestore"""
    for _ in range(num_users):
        # user_data, categories, transactions = generate_fake_user()
        user_data = generate_fake_user()
        user_doc_ref = users_collection_ref.document(user_data["user_id"])
        
        # Create user document
        user_doc_ref.set(user_data)

        # Create sub-collection documents
        # categories_collection_ref = user_doc_ref.collection('categories')
        # for category in categories:
        #     categories_collection_ref.document(category["category_id"]).set(category)
        
        # transactions_collection_ref = user_doc_ref.collection('transactions')
        # for transaction in transactions:
        #     transactions_collection_ref.document(transaction["transaction_id"]).set(transaction)

    print(f"Imported {num_users} fake users into Firestore.")

if __name__ == "__main__":
    import_fake_data_to_firestore(5)  # Adjust the number as needed


'''
#intial attempt to create fake data. 
    return user_data
    # Generate fake categories
    categories = []
    for _ in range(random.randint(1, 3)):
        category = {
            "category_id": str(uuid.uuid4()),
            "category_name": fake.word()
        }
        categories.append(category)

    # Generate fake transactions
    transactions = []
    for _ in range(random.randint(1, 5)):
        transaction = {
            "transaction_id": str(uuid.uuid4()),
            "created_at": firestore.SERVER_TIMESTAMP,
            "amount": random.uniform(10.0, 500.0),
            "vendor": fake.company(),
            "category_id": random.choice(categories)["category_id"],
            "is_successful": fake.boolean(),
            "recheck": fake.boolean()
        }
        transactions.append(transaction)
'''
