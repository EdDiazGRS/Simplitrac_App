from firebase_functions import https_fn
from models import user

from services import users_service
from models.response import Response
from urllib.parse import parse_qs
from typing import Union
import json
from functools import wraps


def cors_enabled_function(func):
    """Decorator for enabling Cross-Origin Resource Sharing (CORS) on Firebase HTTP functions.

    This decorator adds the necessary CORS headers to allow cross-origin requests 
    to your Firebase function endpoints. It handles both the preflight OPTIONS 
    request and modifies the response headers of the decorated function to ensure 
    proper CORS support.

    Args:
        func: The Firebase HTTP function to be wrapped.
    """
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


# Firebase HTTP Function Handlers 
@cors_enabled_function
@https_fn.on_request()
def create_new_user(req: https_fn.Request) -> https_fn.Response:
    """Creates a new user in the Firestore database.

    Args:
        req (https_fn.Request): The HTTP request object containing the new user data in JSON format.

    Returns:
        https_fn.Response: An HTTP response indicating success or failure, containing the ID of the new user
                           or an error message.
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
        return https_fn.Response(response.get_payload())
    else:
        return https_fn.Response(f'There was an error: {response.get_errors()}')


@cors_enabled_function
@https_fn.on_request()
def get_existing_user(req: https_fn.Request) -> https_fn.Response:
    """Retrieves an existing user from the database.

    Args:
        req (https_fn.Request): The HTTP request object containing the `user_id` in the query string.

    Returns:
        https_fn.Response: An HTTP response containing the serialized user data or an error message
                           if the user is not found.
    """
    response = Response()
    user_id = parse_qs(req.query_string.decode()).get('user_id', [None])[0]

    if not user_id:
        return generate_http_response('user_id parameter is required', 400)
    
    user_instance = user.User(user_id)

    if not user_instance.user_id:
        return generate_http_response(f"User {user_id} not found", 400)

    response.set_payload(user_instance.serialize(True))
    return https_fn.Response(f"User {(response.get_payload())} found.", 200)
        


@cors_enabled_function
@https_fn.on_request()
def update_user(req: https_fn.Request) -> https_fn.Response:
    """Updates an existing user in the database.

    Args:
        req (https_fn.Request): The HTTP request object containing:
            - `user_id` in the query string.
            - Updated user data in the request body (JSON format).

    Returns:
        https_fn.Response: An HTTP response indicating success or failure of the update operation.

    Raises:
        ValueError: If the `user_id` format is invalid or if the request body is not valid JSON.
    """
    data = None
    access_token = None
    user_id = None
    user_instance = user.User()

    try:
        data = req.get_json()
        if not data:  # Check for empty JSON
            return generate_http_response('Request body must contain valid JSON data', 400)
    except json.JSONDecodeError as e:  # Catch specific JSON decoding errors
        return generate_http_response(f'Invalid JSON: {e}', 400)

    try:
        user_id = parse_qs(req.query_string.decode()).get('user_id', [None])[0]
        if not user_id:  # Explicitly check for missing user_id
            return generate_http_response('user_id parameter is required', 400)

    except ValueError as e:
        return generate_http_response(f'Invalid user_id: {e}', 400)

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
    """Generates an HTTP response with a JSON-formatted error message.

    Args:
        message (Union[str, list]): The error message (either a string or a list of strings).
        code (int): The HTTP status code (e.g., 400 for Bad Request, 500 for Internal Server Error).

    Returns:
        https_fn.Response: The formatted HTTP response object.
    """
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


