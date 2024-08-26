from firebase_functions import https_fn
from models import user
from models.transaction import Transaction
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
    print("Inside create_new_user function")
    print(f"Request method: {req.method}")
    print(f"Request headers: {dict(req.headers)}")
    print(f"Request data type: {type(req.data)}")

    if isinstance(req.data, bytes):
        print(f"Request data (decoded): {req.data.decode('utf-8')}")
    else:
        print(f"Request data: {req.data}")

    data = None
    user_instance = None
    access_token = None
    response = Response()

    # Try to get JSON data from the request
    try:
        if req.method == "POST":
            if req.headers and req.headers.get('Content-Type', '').startswith('application/json'):
                if req.data:
                    if isinstance(req.data, bytes):
                        data = json.loads(req.data.decode('utf-8'))
                    elif isinstance(req.data, str):
                        data = json.loads(req.data)
                    else:
                        print(f"Unexpected data type: {type(req.data)}")
                else:
                    print("Request body is empty")
            else:
                print(f"Unexpected Content-Type: {req.headers.get('Content-Type')}")
        else:
            print(f"Unexpected HTTP method: {req.method}")
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON from request body: {str(e)}")
    except Exception as e:
        print(f"An error occurred while parsing request data: {str(e)}")

    if data:
        print(f"Received data: {data}")
        user_instance = user.User(data)
        access_token = user_instance.access_token
    else:
        print("No data received, creating default User instance")
        user_instance = user.User()

    response: Response = users_service.add_new_user(user_instance)

    if response.is_successful():
        return https_fn.Response(f"{response.get_payload()}", 200)
    else:
        return https_fn.Response(f'There was an error: {response.get_errors()}', 400)

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
    user_id = parse_qs(req.query_string.decode()).get('user_id', [None])[0]

    if not user_id:
        return generate_http_response('user_id parameter is required', 400)
    
    try:
        user_instance = user.User(user_id)

    except Exception as e:  # Catch general exceptions for get_existing_user and User creation
        return generate_http_response(str(e), 500)  # 500 Internal Server Error if unexpected

    if user_instance.user_id != user_id:
        return generate_http_response(f"User {user_id} not found", 400)

    # return https_fn.Response(f"{user_instance.create_json_string(True)}", 200)
    return https_fn.Response(json.dumps(user_instance.serialize(True)), 200)
        


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
    except Exception as e:  # Catch specific JSON decoding errors
        return generate_http_response(f'Invalid JSON: {e}', 400)
    try:
        user_id = parse_qs(req.query_string.decode()).get('user_id', [None])[0]
        if not user_id:  # Explicitly check for missing user_id
            return generate_http_response('user_id parameter is required', 400)

    except ValueError as e:
        return generate_http_response(f'Invalid user_id: {e}', 400)

    try:
        user_dict = user.User(user_id).serialize(True)
        user_dict.update(data)  # Update the dictionary
        user_instance = user.User(user_dict)

    except Exception as e:  # Catch general exceptions for get_existing_user and User creation
        return generate_http_response(str(e), 500)  # 500 Internal Server Error if unexpected

    if not user_instance.user_id:  # Check if user found in database
        return generate_http_response(f"User {user_id} not found.", 400)

    if user_id != user_instance.user_id:  # Ensure consistency between query and body
        return generate_http_response("user_id in query and body do not match", 400)

    if user_instance:
        access_token = user_instance.access_token

    update_result = users_service.update_user(user_instance)

    if update_result.is_successful():
        return https_fn.Response(json.dumps(update_result.get_payload()), 200)
    else:
        return generate_http_response(update_result.get_errors(), 400)


@cors_enabled_function
@https_fn.on_request()
def delete_transactions(req: https_fn.Request) -> https_fn.Response:
    """
    Deletes transactions from the database.

    Args:
        req (https_fn.Request): The HTTP request object containing the `user_id` in the query string.

    Returns:
        https_fn.Response: An HTTP response indicating success or failure of the deletion.
    """
    data = None
    access_token = None
    user_instance = user.User()
    try:
        data = req.get_json()
        if not data:  # Check for empty JSON
            return generate_http_response('Request body must contain valid JSON data', 400)
    except Exception as e:  # Catch specific JSON decoding errors
        return generate_http_response(f'Invalid JSON: {e}', 400)

    try:
        user_instance = user.User(data)

    except Exception as e:  # Catch general exceptions for get_existing_user and User creation
        return generate_http_response(str(e), 500)  # 500 Internal Server Error if unexpected

    if not user_instance.user_id:  # Check if user found in database
        return generate_http_response(f"User {user_id} not found.", 400)

    if user_instance:
        access_token = user_instance.access_token

    edit_result = users_service.delete_transactions(user_instance)

    if edit_result.is_successful():
        return https_fn.Response(json.dumps(edit_result.get_payload()), 200)
    else:
        return generate_http_response(edit_result.get_errors(), 400)


@cors_enabled_function
@https_fn.on_request()
def delete_category(req: https_fn.Request) -> https_fn.Response:
    """
    Deletes transactions from the database.

    Args:
        req (https_fn.Request): The HTTP request object containing the `user_id` and `category_id` in the query string.

    Returns:
        https_fn.Response: An HTTP response indicating success or failure of the deletion.
    """
    data = None
    try:
        data = req.get_json()
        if not data:  # Check for empty JSON
            return generate_http_response('Request body must contain valid JSON data', 400)
    except Exception as e:  # Catch specific JSON decoding errors
        return generate_http_response(f'Invalid JSON: {e}', 400)

    delete_result = users_service.delete_category(dict(data))

    if delete_result.is_successful():
        return https_fn.Response(json.dumps(delete_result.get_payload().serialize(True)), 200)
    else:
        return generate_http_response(delete_result.get_errors(), 400)



@cors_enabled_function
@https_fn.on_request()
def delete_user(req: https_fn.Request) -> https_fn.Response:
    """Deletes a user from the database.

    Args:
        req (https_fn.Request): The HTTP request object containing the `user_id` in the query string.

    Returns:
        https_fn.Response: An HTTP response indicating success or failure of the deletion.
    """
    try:
        user_id = parse_qs(req.query_string.decode()).get('user_id', [None])[0]
        if not user_id:  # Explicitly check for missing user_id
            return generate_http_response('user_id parameter is required', 400)

    except ValueError as e:
        return generate_http_response(f'Invalid user_id: {e}', 400)

    get_result = users_service.delete_user(user_id)
    
    if get_result.is_successful():
        return https_fn.Response(f"User with ID {user_id} deleted.")
    else:
        return generate_http_response(get_result.get_errors(), 400)


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
        result_message = ", ".join(message)
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