class Response:
    def __init__(self, payload=None, errors=None):
        """
        Initialize the Response object with payload and errors.
        
        :param payload: The main content of the response (default is None).
        :param errors: Any errors associated with the response (default is None).
        """
        self.payload = payload
        self.errors = errors if errors is not None else []

    def add_error(self, error_message):
        """
        Add an error message to the errors list.
        
        :param error_message: A string describing the error.
        """
        self.errors.append(error_message)

    def is_successful(self):
        """
        Determine if the response is successful (i.e., has no errors).
        
        :return: True if there are no errors, False otherwise.
        """
        return len(self.errors) == 0

    def get_payload(self):
        """
        Get the payload of the response.
        
        :return: The payload content.
        """
        return self.payload

    def set_payload(self, payload):
        self.payload = payload

    def get_errors(self):
        """
        Get the list of errors.
        
        :return: The list of error messages.
        """
        return self.errors

    def set_errors(self, error):
        self.errors.append(error)

    def __repr__(self):
        """
        Return a string representation of the Response object.
        
        :return: String representation of the payload and errors.
        """
        return f"Response(payload={self.payload}, errors={self.errors})"
