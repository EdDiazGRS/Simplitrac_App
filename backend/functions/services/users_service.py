from backend.functions.models.user import User
from backend.functions.repository.users_repo import add_new_user
from backend.functions.models.response import Response


async def add_new_user(user: User) -> Response:
    result: Response = await add_new_user(user)
    return result
