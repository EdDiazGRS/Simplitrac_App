import json
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
import uuid
import firebase_admin
from firebase_admin import firestore, credentials
from protocols.user_protocol import UserProtocol
from protocols.category_protocol import CategoryProtocol
from protocols.transaction_protocol import TransactionProtocol
from dotenv import load_dotenv

import os
load_dotenv()

# Initialize Firebase Admin SDK (assuming proper credentials setup)
import firebase_admin
from firebase_admin import credentials, firestore

# Use a service account

firebase_service_account = os.getenv('FIREBASE_SERVICE_ACCOUNT')
firebase_config = json.loads(firebase_service_account)
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)

db = firestore.client()

class User(UserProtocol):
    """
    Represents a user with personal information and associated transactions and categories.

    Attributes:
        _user_id (Optional[uuid.UUID]): The unique identifier for the user.
        _google_id (Optional[str]): The Google ID of the user.
        _email (Optional[str]): The email address of the user.
        _first_name (Optional[str]): The first name of the user.
        _last_name (Optional[str]): The last name of the user.
        _created_at (Optional[datetime]): The date and time when the user was created.
        _last_login (Optional[datetime]): The date and time of the user's last login.
        _transaction_id (Optional[uuid.UUID]): The unique identifier for the user's transaction.
        _category_id (Optional[uuid.UUID]): The unique identifier for the user's category.
        _admin (Optional[bool]): Indicates whether the user has admin privileges.
        _transactions (List[TransactionProtocol]): A list of transactions associated with the user.
        _categories (List[CategoryProtocol]): A list of categories associated with the user.
    """
    # USING UUID 4 because it creates a randon UUID, which does not use the computers network address
    _user_id: Optional[uuid.UUID] = uuid.uuid4
    _google_id: Optional[str] = None
    _email: Optional[str] = None
    _first_name: Optional[str] = None
    _last_name: Optional[str] = None
    _created_at: Optional[datetime] = None
    _last_login: Optional[datetime] = None
    _transaction_id: Optional[uuid.UUID] = None
    _category_id: Optional[uuid.UUID] = None
    _admin: Optional[bool] = None
    _transactions: List[TransactionProtocol] = []
    _categories: List[CategoryProtocol] = []

    def __init__(self, data: Optional[Union[str, uuid.UUID]] = None):
        """
        Initializes a new User instance.

        Args:
            data (Optional[Union[str, uuid.UUID]]): The data to initialize the user. Can be a JSON string or UUID.
        """
        if isinstance(data, str):
            try:
                parsed_data = json.loads(data)
                self._initialize_from_data(parsed_data)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON string provided")
        elif isinstance(data, uuid.UUID):
            self._initialize_from_firestore(data)
        else:
            raise ValueError("Constructor requires either a JSON string or a UUID")

    def _initialize_from_data(self, data: Dict[str, Any]) -> None:
        """
        Initializes the user attributes from a dictionary of data.

        Args:
            data (Dict[str, Any]): The data to initialize the user.
        """
        self._user_id = data.get('user_id')
        self._google_id = data.get('google_id')
        self._email = data.get('email')
        self._first_name = data.get('first_name')
        self._last_name = data.get('last_name')
        self._created_at = data.get('created_at')
        self._last_login = data.get('last_login')
        self._transaction_id = data.get('transaction_id')
        self._category_id = data.get('category_id')
        self._admin = data.get('admin')
        
        if 'transactions' in data:
            self._transactions = [TransactionProtocol(tx) for tx in data['transactions']]
        if 'categories' in data:
            self._categories = [CategoryProtocol(cat) for cat in data['categories']]

    def _initialize_from_firestore(self, user_id: uuid.UUID) -> None:
        """
        Fetches and initializes the user data from Firestore using the provided UUID.

        Args:
            user_id (uuid.UUID): The unique identifier of the user in Firestore.
        """
        user_ref = db.collection('User').document(str(user_id))
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
            transactions_ref = db.collection('User').document(str(self._user_id)).collection('Transaction')
            transaction_docs = transactions_ref.stream()
            self._transactions = [TransactionProtocol(doc.to_dict()) for doc in transaction_docs]

            categories_ref = db.collection('User').document(str(self._user_id)).collection('Category')
            category_docs = categories_ref.stream()
            self._categories = [CategoryProtocol(doc.to_dict()) for doc in category_docs]

    @property
    def user_id(self) -> Optional[uuid.UUID]:
        """
        Gets the user ID.

        Returns:
            Optional[uuid.UUID]: The unique identifier of the user.
        """
        return self._user_id
    
    @user_id.setter
    def user_id(self, value: uuid.UUID) -> None:
        """
        Sets the user ID.

        Args:
            value (uuid.UUID): The unique identifier for the user.
        """
        self._user_id = value

    @property
    def google_id(self) -> Optional[str]:
        """
        Gets the Google ID of the user.

        Returns:
            Optional[str]: The Google ID of the user.
        """
        return self._google_id
    
    @google_id.setter
    def google_id(self, value: str) -> None:
        """
        Sets the Google ID of the user.

        Args:
            value (str): The Google ID of the user.
        """
        self._google_id = value
    
    @property
    def email(self) -> Optional[str]:
        """
        Gets the email of the user.

        Returns:
            Optional[str]: The email address of the user.
        """
        return self._email
    
    @email.setter
    def email(self, value: str) -> None:
        """
        Sets the email of the user.

        Args:
            value (str): The email address of the user.
        """
        self._email = value
    
    @property
    def first_name(self) -> Optional[str]:
        """
        Gets the first name of the user.

        Returns:
            Optional[str]: The first name of the user.
        """
        return self._first_name
    
    @first_name.setter
    def first_name(self, value: str) -> None:
        """
        Sets the first name of the user.

        Args:
            value (str): The first name of the user.
        """
        self._first_name = value
    
    @property
    def last_name(self) -> Optional[str]:
        """
        Gets the last name of the user.

        Returns:
            Optional[str]: The last name of the user.
        """
        return self._last_name
    
    @last_name.setter
    def last_name(self, value: str) -> None:
        """
        Sets the last name of the user.

        Args:
            value (str): The last name of the user.
        """
        self._last_name = value
    
    @property
    def created_at(self) -> Optional[datetime]:
        """
        Gets the creation date and time of the user.

        Returns:
            Optional[datetime]: The date and time when the user was created.
        """
        return self._created_at
    
    @created_at.setter
    def created_at(self, value: datetime) -> None:
        """
        Sets the creation date and time of the user.

        Args:
            value (datetime): The date and time when the user was created.
        """
        self._created_at = value
    
    @property
    def last_login(self) -> Optional[datetime]:
        """
        Gets the last login date and time of the user.

        Returns:
            Optional[datetime]: The date and time of the user's last login.
        """
        return self._last_login
    
    @last_login.setter
    def last_login(self, value: datetime) -> None:
        """
        Sets the last login date and time of the user.

        Args:
            value (datetime): The date and time of the user's last login.
        """
        self._last_login = value
    
    @property
    def transaction_id(self) -> Optional[uuid.UUID]:
        """
        Gets the transaction ID of the user.

        Returns:
            Optional[uuid.UUID]: The unique identifier for the user's transaction.
        """
        return self._transaction_id
    
    @transaction_id.setter
    def transaction_id(self, value: uuid.UUID) -> None:
        """
        Sets the transaction ID of the user.

        Args:
            value (uuid.UUID): The unique identifier for the user's transaction.
        """
        self._transaction_id = value
    
    @property
    def category_id(self) -> Optional[uuid.UUID]:
        """
        Gets the category ID of the user.

        Returns:
            Optional[uuid.UUID]: The unique identifier for the user's category.
        """
        return self._category_id
    
    @category_id.setter
    def category_id(self, value: uuid.UUID) -> None:
        """
        Sets the category ID of the user.

        Args:
            value (uuid.UUID): The unique identifier for the user's category.
        """
        self._category_id = value
    
    @property
    def admin(self) -> Optional[bool]:
        """
        Gets the admin status of the user.

        Returns:
            Optional[bool]: Indicates whether the user has admin privileges.
        """
        return self._admin
    
    @admin.setter
    def admin(self, value: bool) -> None:
        """
        Sets the admin status of the user.

        Args:
            value (bool): Indicates whether the user has admin privileges.
        """
        self._admin = value
    
    @property
    def transactions(self) -> List[TransactionProtocol]:
        """
        Gets the list of transactions associated with the user.

        Returns:
            List[TransactionProtocol]: A list of transactions.
        """
        return self._transactions
    
    @transactions.setter
    def transactions(self, value: List[TransactionProtocol]) -> None:
        """
        Sets the list of transactions associated with the user.

        Args:
            value (List[TransactionProtocol]): A list of transactions.
        """
        self._transactions = value
    
    @property
    def categories(self) -> List[CategoryProtocol]:
        """
        Gets the list of categories associated with the user.

        Returns:
            List[CategoryProtocol]: A list of categories.
        """
        return self._categories
    
    @categories.setter
    def categories(self, value: List[CategoryProtocol]) -> None:
        """
        Sets the list of categories associated with the user.

        Args:
            value (List[CategoryProtocol]): A list of categories.
        """
        self._categories = value

    def add_transaction(self, transaction_data: Dict[str, Any]) -> None:
        """
        Adds a transaction to the user's list of transactions.

        Args:
            transaction_data (Dict[str, Any]): The data for the new transaction.
        """
        transaction = TransactionProtocol(transaction_data)
        self._transactions.append(transaction)
    
    def add_category(self, category_data: Dict[str, Any]) -> None:
        """
        Adds a category to the user's list of categories.

        Args:
            category_data (Dict[str, Any]): The data for the new category.
        """
        category = CategoryProtocol(category_data)
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

        user_data = {
            'user_id': str(self._user_id),
            'google_id': self._google_id,
            'email': self._email,
            'first_name': self._first_name,
            'last_name': self._last_name,
            'created_at': self._created_at,
            'last_login': self._last_login,
            'transaction_id': str(self._transaction_id) if self._transaction_id else None,
            'category_id': str(self._category_id) if self._category_id else None,
            'admin': self._admin
        }

        try:
            # Save to User collection
            user_ref = db.collection('User').document(str(self._user_id))
            user_ref.set(user_data)
        except firestore.FirestoreError as e:
            response.add_error(f"Failed to save user data: {str(e)}")
            return response

        try:
            # Save transactions to Transaction subcollection
            transactions_ref = user_ref.collection('Transaction')
            for transaction in self._transactions:
                transaction_data = {
                    'transaction_id': str(transaction.transaction_id) if transaction.transaction_id else None,
                    'created_at': transaction.created_at,
                    'amount': transaction.amount,
                    'vendor': transaction.vendor,
                    'category_id': str(transaction.category_id) if transaction.category_id else None,
                    'picture_id': str(transaction.picture_id) if transaction.picture_id else None,
                    'is_successful': transaction.is_successful,
                    'recheck': transaction.recheck
                }
                if transaction.transaction_id:
                    transactions_ref.document(str(transaction.transaction_id)).set(transaction_data)
        except firestore.FirestoreError as e:
            response.add_error(f"Failed to save transactions data: {str(e)}")
            return response

        try:
            # Save categories to Category subcollection
            categories_ref = user_ref.collection('Category')
            for category in self._categories:
                category_data = {
                    'category_id': str(category.category_id) if category.category_id else None,
                    'category_name': category.category_name
                }
                if category.category_id:
                    categories_ref.document(str(category.category_id)).set(category_data)
        except firestore.FirestoreError as e:
            response.add_error(f"Failed to save categories data: {str(e)}")
            return response

        # Prepare payload details
        transactions_list = []
        for tx in self._transactions:
            transactions_list.append({
                'transaction_id': str(tx.transaction_id) if tx.transaction_id else None,
                'created_at': tx.created_at,
                'amount': tx.amount,
                'vendor': tx.vendor,
                'category_id': str(tx.category_id) if tx.category_id else None,
                'picture_id': str(tx.picture_id) if tx.picture_id else None,
                'is_successful': tx.is_successful,
                'recheck': tx.recheck
            })

        categories_list = []
        for cat in self._categories:
            categories_list.append({
                'category_id': str(cat.category_id) if cat.category_id else None,
                'category_name': cat.category_name
            })

        # Set the payload with detailed saved information
        response_payload = {
            'user_data': user_data,
            'transactions': transactions_list,
            'categories': categories_list
        }
        response.set_payload(response_payload)

        return response
