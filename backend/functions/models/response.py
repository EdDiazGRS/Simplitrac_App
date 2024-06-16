from typing import Optional, Any, List
from backend.functions.protocols.response_protocol import ResponseProtocol


class Response(ResponseProtocol):
    """
    Represents a response object that includes a payload and a list of errors.

    Attributes:
        payload (Optional[Any]): The main content of the response.
        errors (List[str]): A list of error messages associated with the response.
    """
    payload: Optional[Any] = None
    errors: List[str] = []

    def __init__(self, payload: Optional[Any] = None, errors: Optional[List[str]] = None):
        """
        Initializes a new Response instance.

        Args:
            payload (Optional[Any]): The main content of the response.
            errors (Optional[List[str]]): A list of error messages. Defaults to an empty list if not provided.
        """
        self.payload = payload
        self.errors = errors if errors is not None else []

    def add_error(self, error_message: str) -> None:
        """
        Adds an error message to the list of errors.

        Args:
            error_message (str): A string describing the error.
        """
        self.errors.append(error_message)

    def is_successful(self) -> bool:
        """
        Determines if the response is successful (i.e., has no errors).

        Returns:
            bool: True if there are no errors, False otherwise.
        """
        return len(self.errors) == 0

    def get_payload(self) -> Optional[Any]:
        """
        Gets the payload of the response.

        Returns:
            Optional[Any]: The payload content.
        """
        return self.payload

    def set_payload(self, payload: Any) -> None:
        """
        Sets the payload of the response.

        Args:
            payload (Any): The new payload content.
        """
        self.payload = payload

    def get_errors(self) -> List[str]:
        """
        Gets the list of errors.

        Returns:
            List[str]: The list of error messages.
        """
        return self.errors

    def set_errors(self, error: str) -> None:
        """
        Adds an error to the list of errors.

        Args:
            error (str): A string describing the error.
        """
        self.errors.append(error)

    def __repr__(self) -> str:
        """
        Returns a string representation of the Response object.

        Returns:
            str: String representation of the payload and errors.
        """
        return f"Response(payload={self.payload}, errors={self.errors})"
