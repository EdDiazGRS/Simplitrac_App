from models.user import User
from repository.users_repo import create_user
from models.response import Response
from repository import users_repo

def add_new_user(user: User) -> Response:
    """
    Adds a new user to the database.

    Args:
        user (User): The User object containing the new user's information.

    Returns:
        Response: A Response object indicating the success or failure of the operation.
                  - If successful, `result.is_successful()` is True and `result.get_payload()` contains any relevant data.
                  - If unsuccessful, `result.is_successful()` is False and `result.get_errors()` provides an error message.
    """

    return create_user(user)


def update_user(user: User) -> Response:
    """
    Updates an existing user in the database.

    Args:
        user_id (str): The unique identifier (e.g., UUID) of the user to update.
        user (User): The updated User object with new information.

    Returns:
        Response: A Response object:
            - If successful, `result.is_successful()` is True and `result.get_payload()` contains any relevant data (e.g., a success message).
            - If unsuccessful (user not found), `result.is_successful()` is False and `result.get_errors()` contains "This user does not exist".
            - In case of other errors during the update process, the `errors` attribute will contain an appropriate message.
    """

    return users_repo.update_user(user)


def delete_user(user_id: str) -> Response:
    """
    Deletes an existing user from the database.

    Args:
        user_id (str): The unique identifier (e.g., UUID) of the user to delete.

    Returns:
        Response: A Response object:
            - If successful, `result.is_successful()` is True and `result.get_payload()` contains any relevant data (e.g., a success message).
            - If unsuccessful (user not found), `result.is_successful()` is False and `result.get_errors()` contains "This user does not exist".
            - In case of other errors during the delete process, the `errors` attribute will contain an appropriate message.
    """

    return users_repo.delete_user(user_id)