from backend.functions.data.messages_data import add_document
from backend.functions.models.Response import Response


async def add_text(collection_name: str, text: object) -> Response:
    result: Response = await add_document(collection_name=collection_name, document=text)
    return result


