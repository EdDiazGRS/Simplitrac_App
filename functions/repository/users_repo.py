from models.user import User
from models.response import Response


def create_user(user: User) -> Response:
    """
    This creates a brand new user in the database
    """

    result: Response = Response()
    result = user.save_to_firestore()

    return result


def update_user(user_id: str, user: User) -> Response:
    """
    This creates a brand new user in the database
    """

    result = user.update_user_in_firestore()

    return result


def find_user(user_id: str) -> Response:
    result = Response()
    find_result: Response = User.find(user_id)

    if not find_result.is_successful():
        result.set_errors(f"[User Service] User with this id: {user_id} not found")
        return result
    else:
        return find_result
