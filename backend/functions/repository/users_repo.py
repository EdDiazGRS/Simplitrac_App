from backend.functions.models.User import User
from backend.functions.models.response import Response


async def add_new_user(user: User) -> Response:
    """
    This creates a brand new user in the database
    """

    result: Response = Response()
    result = user.save_to_firestore()

    return result
