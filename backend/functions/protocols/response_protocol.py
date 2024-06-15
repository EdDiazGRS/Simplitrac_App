from typing import Protocol, Optional, List, Any

class ResponseProtocol(Protocol):
    payload: Optional[Any]
    errors: List[str]

    def add_error(self, error_message: str) -> None: ...
    
    def is_successful(self) -> bool: ...
    
    def get_payload(self) -> Optional[Any]: ...
    
    def set_payload(self, payload: Any) -> None: ...
    
    def get_errors(self) -> List[str]: ...
    
    def set_errors(self, error: str) -> None: ...
    
    def __repr__(self) -> str: ...
