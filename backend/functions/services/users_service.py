from backend.functions.models.user import User
from backend.functions.repository.users_repo import create_user
from backend.functions.models.response import Response


def add_new_user(user: User) -> Response:
    result: Response = create_user(user)
    return result
