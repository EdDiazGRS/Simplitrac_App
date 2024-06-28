import os
from dotenv import load_dotenv
import sys
from pathlib import Path

emulators_running = os.getenv('FIRESTORE_EMULATOR_HOST')

if emulators_running:
    #Local environment settings
    sys.path.insert(0, Path(__file__).parent.parent.as_posix())
    from controllers.users_controller import update_user, create_new_user, get_existing_user
else:
    # Production settings
    sys.path.insert(0, Path(__file__).parent.as_posix())
    from controllers.users_controller import update_user, create_new_user, get_existing_user



__all__ = ['create_new_user', 'update_user', 'get_existing_user']