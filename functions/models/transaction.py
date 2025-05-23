from typing import Optional, Dict, Any
from datetime import datetime
import uuid
from protocols.transaction_protocol import TransactionProtocol

class Transaction(TransactionProtocol):
    """
    Represents a financial transaction with various attributes.

    Attributes are initialized during the instantiation of the class.
    """

    class_name = 'transactions'

    def __init__(self, data: Optional[Dict[str, Any]] = None):
        """
        Initializes a new Transaction instance.

        Args:
            data (Optional[Dict[str, Any]]): The data to initialize the transaction, typically from a dictionary.
        """
        self._transaction_id: Optional[uuid.UUID] = None
        self._created_at: Optional[datetime] = None
        self._email: Optional[str] = None
        self._amount: Optional[float] = None
        self._vendor: Optional[str] = None
        self._category_name: Optional[str] = None
        self._category_id: Optional[uuid.UUID] = None
        self._picture_id: Optional[uuid.UUID] = None
        self._is_successful: Optional[bool] = None

        if data:
            self._transaction_id = data.get('transaction_id')
            self._created_at = data.get('created_at')
            self._email = data.get('email') if data.get('email') else None
            self._amount = data.get('amount')
            self._vendor = data.get('vendor').strip().replace("  ", " ").lower() if data.get('vendor') else None
            self._category_name = data.get('category_name').strip().replace("  ", " ").lower() if data.get('category_name') else None
            self._category_id = data.get('category_id')
            self._picture_id = data.get('picture_id')
            self._is_successful = data.get('is_successful')

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
    def email(self) -> Optional[str]:
        """
        Gets the email of the transaction.

        Returns:
            Optional[str]: The email associated with the transaction.
        """
        return self._email if self._email else None

    @email.setter
    def email(self, value: str) -> None:
        """
        Sets the email of the transaction.

        Args:
            value (str): The email associated with the transaction.
        """
        self._email = value if value else None

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
        return self._vendor.strip().replace("  ", " ").lower() if self._vendor else None

    @vendor.setter
    def vendor(self, value: str) -> None:
        """
        Sets the vendor of the transaction.

        Args:
            value (str): The vendor associated with the transaction.
        """
        self._vendor = value.strip().replace("  ", " ").lower() if self._vendor else None

    @property
    def category_id(self) -> Optional[uuid.UUID]:
        """
        Gets the category ID of the transaction.

        Returns:
            Optional[uuid.UUID]: The unique identifier for the category of the transaction.
        """
        return self._category_id

    @property
    def category_name(self) -> Optional[str]:  # Added property
        """
        Gets the category name of the transaction.

        Returns:
            Optional[str]: The category name of the transaction.
        """
        return self._category_name.strip().replace("  ", " ").lower() if self._category_name else None

    @category_name.setter
    def category_name(self, value: str) -> None:  # Added setter
        """
        Sets the category name of the transaction.

        Args:
            value (str): The category name of the transaction.
        """
        self._category_name = value.strip().replace("  ", " ").lower() if self._category_name else None

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

    def serialize(self, getting_transaction: bool = True) -> dict:
        if getting_transaction:
            return {
                'transaction_id': str(self.transaction_id) if self.transaction_id else str(uuid.uuid4()),
                'created_at': self.created_at,
                'amount': self.amount,
                'vendor': self.vendor.strip().replace("  ", " ").lower() if self.vendor else None,
                'category_name': self.category_name.strip().replace("  ", " ").lower() if self.category_name else None,
                'category_id': str(self.category_id) if self.category_id else None,
                'picture_id': str(self.picture_id) if self.picture_id else None,
                'is_successful': self.is_successful
            }
        else:
            return {
                'transaction_id': str(self.transaction_id) if self.transaction_id else str(uuid.uuid4()),
                'created_at': self.created_at,
                'email': self.email if self.email else None,
                'amount': self.amount,
                'vendor': self.vendor.strip().replace("  ", " ").lower() if self.vendor else None,
                'category_name': self.category_name.strip().replace("  ", " ").lower() if self.category_name else None,
                'category_id': str(self.category_id) if self.category_id else None,
                'picture_id': str(self.picture_id) if self.picture_id else None,
                'is_successful': self.is_successful
            }
