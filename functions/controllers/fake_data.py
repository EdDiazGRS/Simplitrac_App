from datetime import datetime, timedelta, timezone
from google.cloud import firestore
from faker import Faker
import uuid
import random

# Initialize Firestore and Faker
db = firestore.Client()
fake = Faker()
users_collection_ref = db.collection('Users')

# fixed categories
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

def check_if_email_exists(email: str) -> bool:
    """
    Check if a user with the specified email already exists in Firestore.

    Args:
        email (str): reference email.

    Returns:
        bool: true if exists, false if new.
    """
    doc = users_collection_ref.document(email).get()
    return doc.exists

def get_user_id_by_email(email: str) -> str:
    """
    Get the user_id associated with an existing email in Firestore. Makes sure the user_id is attached to email.

    Args:
        email (str): The email to query.

    Returns:
        str: The user_id if the email exists, None otherwise.
    """
    doc = users_collection_ref.document(email).get()
    if doc.exists:
        return doc.to_dict().get('user_id')
    return None

def generate_fake_user(specific_email=None) -> tuple:
    """
    Generate a fake user document with categories and transactions as sub-collections.
    If a specific email is provided, use that email for the generated user.
    The function checks if the email already exists and reuses the user_id.

    Args:
        specific_email (str, optional): A specific email to assign to the user. Defaults to None.

    Returns:
        tuple: A tuple containing the user data, categories, and transactions, or None if the email exists.
    """

    #fake data based on user email
    email = specific_email if specific_email else fake.email()

    # does email exist in firestore?

    existing_user_id = get_user_id_by_email(email)
    if existing_user_id:
        print(f"User with email {email} already exists with user_id {existing_user_id}.")
        user_id = existing_user_id  #set email to the one that exists
    else:
        user_id = str(uuid.uuid4())  # if not create a new one

    # formatting to match bigquery so created at is not null
    utc_zone = timezone.utc
    random_days = random.randint(0, 365)
    random_seconds = random.randint(0, 86400)
    random_date = datetime.now(utc_zone) - timedelta(days=random_days, seconds=random_seconds)
    formatted_timestamp = random_date.strftime('%Y-%m-%d %H:%M:%S UTC')

    created_at = firestore.SERVER_TIMESTAMP  #timestamp for user creation
    last_login = firestore.SERVER_TIMESTAMP  #timestamp for last login

    #generate fake user data
    user_data = {
        "user_id": user_id,
        "access_token": str(uuid.uuid4()),  
        "email": "paulan21095@gmail.com",  # hardcoded email
        "first_name": fake.first_name(),  
        "last_name": fake.last_name(),  
        "created_at": formatted_timestamp,
        "last_login": formatted_timestamp,
        "admin": fake.boolean(), 
    }

    # create fake categories
    categories = generate_fake_categories(email)
    # create fake transactions
    transactions = generate_fake_transactions(email, user_id)

    return user_data, categories, transactions

def generate_fake_categories(email: str) -> list:
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
        #each category is sub collection 
        users_collection_ref.document(email).collection('categories').document(category_id).set(category_data)

    return categories

def generate_fake_transactions(email: str, user_id: str) -> list:
    """
    Generate fake transactions for a user and link them to predefined categories.
    Use the user_id associated with the email.

    Args:
        user_id (str): The user ID to link the transactions to.
        email (str): The user's email to link the transactions to.

    Returns:
        list: A list of transaction data.
    """
    transactions = []
    created_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')  # Timestamp for transaction creation

    for _ in range(random.randint(1, 10)):  # number of random transactions to create
        transaction_id = str(uuid.uuid4())  
        transaction_date = fake.date_this_year()
        category_name = random.choice(predefined_categories)
        transaction_data = {
            "user_id": user_id,  #transaction to user_id
            "email": email,  #connect transaction to user's email
            "transaction_id": transaction_id,
            "created_at": created_at,
            "transaction_date": datetime.combine(transaction_date, datetime.min.time()).strftime('%Y-%m-%d %H:%M:%S UTC'),  # Convert date to formatted datetime
            "amount": round(random.uniform(10.0, 1000.0), 2),  
            "vendor": fake.company(),  
            "category_name": category_name,
            "picture_id": str(uuid.uuid4()),
            "is_successful": fake.boolean(),
        }
        transactions.append(transaction_data)
        #each transaction is sub-document in subcolletion 
        users_collection_ref.document(user_id).collection('transactions').document(transaction_id).set(transaction_data)

    return transactions

def import_fake_data_to_firestore(num_users: int = 10, specific_email=None) -> None:
    """
    Import a specified number of fake users into Firestore.
    If a specific email is provided, generate data for that email.
    Check if the email already exists before generating new data.

    Args:
        num_users (int): The number of fake users to generate and import. Defaults to 10.
        specific_email (str, optional): A specific email to assign to one of the users.
    """
    if specific_email:
        user_data, categories, transactions = generate_fake_user(specific_email)
        if user_data: #checking if user exists
            user_doc_ref = users_collection_ref.document(user_data["email"])
            user_doc_ref.set(user_data, merge=True)
            categories_collection_ref = user_doc_ref.collection('categories')
            for category in categories:
                categories_collection_ref.document(category["category_id"]).set(category)
            transactions_collection_ref = user_doc_ref.collection('transactions')
            for transaction in transactions:
                transactions_collection_ref.document(transaction["transaction_id"]).set(transaction)
            print(f"Imported or updated data for {specific_email}")
    else:
        for _ in range(num_users):
            try:
                user_data, categories, transactions = generate_fake_user()
                if user_data:  # executes when no email exists
                    user_doc_ref = users_collection_ref.document(user_data["email"])
                    user_doc_ref.set(user_data, merge=True)
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
    import_fake_data_to_firestore(specific_email="paulan21095@gmail.com")
