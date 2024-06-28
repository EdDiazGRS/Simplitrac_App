from models.user import User
from repository.users_repo import create_user
from models.response import Response
from repository import users_repo


def add_new_user(user: User) -> Response:
    result: Response = create_user(user)
    return result


def update_user(user_id: str, user: User) -> Response:
    """
    This creates a brand new user in the database
    """

    search_result = users_repo.find_user(user_id)
    if not search_result.is_successful():
        search_result.set_errors("This user does not exist")
        return search_result

    result = users_repo.update_user(user_id, user)
    if not result.is_successful():
        pass
    else:
        return result

def get_existing_user(user_id: str) -> Response:
    """
    This retrieves an existing user in the database
    """

    search_result = users_repo.find_user(user_id)
    if search_result.is_successful():
        return search_result
    else:
        search_result.set_errors("This user does not exist")
        return search_result