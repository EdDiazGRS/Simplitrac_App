from typing import Protocol, Optional
import uuid


class CategoryProtocol(Protocol):
    _category_id: Optional[uuid.UUID]
    _category_name: Optional[str]

    @property
    def category_id(self) -> Optional[uuid.UUID]: ...

    @category_id.setter
    def category_id(self, value: uuid.UUID) -> None: ...

    @property
    def category_name(self) -> Optional[str]: ...

    @category_name.setter
    def category_name(self, value: str) -> None: ...
