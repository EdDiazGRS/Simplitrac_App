import json
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
import uuid
import firebase_admin
from firebase_admin import firestore, credentials
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

    def __init__(self, data: Optional[Union[dict, uuid.UUID]] = None):
        """
        Initializes a new User instance.

        Args:
            data (Optional[Union[str, uuid.UUID]]): The data to initialize the user. Can be a JSON string or UUID.
        """
        self._user_id: Optional[uuid.UUID] = uuid.uuid4()
        self._google_id: Optional[str] = None
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
        elif isinstance(data, uuid.UUID):
            self._initialize_from_firestore(data)
        elif data is None:
            pass
        else:
            raise ValueError("Constructor requires either a JSON string or a UUID")

    def _initialize_from_data(self, data: Dict[str, Any]) -> None:
        """
        Initializes the user attributes from a dictionary of data.

        Args:
            data (Dict[str, Any]): The data to initialize the user.
        """
        self._user_id = uuid.UUID(data.get('user_id')) if data.get('user_id') else uuid.uuid4()
        self._google_id = data.get('google_id')
        self._email = data.get('email')
        self._first_name = data.get('first_name')
        self._last_name = data.get('last_name')
        self._created_at = data.get('created_at')
        self._last_login = data.get('last_login')
        self._admin = data.get('admin')

        if 'transactions' in data:
            self._transactions = [Transaction(tx) for tx in data['transactions']]
        if 'categories' in data:
            self._categories = [Category(cat) for cat in data['categories']]

    def _initialize_from_firestore(self, user_id: uuid.UUID) -> None:
        """
        Fetches and initializes the user data from Firestore using the provided UUID.

        Args:
            user_id (uuid.UUID): The unique identifier of the user in Firestore.
        """
        user_ref = db.collection(self.class_name).document(str(user_id))
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
    def user_id(self) -> Optional[uuid.UUID]:
        """Gets the user ID."""
        return self._user_id

    @user_id.setter
    def user_id(self, value: uuid.UUID) -> None:
        """Sets the user ID."""
        self._user_id = value

    @property
    def google_id(self) -> Optional[str]:
        """Gets the Google ID of the user."""
        return self._google_id

    @google_id.setter
    def google_id(self, value: str) -> None:
        """Sets the Google ID of the user."""
        self._google_id = value

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
        result = Response()

        documents: [any] = db.collection(User.class_name).where('user_id', "==", str(user_id)).get()
        if len(documents) == 0:
            result.add_error(f"A user with this id (${user_id} doesn't exist.")
            return result
        else:
            # print(f"Here is the document: {documents[0]}")
            user: Dict[str, str] = documents[0].to_dict()
            # print(f"Here is the user: {user}")
            result.set_payload(User(user))
            return result

    def update_user_in_firestore(self) -> Response:
        result = Response()

        self.save_to_firestore()

        result.set_payload(f"This user was updated: {self.user_id}")
        return result

    def serialize(self) -> dict:
        return {
            'user_id': str(self._user_id),
            'google_id': self._google_id,
            'email': self._email,
            'first_name': self._first_name,
            'last_name': self._last_name,
            'created_at': self._created_at,
            'last_login': self._last_login,
            'admin': self._admin
        }
