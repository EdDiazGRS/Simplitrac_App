
class Transaction:
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        self._transaction_id: Optional[uuid.UUID] = None
        self._created_at: Optional[datetime] = None
        self._amount: Optional[float] = None
        self._vendor: Optional[str] = None
        self._category_id: Optional[uuid.UUID] = None
        self._picture_id: Optional[uuid.UUID] = None
        self._is_successful: Optional[bool] = None
        self._recheck: Optional[bool] = None
        
        if data:
            self._transaction_id = data.get('transaction_id')
            self._created_at = data.get('created_at')
            self._amount = data.get('amount')
            self._vendor = data.get('vendor')
            self._category_id = data.get('category_id')
            self._picture_id = data.get('picture_id')
            self._is_successful = data.get('is_successful')
            self._recheck = data.get('recheck')

    # Property Decorators for getters and setters
    @property
    def transaction_id(self) -> Optional[uuid.UUID]:
        return self._transaction_id
    
    @transaction_id.setter
    def transaction_id(self, value: uuid.UUID) -> None:
        self._transaction_id = value

    @property
    def created_at(self) -> Optional[datetime]:
        return self._created_at
    
    @created_at.setter
    def created_at(self, value: datetime) -> None:
        self._created_at = value

    @property
    def amount(self) -> Optional[float]:
        return self._amount
    
    @amount.setter
    def amount(self, value: float) -> None:
        self._amount = value
    
    @property
    def vendor(self) -> Optional[str]:
        return self._vendor
    
    @vendor.setter
    def vendor(self, value: str) -> None:
        self._vendor = value
    
    @property
    def category_id(self) -> Optional[uuid.UUID]:
        return self._category_id
    
    @category_id.setter
    def category_id(self, value: uuid.UUID) -> None:
        self._category_id = value

    @property
    def picture_id(self) -> Optional[uuid.UUID]:
        return self._picture_id
    
    @picture_id.setter
    def picture_id(self, value: uuid.UUID) -> None:
        self._picture_id = value
    
    @property
    def is_successful(self) -> Optional[bool]:
        return self._is_successful
    
    @is_successful.setter
    def is_successful(self, value: bool) -> None:
        self._is_successful = value
    
    @property
    def recheck(self) -> Optional[bool]:
        return self._recheck
    
    @recheck.setter
    def recheck(self, value: bool) -> None:
        self._recheck = value
