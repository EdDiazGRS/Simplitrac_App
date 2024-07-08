from google.cloud import firestore
from faker import Faker
import uuid
import random
from datetime import datetime, date

# Initialize Firestore and Faker
db = firestore.Client()
fake = Faker()

# Reference to your Firestore collection
users_collection_ref = db.collection('Users')

# Predefined list of categories
predefined_categories = [
    "Vehicle",
    "Insurance/health",
    "rent/mortgage",
    "Meals",
    "Travels",
    "Supplies",
    "Cellphone",
    "Utilities",
    "Marketing",
    "Labor",
    "Professional services",
    "Long-term assets",
    "Wages"
]

def generate_fake_user() -> tuple:
    """
    Generate a fake user document with categories and transactions as sub-collections.

    Returns:
        tuple: A tuple containing the user data, categories, and transactions.
    """
    user_id = str(uuid.uuid4())  # Generate a unique user ID
    created_at = firestore.SERVER_TIMESTAMP  # Timestamp for user creation
    last_login = firestore.SERVER_TIMESTAMP  # Timestamp for last login

    # Generate fake user data
    user_data = {
        "user_id": user_id,
        "access_token": str(uuid.uuid4()),  # Generate a unique access token
        "email": fake.email(),  # Generate a fake email
        "first_name": fake.first_name(),  # Generate a fake first name
        "last_name": fake.last_name(),  # Generate a fake last name
        "created_at": created_at,
        "last_login": last_login,
        "admin": fake.boolean(),  # Randomly assign admin status
    }

    # Generate fake categories
    categories = generate_fake_categories(user_id)
    # Generate fake transactions
    transactions = generate_fake_transactions(user_id, user_data["email"])

    return user_data, categories, transactions

def generate_fake_categories(user_id: str) -> list:
    """
    Generate fake categories for a user from a predefined list.

    Args:
        user_id (str): The user ID to link the categories to.

    Returns:
        list: A list of category data.
    """
    categories = []
    for category_name in predefined_categories:
        category_id = str(uuid.uuid4())  # Generate a unique category ID
        category_data = {
            "category_id": category_id,
            "category_name": category_name,
        }
        categories.append(category_data)
        # Save each category as a sub-collection document
        users_collection_ref.document(user_id).collection('categories').document(category_id).set(category_data)

    return categories

def generate_fake_transactions(user_id: str, email: str) -> list:
    """
    Generate fake transactions for a user and link them to predefined categories.

    Args:
        user_id (str): The user ID to link the transactions to.
        email (str): The user's email to link the transactions to.

    Returns:
        list: A list of transaction data.
    """
    transactions = []
    created_at = firestore.SERVER_TIMESTAMP  # Timestamp for transaction creation

    for _ in range(random.randint(1, 10)):  # Generate a random number of transactions
        transaction_id = str(uuid.uuid4())  # Generate a unique transaction ID
        transaction_date = fake.date_this_year()  # Generate a fake date within this year
        category_name = random.choice(predefined_categories)  # Randomly select a category
        transaction_data = {
            "user_id": user_id,  # Link transaction to user_id
            "user_email": email,  # Link transaction to user's email
            "transaction_id": transaction_id,
            "created_at": created_at,
            "transaction_date": datetime.combine(transaction_date, datetime.min.time()),  # Convert date to datetime
            "amount": round(random.uniform(10.0, 1000.0), 2),  # Generate a random amount
            "vendor": fake.company(),  # Generate a fake vendor
            "category_name": category_name,  # Link transaction to a category name
            "picture_id": str(uuid.uuid4()),  # Generate a fake picture ID
            "is_successful": fake.boolean()  # Randomly assign success status
        }
        transactions.append(transaction_data)
        # Save each transaction as a sub-collection document
        users_collection_ref.document(user_id).collection('transactions').document(transaction_id).set(transaction_data)

    return transactions

def import_fake_data_to_firestore(num_users: int = 10) -> None:
    """
    Import a specified number of fake users into Firestore.

    Args:
        num_users (int): The number of fake users to generate and import. Defaults to 10.
    """
    for _ in range(num_users):
        try:
            # Generate fake user data, categories, and transactions
            user_data, categories, transactions = generate_fake_user()
            user_doc_ref = users_collection_ref.document(user_data["user_id"])

            # Create user document
            user_doc_ref.set(user_data)

            # Create sub-collection documents
            categories_collection_ref = user_doc_ref.collection('categories')
            for category in categories:
                categories_collection_ref.document(category["category_id"]).set(category)

            transactions_collection_ref = user_doc_ref.collection('transactions')
            for transaction in transactions:
                transactions_collection_ref.document(transaction["transaction_id"]).set(transaction)

        except Exception as e:
            print(f"An error occurred: {e}")

    print(f"Imported {num_users} fake users into Firestore.")

if __name__ == "__main__":
    import_fake_data_to_firestore(10)  # Adjust the number as needed
