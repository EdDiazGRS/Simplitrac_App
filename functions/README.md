# Firebase Emulator Guide for Debugging

## Introduction

Using Firebase Emulators allows you to simulate Firebase services locally, making it easier to develop and debug your application without affecting the live environment. This guide will walk you through setting up and using the Firebase Emulators to test and debug your endpoints effectively.

## Steps to Run Firebase Emulators

### 1. Start the Emulators

Open your terminal and navigate to your project directory. Start the Firebase Emulators by running the following command:

```bash
firebase emulators:start
```

This command will start the emulators for the services specified in your `firebase.json` configuration file.

### 2. Prepare Your Development Environment

To effectively debug your code, make sure you have the following tools open:

- **Web Browser**: Access the Firebase Emulator UI at `http://localhost:4000/logs` to monitor logs and view the database state.
- Access the database at `http://localhost:4000/firestore/default/data`
- **Visual Studio Code (VSCode)**: Use VSCode to write and debug your code.
- **Postman**: Use Postman to test your API endpoints and inspect the responses.

### 3. Create an Endpoint for Testing

Add the following code to define an HTTP function in your Firebase project. This function will serve as the endpoint for creating a new user:

```python
from firebase_functions import https_fn

@https_fn.on_request()
def test_controller(req: https_fn.Request) -> https_fn.Response:
    data = None

    try:
        data = req.get_json()
    except:
        pass
    print("Connected to endpoint")
    print("Here's the info you sent:", data)
    return https_fn.Response(f"Here's the data {data}")
`````

### 4. Check the Logs

After starting the emulators and making a request to your endpoint, check the logs in your terminal or in the Firebase Emulator UI at `http://localhost:4000/logs`. Look for messages like "Connected to endpoint" to confirm that your request has reached the server.

### 5. Inspect the Response in Postman

Use Postman to send a request to your endpoint (e.g., `http://localhost:5001/simplitracapp/us-central1/test_controller)). Verify that you receive the expected response and that the data you sent is correctly processed.

### 6. Connect the Controller to the Service Layer

Update your controller function to interact with the service layer, which handles business logic. The service layer will process the request and pass data to the repository layer for database operations. Here’s an example service layer function:

```python
# backend/functions/controllers/test_controller.py
 # ADD THE SERVICE PACKAGE AT THE TOP

 from backend.functions.services.test_service.py import test_service

@https_fn.on_request()
def test_controller(req: https_fn.Request) -> https_fn.Response:
    data = None

    try:
        data = req.get_json()
    except:
        pass
    # print("Connected to endpoint")
    # print("Here's the info you sent:", data)
    result = test_service(data)
    return https_fn.Response(f"Here's teh result from the service layer {result}")

```

```python
# backend/functions/services/test_service.py

def test_service(data):

    return f"This is the data you sent{data}. It reached the service layer"
````

Test the integration to ensure the service layer correctly interacts with the controller.

### 7. Connect the Service Layer to the Repository Layer

Finally, integrate your service layer with the repository layer, which handles database interactions. Here's an example repository layer function:

```python
# backend/functions/services/test_service.py
# UPDATE YOUR SERVICE LAYER TO GO TO YOUR DATA LAYER
from backend.functions.repository.test_repo.py import test_repo

def test_service(data):
    result = test_repo(data)
    return result
```

```python
# backend/functions/services/test_repo.py

from backend.functions.models.user import User
def test_repo(data):
    user1 = User()
    result = user1.update_user_in_firestore()
    return f"This is the data you sent{data}. It reached the data layer. Here's a response from the database: {result}"
```

Test the complete flow to ensure that the entire stack—from the controller to the repository—works as expected.

## Summary

Using Firebase Emulators allows you to test and debug your Firebase functions locally. By following these steps, you can set up your development environment, create and test endpoints, and integrate your service and repository layers effectively.

Keep this guide handy for your development workflow, and don't hesitate to reach out if you need further assistance!

---

### Additional Resources

- [Firebase Emulator Suite Documentation](https://firebase.google.com/docs/emulator-suite)
- [Postman Download and Documentation](https://www.postman.com/downloads/)

---