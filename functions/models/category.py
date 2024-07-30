from typing import Optional, Dict, Any
import uuid
from protocols.category_protocol import CategoryProtocol


class Category(CategoryProtocol):
    """
    Represents a category with an identifier and name.

    Attributes:
        _category_id (Optional[uuid.UUID]): The unique identifier for the category.
        _category_name (Optional[str]): The name of the category.
    """

    class_name = "categories"

    _category_id: Optional[uuid.UUID] = None
    _category_name: Optional[str] = None

    def __init__(self, data: Optional[Dict[str, Any]] = None):
        """
        Initializes a new Category instance.

        Args:
            data (Optional[Dict[str, Any]]): The data to initialize the category, typically from a dictionary.
        """
        if data:
            self._category_id = data.get('category_id')
            self._category_name = data.get('category_name').strip().replace("  ", " ").capitalize() if data.get('category_name') else None

    @property
    def category_id(self) -> Optional[uuid.UUID]:
        """
        Gets the category ID.

        Returns:
            Optional[uuid.UUID]: The unique identifier of the category.
        """
        return self._category_id

    @category_id.setter
    def category_id(self, value: uuid.UUID) -> None:
        """
        Sets the category ID.

        Args:
            value (uuid.UUID): The unique identifier for the category.
        """
        self._category_id = value

    @property
    def category_name(self) -> Optional[str]:
        """
        Gets the category name.

        Returns:
            Optional[str]: The name of the category.
        """
        return self._category_name.strip().replace("  ", " ").capitalize() if self._category_name else None

    @category_name.setter
    def category_name(self, value: str) -> None:
        """
        Sets the category name.

        Args:
            value (str): The name of the category.
        """
        self._category_name = value.strip().replace("  ", " ").capitalize()

    def serialize(self) -> dict:
        return {
                    'category_id': str(self.category_id) if self.category_id else str(uuid.uuid4()),
                    'category_name': self.category_name.strip().replace("  ", " ").capitalize() if self._category_name else None
                }