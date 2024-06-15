import sys
from pathlib import Path

sys.path.insert(0, Path(__file__).parent.parent.parent.as_posix())
from backend.functions.controllers.users_controller import create_new_user

