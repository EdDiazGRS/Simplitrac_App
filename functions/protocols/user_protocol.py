from typing import Protocol, Optional, List
from datetime import datetime
import uuid

from models.category import Category
from models.response import Response
from models.transaction import Transaction


class UserProtocol(Protocol):
    _user_id: Optional[str]
    _access_token: Optional[str]
    _email: Optional[str]
    _first_name: Optional[str]
    _last_name: Optional[str]
    _created_at: Optional[datetime]
    _last_login: Optional[datetime]
    _transaction_id: Optional[str]
    _category_id: Optional[str]
    _admin: Optional[bool]
    _transactions: List[Transaction]
    _categories: List[Category]

    @property
    def user_id(self) -> Optional[str]: ...

    @user_id.setter
    def user_id(self, value: str) -> None: ...

    @property
    def access_token(self) -> Optional[str]: ...

    @access_token.setter
    def access_token(self, value: str) -> None: ...

    @property
    def google_id(self) -> Optional[str]: ...

    @google_id.setter
    def google_id(self, value: str) -> None: ...

    @property
    def email(self) -> Optional[str]: ...

    @email.setter
    def email(self, value: str) -> None: ...

    @property
    def first_name(self) -> Optional[str]: ...

    @first_name.setter
    def first_name(self, value: str) -> None: ...

    @property
    def last_name(self) -> Optional[str]: ...

    @last_name.setter
    def last_name(self, value: str) -> None: ...

    @property
    def created_at(self) -> Optional[datetime]: ...

    @created_at.setter
    def created_at(self, value: datetime) -> None: ...

    @property
    def last_login(self) -> Optional[datetime]: ...

    @last_login.setter
    def last_login(self, value: datetime) -> None: ...

    @property
    def transaction_id(self) -> Optional[str]: ...

    @transaction_id.setter
    def transaction_id(self, value: str) -> None: ...

    @property
    def category_id(self) -> Optional[str]: ...

    @category_id.setter
    def category_id(self, value: str) -> None: ...

    @property
    def admin(self) -> Optional[bool]: ...

    @admin.setter
    def admin(self, value: bool) -> None: ...

    @property
    def transactions(self) -> List[Transaction]: ...

    @transactions.setter
    def transactions(self, value: List[Transaction]) -> None: ...

    @property
    def categories(self) -> List[Category]: ...

    @categories.setter
    def categories(self, value: List[Category]) -> None: ...

    def save_to_firestore(self) -> Response: ...

    def serialize(self) -> dict: ...

    def update_user_in_firestore(self) -> Response: ...

    def is_authenticated(self) -> bool: ...