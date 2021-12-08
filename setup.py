
import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    icon=“assets/icon.ico”
If sys.platform == “darwin”:
    Icon=“assets/icon.icns”

executables = [Executable("main.py", base=base, icon=icon)]

setup(
    name="TimerX",
    version="0.1",
    description="Timer application based on Python + rdbende's Sun Valley theme",
    executables=executables,
)
