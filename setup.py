import sys

from cx_Freeze import Executable, setup

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    icon = "./assets/logo_new.ico"
    executables = [
        Executable(
            "main.py",
            base=base,
            icon=icon,
            shortcut_name="TimerX",
            target_name="TimerX.exe",
            shortcutDir="ProgramMenuFolder",
        )
    ]
elif sys.platform == "darwin":
    icon = "./assets/logo_new.icns"
    executables = [
        Executable(
            "main.py",
            base=base,
            icon=icon,
            shortcut_name="TimerX",
            target_name="TimerX.exe",
        )
    ]
else:
    icon = "./assets/logo_new.png"
    executables = [
        Executable(
            "main.py",
            base=base,
            icon=icon,
            shortcut_name="TimerX",
            target_name="TimerX.exe",
        )
    ]

# directory_table = [
#     ("ProgramMenuFolder", "TARGETDIR", "."),
#     ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|My Program"),
# ]

# msi_data = {
#     "Directory": directory_table,
#     "ProgId": [
#         ("TimerX", None, None, "A simple, lightweight, & beautiful timer app built in Python and tkinter.ttk using rdbende's Sun Valley TTk Theme", "IconId", None),
#     ],
#     "Icon": [
#         ("IconId", "assets/logo.ico"),
#     ],
# }
import uuid

upgradeid = str(uuid.uuid3(uuid.NAMESPACE_DNS, "TimerX.TimerX.org")).upper()

# build_exe_options = {"includes": ["tkinter, platform, threading"], "include_msvcr": True}
build_exe_options = {
    "include_msvcr": True,
    "include_files": (r"./sun-valley.tcl", r"./utils.py", r"./theme", r"./assets"),
    "includes": ["tkinter, platform, threading, win10Toast-click, BlurWindow, darkdetect"],
}

bdist_rpm_options = {"icon": icon}

bdist_msi_options = {
    "add_to_path": False,
    "install_icon": "assets/logo_new.ico",
    "upgrade_code": "{1aaa0457-7406-4383-8307-2ef43e2112cf}",
    "target_name": "TimerX",
}
bdist_mac_options = {"bundle_name": "TimerX", "iconfile": "./assets/logo_new.icns"}

bdist_dmg_options = {
    "volume_label": "TimerX",
    "applications_shortcut": True,
}

version = "0.9"

setup(
    name="TimerX",
    version=version,
    description="A cross-platform simple and modern timer app",
    executables=executables,
    options={
        "build_exe": build_exe_options,
        "bdist_mac": bdist_mac_options,
        "bdist_dmg": bdist_dmg_options,
        "bdist_msi": bdist_msi_options,
        "bdist_rpm": bdist_rpm_options,
    },
)
