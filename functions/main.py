import os
import sys
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# Adding this to the Operating system environment variables to fix  an issue with the OCR functions
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'

# While using .. before the modules does not display errors locally, when you try to run the emulator
# or the deploy the code to firebase, it will give you the following error:
# ImportError: attempted relative import beyond top-level package
# So you have to open the functions folder as the project and run everything from there

# Load environment variables
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(env_path)

emulators_running = os.getenv('FIRESTORE_EMULATOR_HOST')

if emulators_running:
    #Local environment settings
    sys.path.insert(0, Path(__file__).parent.parent.as_posix())
    from controllers.users_controller import update_user, create_new_user, get_existing_user, delete_user, edit_transactions
    from controllers.ocr_controller import process_receipt
else:
    # Production settings
    sys.path.insert(0, Path(__file__).parent.as_posix())
    from controllers.users_controller import update_user, create_new_user, get_existing_user, delete_user, edit_transactions
    from controllers.ocr_controller import process_receipt



__all__ = ['create_new_user', 'update_user', 'get_existing_user', 'delete_user', 'edit_transactions', process_receipt]