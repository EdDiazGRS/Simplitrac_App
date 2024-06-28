import uuid

from firebase_functions import https_fn
from models import user
from services import users_service
from models.response import Response
from urllib.parse import parse_qs
from typing import Union
import json
from flask import jsonify


@https_fn.on_request()
def create_new_user(req: https_fn.Request) -> https_fn.Response:
    """
    Save a new user in the database

    :param req: The request must have the user object in the body
    :return: https_fn.Response
    """
    data = None
    user_instance = None

    try:
        data = req.get_json()
    except:
        pass

    if data:
        user_instance = user.User(data)
    else:
        user_instance = user.User()

    response: Response = users_service.add_new_user(user_instance)
    
    if response.is_successful():
        return https_fn.Response(f"Message with ID {response.get_payload()} added.")
    else:
        return https_fn.Response(f'There was an error: {response.get_errors()}')


@https_fn.on_request()
def update_user(req: https_fn.Request) -> https_fn.Response:
    """
    Update a user in the database

    :param req: The request must have a user_id param in the query string and the updated user object in the body
    :return: https_fn.Response
    """
    user_instance = None
    user_id: string = ""

    query_string = req.query_string.decode()
    params = parse_qs(query_string)
    user_id = params.get('user_id', [None])[0]
    if not user_id:
        return generate_http_response('user_id parameter is required', 400)

    try:
        request_data = req.get_json(silent=False)
        if request_data is None:
            raise ValueError("Empty JSON body")

        user_instance = user.User(request_data)
    except Exception as e:
        if isinstance(e, ValueError):
            return generate_http_response('body must be provided', 400)
        else:
            return generate_http_response('There was an error parsing the json string', 400)

    if user_id != user_instance.user_id:
        return generate_http_response("Param user_id and the user_id in the body do not match", 400)

    # iterate through params send on https req to find updated information
    for k, v in params.items():
        if getattr(user_instance, k) != v[0]:
            setattr(user_instance, k, v[0])

    # return https_fn.Response(f"{user_id} for this user: {user.serialize()}")
    update_result = users_service.update_user(user_id, user_instance)
    if update_result.is_successful():
        return https_fn.Response(update_result.get_payload(), 200)
    else:
        return generate_http_response(update_result.get_errors(), 400)


@https_fn.on_request()
def get_existing_user(req: https_fn.Request) -> https_fn.Response:
    """
    Retrieves existing user in the database
    :param req: The request must have a user_id param in the query string
    :return: https_fn.Response
    """
    user_instance = None
    user_id: str = ""

    query_string = req.query_string.decode()
    params = parse_qs(query_string)
    user_id = params.get('user_id', [None])[0]
    if not user_id:
        return generate_http_response('user_id parameter is required', 400)

    get_result = users_service.get_existing_user(user_id)
    user_instance = get_result.get_payload()
    user_json = json.dumps(user_instance, cls=user.UserEncoder)

    if get_result.is_successful():
        return https_fn.Response(user_json, 200)
    else:
        return generate_http_response(get_result.get_errors(), 400)
    

def generate_http_response(message: Union[str, list], code: int) -> https_fn.Response:
    if isinstance(message, list):
        result_message: str = ""
        result_message = result_message.join(", ")
        return https_fn.Response(
            response=json.dumps({'error': result_message}),
            status=code
        )
    else:
        return https_fn.Response(
            response=json.dumps({'error':message}),
            status=code
        )

