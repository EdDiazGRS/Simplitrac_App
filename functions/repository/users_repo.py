from models.user import User
from models.response import Response
import string
import random


def create_user(user: User) -> Response:
    """Creates a new user in the Firestore database.

    This function takes a `User` object as input. If the provided `User` object 
    doesn't have a `user_id`, a random alphanumeric string of 16 characters will be generated and assigned.

    The user object is then saved to Firestore using the `save_to_firestore` method 
    (presumably implemented within the `User` class). The result of this operation
    is returned as a `Response` object.

    Args:
        user (User): A User object representing the new user to be created.

    Returns:
        Response: A `Response` object indicating the outcome of the operation.
            - If successful, `result.is_successful()` is True and `result.get_payload()` may contain the saved user data or a confirmation message.
            - If unsuccessful, `result.is_successful()` is False and `result.get_errors()` contains error details.

    Raises:
        google.cloud.exceptions.FirebaseError: If there's an error communicating with Firestore during the save operation.
    """
    if not user.user_id:
        user.user_id = "".join(random.choices(string.ascii_letters + string.digits, k=16))
    result = user.save_to_firestore()  
    return result


# def find_user(user_id: str) -> Response:
#     """Finds an existing user in the Firestore database.

#     Args:
#         user_id (str): The unique identifier (e.g., UUID) of the user to find.

#     Returns:
#         Response: A `Response` object:
#             - If successful, `result.is_successful()` is True and `result.get_payload()` contains the serialized User object.
#             - If unsuccessful (user not found), `result.is_successful()` is False and `result.get_errors()` contains a 'user not found' message.
#     """
#     find_result: Response = User.find(user_id)  
#     if not find_result.is_successful():
#         find_result.set_errors(f"[User Service] User with this id: {user_id} not found") 
#     return find_result


def update_user(user: User) -> Response:
    """Updates an existing user in the Firestore database.

    Args:
        user_id (str): The unique identifier of the user to update.
        user (User): The updated User object with new information.

    Returns:
        Response: A `Response` object:
            - If successful, `result.is_successful()` is True, and `result.get_payload()` contains a success message.
            - If unsuccessful, `result.is_successful()` is False, and `result.get_errors()` contains error details.

    Note:
        This function assumes that the User object (`user`) already has the updated data.
    """
    result = user.update_user_in_firestore()
    return result


def delete_user(user_id: str) -> Response:
    """Deletes an existing user from the Firestore database.

    Args:
        user_id (str): The unique identifier of the user to delete.

    Returns:
        Response: A `Response` object:
            - If successful, `result.is_successful()` is True, and `result.get_payload()` contains a success message.
            - If unsuccessful (user not found), `result.is_successful()` is False, and `result.get_errors()` contains a 'user not found' message.
            - In case of other errors during the delete process, the `errors` attribute will contain an appropriate message.
    """
    return User.remove(user_id) 
