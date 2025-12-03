import os
import pathlib
import subprocess

BASE_DIR = pathlib.Path(__file__).parent
UI_FILE = BASE_DIR / "app" / "dashboard" / "ui.py"

subprocess.run(["streamlit", "run", str(UI_FILE)])