from typing import Protocol, Optional, List
from datetime import datetime
import uuid
from .category_protocol import CategoryProtocol
from .transaction_protocol import TransactionProtocol

class UserProtocol(Protocol):
    _user_id: Optional[uuid.UUID]
    _google_id: Optional[str]
    _email: Optional[str]
    _first_name: Optional[str]
    _last_name: Optional[str]
    _created_at: Optional[datetime]
    _last_login: Optional[datetime]
    _transaction_id: Optional[uuid.UUID]
    _category_id: Optional[uuid.UUID]
    _admin: Optional[bool]
    _transactions: List[TransactionProtocol]
    _categories: List[CategoryProtocol]
    
    @property
    def user_id(self) -> Optional[uuid.UUID]: ...
    
    @user_id.setter
    def user_id(self, value: uuid.UUID) -> None: ...
    
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
    def transaction_id(self) -> Optional[uuid.UUID]: ...
    
    @transaction_id.setter
    def transaction_id(self, value: uuid.UUID) -> None: ...
    
    @property
    def category_id(self) -> Optional[uuid.UUID]: ...
    
    @category_id.setter
    def category_id(self, value: uuid.UUID) -> None: ...
    
    @property
    def admin(self) -> Optional[bool]: ...
    
    @admin.setter
    def admin(self, value: bool) -> None: ...
    
    @property
    def transactions(self) -> List[TransactionProtocol]: ...
    
    @transactions.setter
    def transactions(self, value: List[TransactionProtocol]) -> None: ...
    
    @property
    def categories(self) -> List[CategoryProtocol]: ...
    
    @categories.setter
    def categories(self, value: List[CategoryProtocol]) -> None: ...
