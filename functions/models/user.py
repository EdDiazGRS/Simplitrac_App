import json
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
import firebase_admin
from firebase_admin import firestore, credentials, auth
from dotenv import load_dotenv
import os
from models.category import Category
from models.transaction import Transaction
from protocols.user_protocol import UserProtocol
from models.response import Response


# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(env_path)

# Initialize Firebase using the service account
from flask_cors import CORS
firebase_service_account = os.getenv('SECRET_KEY_FOR_FIREBASE')
firebase_config = json.loads(firebase_service_account)
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)

db = firestore.client()


class User(UserProtocol):
    """
    Represents a user with personal information and associated transactions and categories.

    Attributes:
        class_name (str): The name of the class.
    """

    class_name = "User"

    def __init__(self, data: Optional[Union[dict, str]] = None):
        """
        Initializes a new User instance.

        Args:
            data (Optional[Union[str, Any]]): The data to initialize the user. Can be a JSON string or str.
        """
        self._user_id: Optional[str] = None
        self._access_token: [Optional[str]] = None
        self._email: Optional[str] = None
        self._first_name: Optional[str] = None
        self._last_name: Optional[str] = None
        self._created_at: Optional[datetime] = None
        self._last_login: Optional[datetime] = None
        self._admin: Optional[bool] = None
        self._transactions: List[Transaction] = []
        self._categories: List[Category] = []

        if isinstance(data, dict):
            try:
                self._initialize_from_data(data)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON string provided")
        elif isinstance(data, str):
            self._initialize_from_firestore(data)
        elif data is None:
            pass
        else:
            raise ValueError("Constructor requires either a JSON string or a str")

    def _initialize_from_data(self, data: Dict[str, Any]) -> None:
        """
        Initializes the user attributes from a dictionary of data.

        Args:
            data (Dict[str, str]): The data to initialize the user.
        """
        # self._user_id = data.get('user_id') if data.get('user_id') else ""
        # self._access_token = data.get('access_token')
        # self._email = data.get('email')
        # self._first_name = data.get('first_name')
        # self._last_name = data.get('last_name')
        # self._created_at = data.get('created_at')
        # self._last_login = data.get('last_login')
        # self._admin = data.get('admin')
        for k, v in data.items():
            setattr(self, k, v)

        if 'transactions' in data:
            self._transactions = [Transaction(tx) for tx in data['transactions']]
        if 'categories' in data:
            self._categories = [Category(cat) for cat in data['categories']]

    def _initialize_from_firestore(self, user_id: str) -> None:
        """
        Fetches and initializes the user data from Firestore using the provided UUID.

        Args:
            user_id (str): The unique identifier of the user in Firestore.
        """
        user_ref = db.collection(self.class_name).document(user_id)
        user_doc = user_ref.get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            self._initialize_from_data(user_data)
            self._user_id = user_id
            self._fetch_subcollections()

    def _fetch_subcollections(self) -> None:
        """
        Fetches and initializes the transactions and categories subcollections from Firestore.
        """
        if self._user_id:
            transactions_ref = db.collection(self.class_name).document(str(self._user_id)).collection('Transaction')
            transaction_docs = transactions_ref.stream()
            self._transactions = [Transaction(doc.to_dict()) for doc in transaction_docs]

            categories_ref = db.collection(self.class_name).document(str(self._user_id)).collection('Category')
            category_docs = categories_ref.stream()
            self._categories = [Category(doc.to_dict()) for doc in category_docs]

    @property
    def user_id(self) -> Optional[str]:
        """Gets the user ID."""
        return self._user_id

    @user_id.setter
    def user_id(self, value: str) -> None:
        """Sets the user ID."""
        self._user_id = value

    @property
    def access_token(self) -> Optional[str]:
        """Gets the access token for the user."""
        return self._access_token

    @access_token.setter
    def access_token(self, value: str) -> None:
        """Sets the access token for the user"""
        self._access_token = value

    @property
    def email(self) -> Optional[str]:
        """Gets the email of the user."""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """Sets the email of the user."""
        self._email = value

    @property
    def first_name(self) -> Optional[str]:
        """Gets the first name of the user."""
        return self._first_name

    @first_name.setter
    def first_name(self, value: str) -> None:
        """Sets the first name of the user."""
        self._first_name = value

    @property
    def last_name(self) -> Optional[str]:
        """Gets the last name of the user."""
        return self._last_name

    @last_name.setter
    def last_name(self, value: str) -> None:
        """Sets the last name of the user."""
        self._last_name = value

    @property
    def created_at(self) -> Optional[datetime]:
        """Gets the creation date and time of the user."""
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime) -> None:
        """Sets the creation date and time of the user."""
        self._created_at = value

    @property
    def last_login(self) -> Optional[datetime]:
        """Gets the last login date and time of the user."""
        return self._last_login

    @last_login.setter
    def last_login(self, value: datetime) -> None:
        """Sets the last login date and time of the user."""
        self._last_login = value

    @property
    def admin(self) -> Optional[bool]:
        """Gets the admin status of the user."""
        return self._admin

    @admin.setter
    def admin(self, value: bool) -> None:
        """Sets the admin status of the user."""
        self._admin = value

    @property
    def transactions(self) -> List[Transaction]:
        """Gets the list of transactions associated with the user."""
        return self._transactions

    @transactions.setter
    def transactions(self, value: List[Transaction]) -> None:
        """Sets the list of transactions associated with the user."""
        self._transactions = value

    @property
    def categories(self) -> List[Category]:
        """Gets the list of categories associated with the user."""
        return self._categories

    @categories.setter
    def categories(self, value: List[Category]) -> None:
        """Sets the list of categories associated with the user."""
        self._categories = value

    def add_transaction(self, transaction_data: Dict[str, Any]) -> None:
        """
        Adds a transaction to the user's list of transactions.

        Args:
            transaction_data (Dict[str, Any]): The data for the new transaction.
        """
        transaction = Transaction(transaction_data)
        self._transactions.append(transaction)

    def add_category(self, category_data: Dict[str, Any]) -> None:
        """
        Adds a category to the user's list of categories.

        Args:
            category_data (Dict[str, Any]): The data for the new category.
        """
        category = Category(category_data)
        self._categories.append(category)

    def save_to_firestore(self) -> Response:
        """
        Saves the user's information to the Firestore User collection and its subcollections.
        Returns a Response object indicating the result of the operation.

        Returns:
            Response: A Response object with the payload of saved data if successful, or errors if not.
        """
        response = Response()

        if not self._user_id:
            response.add_error("User ID is required to save the data to Firestore")
            return response

        try:
            # Save to User collection
            user_ref = db.collection(self.class_name).document(str(self._user_id))
            user_ref.set(self.serialize())

            # Save transactions to Transaction subcollection
            transactions_ref = user_ref.collection(Transaction.class_name)
            for transaction in self._transactions:
                transaction_data = transaction.serialize()
                transactions_ref.document(transaction_data['transaction_id']).set(transaction_data)

            # Save categories to Category subcollection
            categories_ref = user_ref.collection('Category')
            for category in self._categories:
                category_data = category.serialize()
                categories_ref.document(category_data['category_id']).set(category_data)

        except Exception as e:
            response.add_error(f"Failed to save data: {str(e)}")
            return response

        # Prepare payload details
        transactions_list = []
        for transaction in self._transactions:
            transactions_list.append(transaction.serialize())

        categories_list = []
        for cat in self._categories:
            categories_list.append(cat.serialize())

        # Set the payload with detailed saved information
        response_payload = self.serialize()
        response_payload['transactions'] = transactions_list
        response_payload['categories'] = categories_list
        response.set_payload(response_payload)

        return response
    
    @staticmethod
    def find(user_id: str) -> Response:
        """Finds a single user in the Firestore database by their user_id.

        This function queries the Firestore collection specified by the `User` class
        to locate a user with the given `user_id`. It returns a `Response` object 
        containing either the serialized user data or an error message.

        Args:
            user_id: A string representing the unique identifier (UUID) of the user to find.

        Returns:
            A Response object:
                - If the user is found, the `payload` attribute will contain a dictionary 
                  representing the serialized user data.
                - If no user is found, or multiple users are found with the same ID (an error condition),
                  the `errors` attribute will contain an error message.
                - The `is_successful()` method can be used to determine the success of the operation.

        Raises:
            google.cloud.exceptions.NotFound: If the specified collection does not exist.
            google.cloud.exceptions.FirebaseError: If there is an error communicating with Firestore.

        Example Usage:
            result = User.find("123e4567-e89b-12d3-a456-426614174000")
            if result.is_successful():
                user_data = result.get_payload()
                # Process user_data
            else:
                error_message = result.get_errors()
                # Handle the error
        """

        result = Response()  # Initialize a Response object

        # Query Firestore for documents with the matching user_id
        documents = db.collection(User.class_name).where('user_id', "==", user_id).get()
    
        # Handle different query result scenarios using pattern matching:
        match len(documents):
            case 0:  # No user found
                result.add_error(f"A user with id {user_id} doesn't exist.")
            case 1:  # Single user found
                user_instance: User = User.extract_subcollections(documents[0])
                result.set_payload(user_instance)
            case _:  # Multiple users found (shouldn't happen with unique IDs)
                result.add_error(f"More than one user with id {user_id} exists.")

        return result


    def update_user_in_firestore(self) -> Response:
        """Updates the user data in the Firestore database.
    
        This method assumes that the `User` object (`self`) has already been modified with the new data.
        It calls the `save_to_firestore()` method (not shown here) to persist the changes to Firestore.
        It then returns a `Response` object indicating the success of the operation.
    
        Args:
            self: The User object whose data will be updated in Firestore.
    
        Returns:
            A Response object:
                - If the update is successful, the `payload` attribute will contain a message
                  confirming the update.
                - If there is an error during the update process, the `errors` attribute will 
                  contain an error message.
                - Use the `is_successful()` method to determine the success or failure of the update.
    
        Raises:
            google.cloud.exceptions.FirebaseError: If there is an error communicating with Firestore.
            Other exceptions may be raised depending on the implementation of `save_to_firestore()`.
    
        Example Usage:
            user = User.get_by_id("123e4567-e89b-12d3-a456-426614174000")  # Assume you have a get_by_id method
            user.name = "New Name"
            result = user.update_user_in_firestore()
    
            if result.is_successful():
                print(result.get_payload())  # Output: "User 123e4567-e89b-12d3-a456-426614174000 was updated"
            else:
                print(f"Error updating user: {result.get_errors()}")
        """
    
        result = Response()  # Initialize the response object
    
        # Save the updated user data to Firestore
        self.save_to_firestore()  
    
        # Set a success message in the response payload
        result.set_payload(f"User {self.user_id} was updated")
        return result


    def remove(self) -> Response:
        result = Response()

        documents: [any] = db.collection(User.class_name).where('user_id', "==", self.user_id).get()
        if len(documents) == 0:
            result.add_error(f"A user with this id (${self.user_id} doesn't exist.")
            return result
        else:
            for doc in documents:
                doc.reference.delete()
            result.set_payload(f"This user was deleted: {self.user_id}")
            return result

    def is_authenticated(self) -> bool:
        return True
        # TODO UNCOMMENT AND DELETE LINE ABOVE BEFORE PUSH
        # try:
        #     # The decoded token will return a dictionary with key-value pairs for the user
        #     decoded_token = auth.verify_id_token(self._access_token)
        #     return True if decoded_token.get("uid") == self._user_id else False
        # except Exception as e:
        #     print(f"Token verification error: {str(e)}")
        #     return False

    def serialize(self) -> dict:
        return {
            'user_id': self._user_id,
            'access_token': self._access_token,
            'email': self._email,
            'first_name': self._first_name,
            'last_name': self._last_name,
            'created_at': self._created_at,
            'last_login': self._last_login,
            'admin': self._admin,
            'categories': self._categories,
            'transactions': self._transactions
        }


    def extract_subcollections(collection_ref) -> dict:
        """Extracts a Firestore document and its subcollections into a JSON-serializable dictionary.

        This function retrieves a Firestore document's data, then fetches data from
        its 'Category' and 'Transaction' subcollections. It combines all this data
        into a single dictionary, making it suitable for conversion to JSON.

        Args:
            collection_ref (google.cloud.firestore.DocumentSnapshot): 
                A reference to a Firestore document snapshot.

        Returns:
            dict: A dictionary containing:
                - The data from the original document.
                - A 'categories' key with a list of dictionaries representing the documents in the 'Category' subcollection.
                - A 'transaction' key with a list of dictionaries representing the documents in the 'Transaction' subcollection.

        Raises:
            google.cloud.exceptions.NotFound: If the document or subcollections do not exist.

        Example:
            doc_ref = db.collection('users').document('user_id_123')
            result = extract_subcollections(doc_ref)
            print(json.dumps(result, indent=2))  
        """

        doc_data = collection_ref.to_dict()

        # Retrieve data from 'Category' subcollection
        category_ref = collection_ref.reference.collection('Category')
        category_docs = [subdoc.to_dict() for subdoc in category_ref.stream()]  # Use stream() for efficiency
        doc_data['categories'] = category_docs  

        # Retrieve data from 'Transaction' subcollection
        transaction_ref = collection_ref.reference.collection('Transaction')
        transaction_docs = [subdoc.to_dict() for subdoc in transaction_ref.stream()]
        doc_data['transactions'] = transaction_docs  # Pluralized to match data structure

        return doc_data
