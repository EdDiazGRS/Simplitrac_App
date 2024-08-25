from models.user import User
from models.response import Response
import string
import random
import uuid

def create_user(user: User) -> Response:
    """Creates a new user in the Firestore database.

    This function takes a `User` object as input. If the provided `User`
    object doesn't have a `user_id`, a random alphanumeric string of 
    16 characters will be generated and assigned.

    The user object is then saved to Firestore using the `save_to_firestore` 
    method implemented within the `User` class. The result of this operation
    is returned as a `Response` object.

    Args:
        user (User): A User object representing the new user to be created.

    Returns:
        Response: A `Response` object indicating the outcome of the operation.

    Raises:
        google.cloud.exceptions.FirebaseError: If there's an error 
        communicating with Firestore during the save operation.
    """
    if not user.user_id:
        user.user_id = str(uuid.uuid4())

    return user.save_to_firestore()


def update_user(user: User) -> Response:
    """Updates an existing user in the Firestore database.

    Args:
        user (User): The updated User object with new information.

    Returns:
        Response: A `Response` object from `update_user_in_firestore()` method.

    Note:
        This function assumes that the User object (`user`) already has the updated data.
    """

    return user.save_to_firestore()


def delete_user(user_id: str) -> Response:
    """Deletes an existing user from the Firestore database.

    Args:
        user_id (str): The unique identifier of the user to delete.

    Returns:
        Response: A `Response` object from `remove()` method.
    """
    return User.remove(user_id) 


def delete_transactions(user: User) -> Response:
    """
    Deletes existing transactions in the Firestore database.

    Args:
        user (User): The updated User object with deleted transaction information.

    Returns:
        Response: A `Response` object from `delete_transactions()` method.
    """
    return user.delete_transactions() 


def delete_category(data: dict) -> Response:
    """
    Deletes existing transactions in the Firestore database.

    Args:
        user (User): The updated User object with deleted transaction information.

    Returns:
        Response: A `Response` object from `delete_transactions()` method.
    """
    user_instance = User(data.get('user_id'))
    return user_instance.delete_category(data) 