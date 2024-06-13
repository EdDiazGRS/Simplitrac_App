from firebase_functions import https_fn

from backend.functions.services.messages_service import add_text
from backend.functions.models import Response


@https_fn.on_request()
async def addmessage(req: https_fn.Request) -> https_fn.Response:
    """
    Take the text parameter passed to this HTTP endpoint and insert it into
    a new document in the messages collection.
    """
    # Grab the text parameter.
    original = req.args.get("text")
    if original is None:
        return https_fn.Response("No text parameter provided", status=400)

    response: Response = await add_text(collection_name="messages", text={"original": original})

    if response.is_successful():
        return https_fn.Response(f"Message with ID {response.get_payload.id} added.")
    else:
        return https_fn.Response(f'There was an error: {response.get_errors}')