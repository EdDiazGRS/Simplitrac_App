import json
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
import firebase_admin
from firebase_admin import firestore, credentials, auth
import os

from google.api_core.exceptions import InvalidArgument, PermissionDenied
from google.cloud.firestore_v1 import FieldFilter

from models.category import Category
from models.transaction import Transaction
from protocols.user_protocol import UserProtocol
from models.response import Response
import uuid

# Load environment variables
from dotenv import load_dotenv
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

    class_name = "Users"

    def __init__(self, data: Optional[Union[dict, str]] = None):
        """
        Initializes a new User instance.

        Args:
            data (Optional[Union[str, Any]]): The data to initialize the user. Can be a JSON string or str.
        """
        self._user_id: Optional[str] = None
        self._access_token: Optional[str] = None
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
            self._fetch_subcollections()
           
    def _fetch_subcollections(self) -> None:
        """
        Fetches and initializes the transactions and categories subcollections from Firestore,
        adding them to the `user_data` dictionary.
        """
        if self._user_id:
            transactions_ref = db.collection(self.class_name).document(str(self._user_id)).collection(Transaction.class_name)
            transaction_docs = transactions_ref.stream()
            for doc in transaction_docs:
                transaction = doc.to_dict()
                transaction.pop('email')
                self._transactions.append(transaction)

            categories_ref = db.collection(self.class_name).document(str(self._user_id)).collection(Category.class_name)
            category_docs = categories_ref.stream()
            self._categories.extend(doc.to_dict() for doc in category_docs)


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

        # Prepare payload details
        transactions_list = []
        categories_list = []

        # iterate over all categories, check if all have a category_id
        for cat in self._categories:
            # check if category has a category_id
            if not cat._category_id:
                # if no category_id, search for category name in firebase
                # category = db.collection_group(Category.class_name).where('category_name', '==', cat._category_name).get()
                query_result = db.collection_group(Category.class_name).where(filter=FieldFilter('category_name', '==', cat._category_name))

                category = None
                try:
                    category = query_result.get()
                except PermissionDenied as e:
                    print(f"Permission Denied: {e}")
                except InvalidArgument as e:
                    print(f"Invalid Argument: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")

                # remove duplicate category_id by assigning to set
                cat_set = set()
                cat_id_list = []
                if category:
                    for c in category:
                        cat_set.add(c.to_dict()['category_id'])
                    cat_id_list.append(list(cat_set))

                match len(cat_id_list):
                    # if category_name doesn't exist, create new category_id
                    case 0:
                        cat._category_id = str(uuid.uuid4())
                    # if category_name exists, assign existing category_id
                    case 1:
                        cat._category_id = cat_id_list[0]
                    # There should never be more than one category returned
                    case _:
                        response.add_error(f"{len(cat_id_list)} category entries with same name found on Firebase.")
                        return response
            categories_list.append(cat.serialize())

        # convert categories to dict for O1 efficiency
        cat_dict = {}
        for c in categories_list:
            cat_dict.update({f"{c.get('category_name')}":f"{c.get('category_id')}"})

        # iterate over all transactions
        for transaction in self._transactions:
            # check if transaction has a category_id
            if not transaction._category_id:
                # Assign category_id
                transaction._category_id = cat_dict.get(transaction._category_name)
            transaction._email = self._email
            transactions_list.append(transaction.serialize(False))

        try:
            # Save to User collection
            user_ref = db.collection(self.class_name).document(str(self._user_id))
            user_ref.set(self.serialize(False)) # not getting_existing_user()

            # Save transactions to Transaction subcollection
            transactions_ref = user_ref.collection(Transaction.class_name)
            for transaction in self._transactions:
                transaction_data = transaction.serialize(False)
                transactions_ref.document(transaction_data['transaction_id']).set(transaction_data)

            # Save categories to Category subcollection
            categories_ref = user_ref.collection(Category.class_name)
            for category in self._categories:
                category_data = category.serialize()
                categories_ref.document(category_data['category_id']).set(category_data)

        except Exception as e:
            response.add_error(f"Failed to save data: {str(e)}")
            return response

        # Set the payload with detailed saved information
        response_payload = self.serialize(False) # not getting_existing_user()
        response_payload[Transaction.class_name] = transactions_list
        response_payload[Category.class_name] = categories_list
        response.set_payload(response_payload)

        return response
 
    def remove(user_id: str) -> Response:
        """Removes a user from the Firestore database.
    
        This function searches for a user with the specified `user_id` in the 
        Firestore collection designated by `User.class_name`. If a single matching user
        is found, it is deleted. The function returns a `Response` object indicating 
        the success or failure of the operation.
    
        Args:
            user_id: The unique identifier (UUID) of the user to remove.
    
        Returns:
            Response: An object indicating the outcome of the operation:
                - If successful, the `payload` attribute will contain a message confirming the deletion.
                - If the user is not found or if multiple users with the same ID exist (unexpected),
                  the `errors` attribute will contain an error message.
                - Use the `is_successful()` method to determine the outcome.
    
        Raises:
            google.cloud.exceptions.FirebaseError: If there's an error communicating with Firestore.
    
        Example Usage:
            result = remove("123e4567-e89b-12d3-a456-426614174000") 
            if result.is_successful():
                print(result.get_payload())  
            else:
                print(f"Error deleting user: {result.get_errors()}") 
        """
        result = Response()
        
        # Query for the user document
        document = db.collection(User.class_name).document(user_id).get()

        if not document.exists:
            result.add_error(f"A user with id {user_id} doesn't exist.")
        else:
            document.reference.delete()
            result.set_payload({'message':'User account deleted.'}) # Updated message for consistency
  
        return result

    def delete_transactions(self) -> Response:
        """
        Deletes transactions on the Firestore database.
    
        Returns:
            Response: An object indicating the outcome of the operation:
        """
        result = Response()
        
        # Query for the user document
        document = db.collection(self.class_name).document(self.user_id).collection(Transaction.class_name).get()
        if document:
            for doc in document:
                doc.reference.delete()
        
        result = self.save_to_firestore()

        return result

    def delete_category(self, data: dict) -> Response:
        """
        Deletes transactions on the Firestore database.
    
        Returns:
            Response: An object indicating the outcome of the operation:
        """
        result = Response()

        # Query for the user document
        document = db.collection(User.class_name).document(data['user_id']).collection(Category.class_name).document(data['category_id'])

        if document:
            document.delete()
        
        result.set_payload(self)

        return result

    # TODO TURN OFF WHEN DEBUGGING
    def is_authenticated(self) -> bool:
        """Verifies if the user is authenticated using a Firebase ID token.

        This method attempts to verify the `access_token` associated with the user
        using Firebase Authentication. It compares the user ID (UID) extracted from 
        the decoded token with the user's stored `user_id` attribute.

        Returns:
            bool: True if the token is valid and the UIDs match, indicating the user is authenticated; 
                  False otherwise.
        """
        # print('inside auth')
        # try:
        #     # The decoded token will return a dictionary with key-value pairs for the user
        #     decoded_token = auth.verify_id_token(self._access_token)
        #     return True if decoded_token.get("uid") == self._user_id else False
        # except Exception as e:
        #     print(f"Token verification error: {str(e)}")
        #     return False

        return True


    def serialize(self, getting_user: bool = False) -> dict:
    # def serialize(self, getting_user: bool = False) -> str:
        """Serializes a User object into a dictionary for JSON representation.

        This method converts a User object's attributes into a dictionary format,
        making it suitable for serialization into JSON. The serialization behavior
        can be customized based on the `getting_user` flag:

        - If `getting_user` is True, the serialized dictionary will include all user attributes,
          including subcollections (e.g., 'categories' and 'transactions').
        - If `getting_user` is False (default), the subcollections will be excluded from the serialization.

        Args:
            getting_user (bool, optional): Determines whether to include subcollections in the output.
                                          Defaults to False.

        Returns:
            dict: A dictionary representation of the User object, with keys corresponding to attributes
                  and values representing their serialized values.
        """
        if getting_user:
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
        else:
            return {
                'user_id': self._user_id,
                'access_token': self._access_token,
                'email': self._email,
                'first_name': self._first_name,
                'last_name': self._last_name,
                'created_at': self._created_at,
                'last_login': self._last_login,
                'admin': self._admin
            }
