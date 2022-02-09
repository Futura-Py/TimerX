# CONFIG
import json
import tkinter as tk
from tkinter import ttk, PhotoImage, TclError
from functools import partial
from platform import system

def loadConfig(current_version):
    with open("config.json") as config_file:
        config = json.load(config_file)
        try:
            if config['version'] < current_version:
                # Update Settings when Needed
                config['version'] = current_version
                saveConfig(config)
        except KeyError:
            config.update({"version": current_version})
            config.update({"fullscreen":"Windowed"})
            saveConfig(config)
    return config


def saveConfig(config):
    with open("config.json", "w") as config_file:
        json.dump(config, config_file)


def createConfig():
    with open("config.json", "w") as config_file:
        json.dump(
            {
                "theme": "Light",
                "notify": False,
                "ontop": False,
                "transperency": 0.99,
                "sound": True,
                "default_minutes": 0,
                "default_hours": 0,
                "default_seconds": 5,
                "sound_path": r".\assets\sounds\sound1.wav",
                "fullscreen": "Windowed"
            },
            config_file,
        )


# VALIDATION
def validate(input):
    if input.isdigit():
        return True

    elif input == "":
        return True

    else:
        return False


# POPUP
# From Sun-Valley-Messageboxes
def popup(parent, title, details, icon, *, buttons):
    dialog = tk.Toplevel()
    dialog.attributes("-topmost", True)

    try:
        if system() == "darwin":
            dialog.iconbitmap(r"assets/logo_new.icns")
            dialog.wm_attributes("-transparent", True)
            dialog.config(bg="systemTransparent")
        elif system() == "Windows":
            dialog.iconbitmap(r"assets/logo_new.ico")
        elif system() == "win":
            dialog.iconphoto(r"assets/logo_new.ico")
        else:
            logo_img = PhotoImage(file="assets/images/logo_new.png")
            dialog.iconphoto(False, logo_img)
    except TclError:
        pass
        try:
            dialog.iconphoto(r"assets/logo.ico")
        except TclError:
            pass
            
    result = None

    big_frame = ttk.Frame(dialog)
    big_frame.pack(fill="both", expand=True)
    big_frame.columnconfigure(0, weight=1)
    big_frame.rowconfigure(0, weight=1)

    info_frame = ttk.Frame(big_frame, padding=(10, 12), style="Dialog_info.TFrame")
    info_frame.grid(row=0, column=0, sticky="nsew")
    info_frame.columnconfigure(1, weight=1)
    info_frame.rowconfigure(1, weight=1)

    try:
        color = big_frame.tk.call("set", "themeColors::dialogInfoBg")
    except tk.TclError:
        color = big_frame.tk.call("ttk::style", "lookup", "TFrame", "-background")

    title_label = ttk.Label(
        info_frame, text=title, anchor="nw", font=("", 14, "bold"), background=color
    )
    title_label.grid(row=0, column=1, sticky="nsew", padx=(12, 17), pady=(10, 8))

    detail_label = ttk.Label(info_frame, text=details, anchor="nw", background=color)
    detail_label.grid(row=1, column=1, sticky="nsew", padx=(12, 17), pady=(5, 10))

    button_frame = ttk.Frame(
        big_frame, padding=(22, 22, 12, 22), style="Dialog_buttons.TFrame"
    )
    button_frame.grid(row=2, column=0, sticky="nsew")

    def on_button(value):
        nonlocal result
        result = value
        dialog.destroy()

    for index, button_value in enumerate(buttons):
        style = None
        state = None
        default = False
        sticky = "nes" if len(buttons) == 1 else "nsew"

        if len(button_value) > 2:
            if button_value[2] == "accent":
                style = "Accent.TButton"
                default = True
            elif button_value[2] == "disabled":
                state = "disabled"
            elif button_value[2] == "default":
                default = True

        button = ttk.Button(
            button_frame,
            text=button_value[0],
            width=18,
            command=partial(on_button, button_value[1]),
            style=style,
            state=state,
        )
        if default:
            button.bind("<Return>", button["command"])
            button.focus()

        button.grid(row=0, column=index, sticky=sticky, padx=(0, 10))

        button_frame.columnconfigure(index, weight=1)

    dialog.update()

    dialog_width = dialog.winfo_width()
    dialog_height = dialog.winfo_height()

    if parent is None:
        parent_width = dialog.winfo_screenwidth()
        parent_height = dialog.winfo_screenheight()
        parent_x = 0
        parent_y = 0
    else:
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()

    x_coord = int(parent_width / 2 + parent_x - dialog_width / 2)
    y_coord = int(parent_height / 2 + parent_y - dialog_height / 2)

    dialog.geometry("+{}+{}".format(x_coord, y_coord))
    dialog.minsize(320, dialog_height)

    dialog.transient(parent)
    dialog.grab_set()

    dialog.wait_window()
    return result

# UPDATE
def createUpdatePopup(title="Title", details="Description", *, parent=None, icon=None):
    return popup(
        parent,
        title,
        details,
        icon,
        buttons=[("Yes", True, "accent"), ("No", False)],
    )

def checkForUpdates(current_version):
    import requests, webbrowser
    api_response = requests.get(
    "https://api.github.com/repos/Futura-Py/TimerX/releases/latest"
    )

    latest_tag = api_response.json()["tag_name"]

    try:
        latest_tag = latest_tag.lstrip("v")
    except:
        pass

    if latest_tag != current_version:
        answer = createUpdatePopup(title="Update Available", details="Do you want to Update TimerX?")
        if answer:
            webbrowser.open(api_response.json()["html_url"])
