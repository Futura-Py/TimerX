import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    icon="./assets/logo.ico"
elif sys.platform == "darwin":
    icon="./assets/logo.icns"
else:
    icon= "./assets/logo.png"

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
#         ("IconId", "assets/icon.ico"),
#     ],
# }
import uuid
uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, 'TimerX.TimerX.org')).upper()
# print(str(uuid.uuid3(uuid.NAMESPACE_DNS, 'TimerX.TimerX.org')).upper())

executables = [Executable("main.py", base=base, icon=icon, shortcutName="TimerX", shortcutDir="TimerX")]

# build_exe_options = {"includes": ["tkinter, platform, threading"], "include_msvcr": True}
build_exe_options = {"include_msvcr": True}

bdist_msi_options = {
    "add_to_path":False,
    "install_icon":"assets/logo.ico",
    "upgrade_code":f'{uid}',
    "target_name":"TimerX"
}
bdist_mac_options = {
    "bundle_name": "TimerX",
}

bdist_dmg_options = {
    "volume_label": "TimerX",
}

setup(
    name="TimerX",
    version="1.0.0.0",
    description="A cross-platform simple and modern timer app",
    executables=executables,
    options={
        "build_exe": build_exe_options,
        "bdist_mac": bdist_mac_options,
        "bdist_dmg": bdist_dmg_options,
        "bdist_msi": bdist_msi_options,
    },
)
