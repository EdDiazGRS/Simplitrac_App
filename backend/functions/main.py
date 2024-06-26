import sys
import os
from firebase_functions import https_fn
from pathlib import Path



sys.path.insert(0, Path(__file__).parent.parent.parent.as_posix())
from backend.functions.controllers.users_controller import create_new_user

from backend.functions.controllers.ocr_controller import process_receipt


