import json  # Import for parsing JSON strings
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
import uuid
import firebase_admin
from firebase_admin import firestore, credentials

# Initialize Firebase Admin SDK (assuming proper credentials setup)
cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

class User:
    """
    
    """
    def __init__(self, data: Optional[Union[str, uuid.UUID]] = None):
        self._user_id: Optional[uuid.UUID] = None
        self._google_id: Optional[str] = None
        self._email: Optional[str] = None
        self._first_name: Optional[str] = None
        self._last_name: Optional[str] = None
        self._created_at: Optional[datetime] = None
        self._last_login: Optional[datetime] = None
        self._transaction_id: Optional[uuid.UUID] = None
        self._category_id: Optional[uuid.UUID] = None
        self._admin: Optional[bool] = None
        self._transactions: List['Transaction'] = []
        self._categories: List['Category'] = []

        if isinstance(data, str):
            # If data is a JSON string, parse it into a dictionary
            try:
                parsed_data = json.loads(data)
                self._initialize_from_data(parsed_data)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON string provided")
        elif isinstance(data, uuid.UUID):
            # If data is a UUID, fetch from Firestore
            self._initialize_from_firestore(data)
        else:
            raise ValueError("Constructor requires either a JSON string or a UUID")

    def _initialize_from_data(self, data: Dict[str, Any]) -> None:
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
            self._transactions = [Transaction(tx) for tx in data['transactions']]
        if 'categories' in data:
            self._categories = [Category(cat) for cat in data['categories']]

    def _initialize_from_firestore(self, user_id: uuid.UUID) -> None:
        user_ref = db.collection('User').document(str(user_id))
        user_doc = user_ref.get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            self._initialize_from_data(user_data)
            self._user_id = user_id
            self._fetch_subcollections()

    def _fetch_subcollections(self) -> None:
        if self._user_id:
            transactions_ref = db.collection('User').document(str(self._user_id)).collection('Transaction')
            transaction_docs = transactions_ref.stream()
            self._transactions = [Transaction(doc.to_dict()) for doc in transaction_docs]

            categories_ref = db.collection('User').document(str(self._user_id)).collection('Category')
            category_docs = categories_ref.stream()
            self._categories = [Category(doc.to_dict()) for doc in category_docs]

    @property
    def user_id(self) -> Optional[uuid.UUID]:
        return self._user_id
    
    @user_id.setter
    def user_id(self, value: uuid.UUID) -> None:
        self._user_id = value

    @property
    def google_id(self) -> Optional[str]:
        return self._google_id
    
    @google_id.setter
    def google_id(self, value: str) -> None:
        self._google_id = value
    
    @property
    def email(self) -> Optional[str]:
        return self._email
    
    @email.setter
    def email(self, value: str) -> None:
        self._email = value
    
    @property
    def first_name(self) -> Optional[str]:
        return self._first_name
    
    @first_name.setter
    def first_name(self, value: str) -> None:
        self._first_name = value
    
    @property
    def last_name(self) -> Optional[str]:
        return self._last_name
    
    @last_name.setter
    def last_name(self, value: str) -> None:
        self._last_name = value
    
    @property
    def created_at(self) -> Optional[datetime]:
        return self._created_at
    
    @created_at.setter
    def created_at(self, value: datetime) -> None:
        self._created_at = value
    
    @property
    def last_login(self) -> Optional[datetime]:
        return self._last_login
    
    @last_login.setter
    def last_login(self, value: datetime) -> None:
        self._last_login = value
    
    @property
    def transaction_id(self) -> Optional[uuid.UUID]:
        return self._transaction_id
    
    @transaction_id.setter
    def transaction_id(self, value: uuid.UUID) -> None:
        self._transaction_id = value
    
    @property
    def category_id(self) -> Optional[uuid.UUID]:
        return self._category_id
    
    @category_id.setter
    def category_id(self, value: uuid.UUID) -> None:
        self._category_id = value
    
    @property
    def admin(self) -> Optional[bool]:
        return self._admin
    
    @admin.setter
    def admin(self, value: bool) -> None:
        self._admin = value
    
    @property
    def transactions(self) -> List[Transaction]:
        return self._transactions
    
    @transactions.setter
    def transactions(self, value: List[Transaction]) -> None:
        self._transactions = value
    
    @property
    def categories(self) -> List[Category]:
        return self._categories
    
    @categories.setter
    def categories(self, value: List[Category]) -> None:
        self._categories = value

    def add_transaction(self, transaction_data: Dict[str, Any]) -> None:
        transaction = Transaction(transaction_data)
        self._transactions.append(transaction)
    
    def add_category(self, category_data: Dict[str, Any]) -> None:
        category = Category(category_data)
        self._categories.append(category)

