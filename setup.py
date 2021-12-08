import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    icon="./assets/icon.ico"
elif sys.platform == "darwin":
    icon="./assets/icon.icns"
else;
    icon= "./assets/icon.png"

directory_table = [
    ("ProgramMenuFolder", "TARGETDIR", "."),
    ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|My Program"),
]

msi_data = {
    "Directory": directory_table,
    "ProgId": [
        ("TimerX", None, None, "A simple, lightweight, & beautiful timer app built in Python and tkinter.ttk using rdbende's Sun Valley TTk Theme", "IconId", None),
    ],
    "Icon": [
        ("IconId", "assets/icon.ico"),
    ],
}

executables = [Executable("main.py", base=base, icon=icon, shortcutName="TimerX", shortcutDir="TimerX")]

build_exe_options = {"includes": ["tkinter, platform, threading"], "include_msvcr": True}

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
