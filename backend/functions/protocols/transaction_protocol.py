from typing import Protocol, Optional
from datetime import datetime
import uuid


class TransactionProtocol(Protocol):
    _transaction_id: Optional[uuid.UUID]
    _created_at: Optional[datetime]
    _amount: Optional[float]
    _vendor: Optional[str]
    _category_id: Optional[uuid.UUID]
    _picture_id: Optional[uuid.UUID]
    _is_successful: Optional[bool]
    _recheck: Optional[bool]

    @property
    def transaction_id(self) -> Optional[uuid.UUID]: ...

    @transaction_id.setter
    def transaction_id(self, value: uuid.UUID) -> None: ...

    @property
    def created_at(self) -> Optional[datetime]: ...

    @created_at.setter
    def created_at(self, value: datetime) -> None: ...

    @property
    def amount(self) -> Optional[float]: ...

    @amount.setter
    def amount(self, value: float) -> None: ...

    @property
    def vendor(self) -> Optional[str]: ...

    @vendor.setter
    def vendor(self, value: str) -> None: ...

    @property
    def category_id(self) -> Optional[uuid.UUID]: ...

    @category_id.setter
    def category_id(self, value: uuid.UUID) -> None: ...

    @property
    def picture_id(self) -> Optional[uuid.UUID]: ...

    @picture_id.setter
    def picture_id(self, value: uuid.UUID) -> None: ...

    @property
    def is_successful(self) -> Optional[bool]: ...

    @is_successful.setter
    def is_successful(self, value: bool) -> None: ...

    @property
    def recheck(self) -> Optional[bool]: ...

    @recheck.setter
    def recheck(self, value: bool) -> None: ...
