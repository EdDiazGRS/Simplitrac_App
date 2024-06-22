# SimpliTrac JTC Capstone

## Setup

---

1. Navigate to the folder where you want to close the repository. Make sure you are standing in the root folder and run the following command:

`git clone git@github.com:dave-b-b/SimpliTrac.git`

2. Make sure that you have Python installed on your machine. If you do not, then install Python3.12.

3. Install the [Firebase CLI](https://firebase.google.com/docs/cli#setup_update_cli). If you haven't signed up for a Firebase account, you should set that up too.

4. Install the dependencies for the client and the server:

`chmod 755 ./bin/install_dependencies.sh`

`./bin/install_dependencies.sh`

   This will install the following dependencies for the server:

   - Firebase Admin (Connects to Firestore)
   - Firestore (Database and "backend server")
   - Emulators (For testing Firestore locally)

   This will install the following dependencies for the client:

   - insert dependencies here

5. Once you have this set up, you'll need to get a key from Firebase. To do this, follow these steps:

    - Go to the Firebase console.
    - Click the gear near the top left of the screen and select "Project Settings".
    - 

6. Make sure that you put all secrets in your .env file. This file should be in the root of the server folder. The .env file should look like this:

```
SUPER_SECRET_KEY=your_secret_key_here
```

## Running the Server for local testing 
1. Run the server for local testing:
`firebase emulators:start`

## Deploying Code
1. To deploy the code, run the following command:

`firebase deploy`

This will deploy everything at once. In my experience, you could really run into some problems by doing this, so its best to deploy each function individually by running this:

`firebase deploy --only functions:<function_name>`

This will deploy the function with the name <function_name> to the cloud.

This avoids the issue where deploying everything my cause everything to break at once instead of just one function.