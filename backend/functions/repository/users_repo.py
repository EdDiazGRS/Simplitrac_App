from backend.functions.models.user import User
from backend.functions.models.response import Response


def create_user(user: User) -> Response:
    """
    This creates a brand new user in the database
    """

    result: Response = Response()
    result = user.save_to_firestore()

    return result
