from models.user import User
from models.response import Response
import string
import random


def create_user(user: User) -> Response:
    """
    This creates a brand new user in the database
    """

    result: Response = Response()
    if not user.user_id:
        user.user_id = "".join(random.choices(string.ascii_letters+string.digits, k=16))
    result = user.save_to_firestore()

    return result


def update_user(user_id: str, user: User) -> Response:
    """
    This creates a brand new user in the database
    """

    result = user.update_user_in_firestore()

    return result


def find_user(user_id: str) -> Response:
    find_result: Response = User.find(user_id)

    if not find_result.is_successful():
        find_result.set_errors(f"[User Service] User with this id: {user_id} not found")
        return find_result
    else:
        return find_result

def delete_user(user_id: str) -> Response:
    user = find_user(user_id)
    user_instance: User = user.get_payload()
    return user_instance.remove()

