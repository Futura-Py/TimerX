
import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    icon="./assets/icon.ico"
If sys.platform == "darwin":
    Icon="./assets/icon.icns"

executables = [Executable("main.py", base=base, icon=icon, shortcutName="TimerX")]

bdist_msi = {
    add_to_path=False
    install_icon="./assets/icon.ico"
    upgrade_code="ADDLATER"
    target_name="TimerX"
}

setup(
    name="TimerX",
    version="1.0-alpha",
    description="A cross-platform siple and modern timer app",
    executables=executables,
    bdist_msi=bdist_msi
)
