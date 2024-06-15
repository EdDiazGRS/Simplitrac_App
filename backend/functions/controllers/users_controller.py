from firebase_functions import https_fn

from backend.functions.models.user import User
from backend.functions.services.users_service import add_new_user
from backend.functions.models.response import Response


@https_fn.on_request()
async def create_new_user(req: https_fn.Request) -> https_fn.Response:
    """
    Save new user to database
    """

    user = User()

    response: Response = await add_new_user(user)

    if response.is_successful():
        return https_fn.Response(f"Message with ID {response.get_payload.id} added.")
    else:
        return https_fn.Response(f'There was an error: {response.get_errors()}')