from typing import Optional, Dict, Any
from datetime import datetime
import uuid
from backend.functions.protocols.transaction_protocol import TransactionProtocol


class Transaction(TransactionProtocol):
    """
    Represents a financial transaction with various attributes.

    Attributes:
        _transaction_id (Optional[uuid.UUID]): The unique identifier for the transaction.
        _created_at (Optional[datetime]): The date and time when the transaction was created.
        _amount (Optional[float]): The amount of money involved in the transaction.
        _vendor (Optional[str]): The vendor associated with the transaction.
        _category_id (Optional[uuid.UUID]): The unique identifier for the category of the transaction.
        _picture_id (Optional[uuid.UUID]): The unique identifier for the picture related to the transaction.
        _is_successful (Optional[bool]): Indicates whether the transaction was successful.
        _recheck (Optional[bool]): Indicates whether the transaction needs to be rechecked.
    """
    _transaction_id: Optional[uuid.UUID] = None
    _created_at: Optional[datetime] = None
    _amount: Optional[float] = None
    _vendor: Optional[str] = None
    _category_id: Optional[uuid.UUID] = None
    _picture_id: Optional[uuid.UUID] = None
    _is_successful: Optional[bool] = None
    _recheck: Optional[bool] = None

    def __init__(self, data: Optional[Dict[str, Any]] = None):
        """
        Initializes a new Transaction instance.

        Args:
            data (Optional[Dict[str, Any]]): The data to initialize the transaction, typically from a dictionary.
        """
        if data:
            self._transaction_id = data.get('transaction_id')
            self._created_at = data.get('created_at')
            self._amount = data.get('amount')
            self._vendor = data.get('vendor')
            self._category_id = data.get('category_id')
            self._picture_id = data.get('picture_id')
            self._is_successful = data.get('is_successful')
            self._recheck = data.get('recheck')

    @property
    def transaction_id(self) -> Optional[uuid.UUID]:
        """
        Gets the transaction ID.

        Returns:
            Optional[uuid.UUID]: The unique identifier of the transaction.
        """
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, value: uuid.UUID) -> None:
        """
        Sets the transaction ID.

        Args:
            value (uuid.UUID): The unique identifier for the transaction.
        """
        self._transaction_id = value

    @property
    def created_at(self) -> Optional[datetime]:
        """
        Gets the creation date and time of the transaction.

        Returns:
            Optional[datetime]: The date and time when the transaction was created.
        """
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime) -> None:
        """
        Sets the creation date and time of the transaction.

        Args:
            value (datetime): The date and time when the transaction was created.
        """
        self._created_at = value

    @property
    def amount(self) -> Optional[float]:
        """
        Gets the amount of the transaction.

        Returns:
            Optional[float]: The amount of money involved in the transaction.
        """
        return self._amount

    @amount.setter
    def amount(self, value: float) -> None:
        """
        Sets the amount of the transaction.

        Args:
            value (float): The amount of money involved in the transaction.
        """
        self._amount = value

    @property
    def vendor(self) -> Optional[str]:
        """
        Gets the vendor of the transaction.

        Returns:
            Optional[str]: The vendor associated with the transaction.
        """
        return self._vendor

    @vendor.setter
    def vendor(self, value: str) -> None:
        """
        Sets the vendor of the transaction.

        Args:
            value (str): The vendor associated with the transaction.
        """
        self._vendor = value

    @property
    def category_id(self) -> Optional[uuid.UUID]:
        """
        Gets the category ID of the transaction.

        Returns:
            Optional[uuid.UUID]: The unique identifier for the category of the transaction.
        """
        return self._category_id

    @category_id.setter
    def category_id(self, value: uuid.UUID) -> None:
        """
        Sets the category ID of the transaction.

        Args:
            value (uuid.UUID): The unique identifier for the category of the transaction.
        """
        self._category_id = value

    @property
    def picture_id(self) -> Optional[uuid.UUID]:
        """
        Gets the picture ID related to the transaction.

        Returns:
            Optional[uuid.UUID]: The unique identifier for the picture related to the transaction.
        """
        return self._picture_id

    @picture_id.setter
    def picture_id(self, value: uuid.UUID) -> None:
        """
        Sets the picture ID related to the transaction.

        Args:
            value (uuid.UUID): The unique identifier for the picture related to the transaction.
        """
        self._picture_id = value

    @property
    def is_successful(self) -> Optional[bool]:
        """
        Gets the success status of the transaction.

        Returns:
            Optional[bool]: Indicates whether the transaction was successful.
        """
        return self._is_successful

    @is_successful.setter
    def is_successful(self, value: bool) -> None:
        """
        Sets the success status of the transaction.

        Args:
            value (bool): Indicates whether the transaction was successful.
        """
        self._is_successful = value

    @property
    def recheck(self) -> Optional[bool]:
        """
        Gets the recheck status of the transaction.

        Returns:
            Optional[bool]: Indicates whether the transaction needs to be rechecked.
        """
        return self._recheck

    @recheck.setter
    def recheck(self, value: bool) -> None:
        """
        Sets the recheck status of the transaction.

        Args:
            value (bool): Indicates whether the transaction needs to be rechecked.
        """
        self._recheck = value
