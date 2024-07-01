import os
os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
import sys
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()


emulators_running = os.getenv('FIRESTORE_EMULATOR_HOST') 

if emulators_running:
    #Local environment settings
    sys.path.insert(0, Path(__file__).parent.parent.as_posix())
    from controllers.users_controller import update_user, create_new_user, get_existing_user, delete_user
    from controllers.ocr_controller import process_receipt
else:
    # Production settings
    sys.path.insert(0, Path(__file__).parent.as_posix())
    from controllers.users_controller import update_user, create_new_user, get_existing_user, delete_user
    from controllers.ocr_controller import process_receipt

