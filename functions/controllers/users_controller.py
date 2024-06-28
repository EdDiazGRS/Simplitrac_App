import uuid

from firebase_functions import https_fn

from models import user
from services import users_service
from models.response import Response
from urllib.parse import parse_qs
from typing import Union
import json
from functools import wraps


def cors_enabled_function(func):
    @wraps(func)
    def wrapper(req, *args, **kwargs):
        if req.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'PUT, POST, GET, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            }
            print("Inside cors function")
            return https_fn.Response('', 204, headers)

        # Call the original function
        response = func(req, *args, **kwargs)

        # Ensure the response has the CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        print("Returning response in cors")
        print(response)
        return response
    print("returning wrapper")
    return wrapper


@cors_enabled_function
@https_fn.on_request()
def create_new_user(req: https_fn.Request) -> https_fn.Response:
    """
    Save a new user in the database

    :param req: The request must have the user object in the body
    :return: https_fn.Response
    """
    data = None
    user_instance = None
    access_token = None
    response = Response()


    try:
        data = req.get_json()
    except:
        pass

    if data:
        print(data)
        user_instance = user.User(data)
        access_token = user_instance.access_token
    else:
        user_instance = user.User()

    if not access_token:
        return generate_http_response("A token is needed to access this resource", 400)

    try:
        if not user_instance.is_authenticated():
            response.add_error("User could not be authenticated")
            return generate_http_response(response.get_errors(), 400)

    except Exception as e:
        response.add_error("There was an issue authenticating the user")
        return generate_http_response(response.get_errors(), 400)

    response: Response = users_service.add_new_user(user_instance)

    if response.is_successful():
        return https_fn.Response(f"Message with ID {response.get_payload()} added.")
    else:
        return https_fn.Response(f'There was an error: {response.get_errors()}')


@cors_enabled_function
@https_fn.on_request()
def update_user(req: https_fn.Request) -> https_fn.Response:
    """
    Update a user in the database

    :param req: The request must have a user_id param in the query string and the updated user object in the body
    :return: https_fn.Response
    """
    user_instance = None
    user_id: str = ""

    query_string = req.query_string.decode()
    params = parse_qs(query_string)
    user_id_string = params.get('user_id', [None])[0]
    user_id = user_id_string

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

    print(user_id)
    print(user_instance.user_id)
    if user_id != user_instance.user_id:
        return generate_http_response("Param user_id and the user_id in the body do not match", 400)

    # return https_fn.Response(f"{user_id} for this user: {user.serialize()}")
    update_result = users_service.update_user(user_id, user)
    if not update_result.is_successful():
        return generate_http_response(update_result.get_errors(), 400)
    else:
        return https_fn.Response(update_result.get_payload(), 200)


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
            response=json.dumps({'error': message}),
            status=code
        )
#
#
# def handle_cors(req: https_fn.Request) -> Union[https_fn.Response, None]:
#     if req.method == 'OPTIONS':
#         headers = {
#             'Access-Control-Allow-Origin': '*',
#             'Access-Control-Allow-Methods': 'PUT, POST, GET, DELETE, OPTIONS',
#             'Access-Control-Allow-Headers': 'Content-Type, Authorization'
#         }
#         return https_fn.Response('', 204, headers)
#     return None
