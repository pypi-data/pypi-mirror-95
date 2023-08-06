"""Define global paths for easy file find."""
from os import environ
from pathlib import Path
from sys import exit as sysexit

# Define basic paths for global use
try:
    SOURCE_DIR_PATH = Path(__file__).parent.resolve(strict=True)
    PROBEN1_DIR_PATH = (SOURCE_DIR_PATH / "datasets" / "proben1").resolve(
        strict=True
    )
except FileNotFoundError as error:
    sysexit(f"{error.strerror}: {error.filename}")

# Possibly not existent folders
LOGS_DIR_PATH = SOURCE_DIR_PATH / "logs"
LOGS_DIR_PATH.mkdir(exist_ok=True)

# Globals
SEED = int(environ.get("SEED", 31415))
