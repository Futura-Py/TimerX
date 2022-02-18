# TimerX v1.1
# IMPORTS
ver = "1.0"

import time
import tkinter
from unittest.loader import VALID_MODULE_NAME
import webbrowser
from pathlib import Path
from platform import system
from threading import Thread
from tkinter import Frame, PhotoImage, Tk, ttk
from tkinter.constants import DISABLED, LEFT

import darkdetect
import sv_ttk
from playsound import playsound

from utils import *

if not Path("config.json").exists():
    createConfig()

config = loadConfig(ver)

theme = config["theme"]
if config["theme"] == "System":
    if darkdetect.isDark():
        theme = "Dark"
    else:
        theme = "Light"

# TKINTER WINDOW
app = Tk()
app.title("TimerX")
app.minsize(width=300, height=210)

sv_ttk.set_theme(theme.lower())
bg_color = ttk.Style().lookup(".", "background")


# SYSTEM CODE
try:
    if system() == "darwin":
        app.iconbitmap("./assets/logo_new.icns")
    elif system() == "Windows":
        app.iconbitmap("./assets/logo_new.ico")
        from win10toast_click import ToastNotifier
    elif system() == "win":
        app.iconphoto("./assets/logo_new.ico")
    else:
        logo_img = PhotoImage(file="./assets/logo_new.png")
        app.iconphoto(False, logo_img)
except tkinter.TclError:
    try:
        app.iconphoto("assets/logo.ico")
    except tkinter.TclError:
        pass

# VARIABLES
app_on = True

timer_on = False
timer_paused = False

timer_seconds = int(config["default_seconds"])
timer_minutes = int(config["default_minutes"])
timer_hours = int(config["default_hours"])

# FUNCTIONS
def playBuzzer():
    playsound(config["sound_path"])
def playBuzzer(config):
    playsound(Path(config["sound_path"]))


def startstopButtonPressed(*_):
    global timer_on, timer_paused, timer_hours, timer_minutes, timer_seconds, last_paused
    
    if timer_on and not timer_paused:
        timer_on = False
        timer_paused = True
        last_paused = time.time()
        timer_hours = hours_left
        timer_minutes = minutes_left
        timer_seconds = seconds_left
        play_button.configure(text="Play")
    elif not timer_paused and not timer_on:
        play_button.configure(text="Pause")
        timer_thread = Thread(target=runTimer, daemon=True)
        timer_thread.start()
    else:
        timer_paused = False
        timer_on = True
        play_button.configure(text="Pause")


def saveTimer(secs, mins, hours, manager_app_window):
    global timer_seconds, timer_minutes, timer_hours

    timer_seconds = int(secs)
    timer_minutes = int(mins)
    timer_hours = int(hours)

    time_selected_display.configure(
        text=f"{hours} Hours, {mins} Minutes, {secs} Seconds"
    )
    time_display.configure(text=f"{hours} : {mins} : {secs}")

    if not manager_app_window == None:
        manager_app_window.destroy()


def showNotification():
    if system() == "Windows":
        notification = ToastNotifier()
        notification.show_toast(
            "TimerX",
            "Time's up!",
            icon_path="./assets/logo_new.ico",
            duration="None",
            threaded=True,
            callback_on_click=app.focus_force(),
        )


def runTimer():
    global timer_seconds, timer_minutes, timer_hours, timer_on, app, config, last_paused, seconds_left, minutes_left, hours_left

    timer_seconds = config["default_seconds"]
    timer_minutes = config["default_minutes"]
    timer_hours = config["default_hours"]

    seconds_left = timer_seconds
    minutes_left = timer_minutes
    hours_left = timer_hours
    milliseconds_left = 99
    timer_on = True

    last_paused = time.time()

    while True:
        if timer_on and not timer_paused:
            latest_time = time.time()

            time_to_subtract = round((latest_time - last_paused), 3)

            split_time = str(time_to_subtract).split(".")

            ty_res = time.gmtime(int(split_time[0]))
            formatted_time = time.strftime(f"%H:%M:%S:{split_time[1]}", ty_res)

            milliseconds_left -= int(split_time[1])
            split_fmt_time = formatted_time.split(":")
            hours_left = int(timer_hours) - int(split_fmt_time[0])
            minutes_left = int(timer_minutes) - int(split_fmt_time[1])
            seconds_left = int(timer_seconds) - int(split_fmt_time[2])

            if seconds_left < 0 and minutes_left == 0 and hours_left == 0:
                break

            if seconds_left < 0:
                subtract_secs = abs(seconds_left)
                seconds_left = 60 - subtract_secs
                minutes_left -= 1
            if minutes_left < 0:
                subtract_mins = abs(minutes_left)
                minutes_left = 60 - subtract_mins
                hours_left -= 1

            time_display.configure(
                text=f"{hours_left} : {minutes_left} : {seconds_left}"
            )

    timer_on = False
    play_button.config(text="Play")

    if config["notify"]:
        showNotification()
    if config["sound"]:
        playBuzzer()


def setAlwaysOnTop(app):
    app.attributes("-topmost", config["ontop"])


setAlwaysOnTop(app)

# WINDOWS
def createManagerWindow(saveTimer, current_mins, current_secs, current_hrs):
    global manager_app_window, config

    manager_app_window = tkinter.Toplevel()
    manager_app_window.geometry("250x170")
    manager_app_window.title("Edit Timer")
    manager_app_window.wait_visibility()  # Needed on Linux
    manager_app_window.attributes("-alpha", config["transperency"])
    manager_app_window.resizable(False, False)

    try:
        if system() == "darwin":
            manager_app_window.iconbitmap("./assets/logo_new.icns")
        elif system() == "Windows":
            manager_app_window.iconbitmap("./assets/logo_new.ico")
        elif system() == "win":
            manager_app_window.iconphoto("./assets/logo_new.ico")
        else:
            logo_img = PhotoImage(file="./assets/logo.png")
            manager_app_window.iconphoto(False, logo_img)
    except tkinter.TclError:
        pass

    # VALIDATION
    validate_command = manager_app_window.register(validate)

    # WINDOW FRAME
    manager_window = ttk.Frame(manager_app_window)
    manager_window.pack(fill="both", expand=True)

    timer_hr_label = ttk.Label(manager_window, text="Hours: ")
    timer_hr_label.place(x=17, y=17)
    timer_hr_input = ttk.Entry(
        manager_window, validate="key", validatecommand=(validate_command, "%P")
    )
    timer_hr_input.place(x=65, y=10)
    timer_hr_input.insert(1, current_hrs)

    timer_min_label = ttk.Label(manager_window, text="Minutes: ")
    timer_min_label.place(x=13, y=57)
    timer_min_input = ttk.Entry(
        manager_window, validate="key", validatecommand=(validate_command, "%P")
    )
    timer_min_input.place(x=65, y=50)
    timer_min_input.insert(1, current_mins)

    timer_sec_label = ttk.Label(manager_window, text="Seconds: ")
    timer_sec_label.place(x=12, y=97)
    timer_sec_input = ttk.Entry(
        manager_window, validate="key", validatecommand=(validate_command, "%P")
    )
    timer_sec_input.place(x=65, y=90)
    timer_sec_input.insert(1, current_secs)

    ok_button = ttk.Button(
        manager_window,
        text="Ok!",
        command=lambda: saveTimer(
            timer_sec_input.get(), timer_min_input.get(), timer_hr_input.get(), manager_app_window
        ),
        style="Accent.TButton",
    )
    ok_button.place(x=95, y=126)


def createSettingsWindow():
    global theme, config, sp

    settings_window = tkinter.Toplevel()
    settings_window.geometry("500x320")
    settings_window.title("Settings")
    settings_window.resizable(False, False)
    settings_window.wait_visibility()  # Needed on Linux
    settings_window.attributes("-alpha", config["transperency"])

    try:
        if system() == "darwin":
            settings_window.iconbitmap("./assets/logo_new.icns")
        elif system() == "Windows":
            settings_window.iconbitmap("./assets/logo_new.ico")
        elif system() == "win":
            settings_window.iconphoto("./assets/logo_new.ico")
        else:
            logo_img = PhotoImage(file="./assets/logo_new.png")
            settings_window.iconphoto(False, logo_img)
    except tkinter.TclError:
        pass

    tabview = ttk.Notebook(settings_window)
    tabview.pack(fill="both", expand=True)

    tab_1 = ttk.Frame(tabview)
    tab_2 = ttk.Frame(tabview)
    tab_3 = ttk.Frame(tabview)
    tab_4 = ttk.Frame(tabview)

    tabview.add(tab_1, text="Appearence")
    tabview.add(tab_2, text="Notifications & Sound")
    tabview.add(tab_3, text="Timer Defaults")
    tabview.add(tab_4, text="About")

    theme_label = ttk.Label(
        tab_1,
        text="  Change theme of the app",
        image=theme_dark,
        compound=LEFT,
    )
    theme_label.place(x=23, y=23)

    transparency_label = ttk.Label(
        tab_1,
        text="  Adjust Transparency of the app",
        image=transparency_dark,
        compound=LEFT,
    )
    transparency_label.place(x=23, y=73)

    pin_label = ttk.Label(
        tab_1, text="  Keep app always on top", image=pin_dark, compound=LEFT
    )
    pin_label.place(x=23, y=123)

    speaker_label = ttk.Label(
        tab_2,
        text="  Play sound when timer ends",
        image=speaker_dark,
        compound=LEFT,
    )
    speaker_label.place(x=23, y=23)

    bell_label = ttk.Label(
        tab_2,
        text="  Show notification when timer ends",
        image=bell_dark,
        compound=LEFT,
    )
    bell_label.place(x=23, y=73)

    pin_label = ttk.Label(
        tab_1,
        text="  Keep app always on top",
        image=pin_dark,
        compound=LEFT,
    )
    pin_label.place(x=23, y=123)

    logo_label = ttk.Label(tab_3, image=logo)
    logo_label.place(x=50, y=30)

    TimerX_Label = ttk.Label(tab_4, text="TimerX", font=("Arial Rounded MT Bold", 50))
    TimerX_Label.place(x=210, y=40)

    version_Label = ttk.Label(tab_4, text=f"Version: {ver}", font=("Segoe UI", "20"))
    version_Label.place(x=220, y=120)

    github_btn = ttk.Button(
        tab_4,
        text=" Fork on Github",
        image=github_logo_dark,
        compound=LEFT,
        command=lambda: webbrowser.open("https://github.com/Futura-Py/TimerX"),
    )
    github_btn.place(x=50, y=200)

    website_btn = ttk.Button(
        tab_4,
        text=" Check out our Website!",
        image=globe_dark,
        compound=LEFT,
        command=lambda: webbrowser.open("https://Futura-Py.netlify.app/"),
    )
    website_btn.place(x=250, y=200)

    if theme == "Dark":
        theme_label.configure(image=theme_dark)
        transparency_label.configure(image=transparency_dark)
        speaker_label.configure(image=speaker_dark)
        bell_label.configure(image=bell_dark)
        pin_label.configure(image=pin_dark)
        github_btn.configure(image=github_logo_dark)
        website_btn.configure(image=globe_dark)
    else:
        theme_label.configure(image=theme_light)
        transparency_label.configure(image=transparency_light)
        speaker_label.configure(image=speaker_light)
        bell_label.configure(image=bell_light)
        pin_label.configure(image=pin_light)
        github_btn.configure(image=github_logo_light)
        website_btn.configure(image=globe_light)

    theme_combobox = ttk.Combobox(
        tab_1,
        state="readonly",
        values=("Dark", "Light", "System"),
    )
    theme_combobox.set(config["theme"])
    theme_combobox.place(x=275, y=20)

    def slider_changed(value):
        value = float(value) / 100
        settings_window.attributes("-alpha", value)
        app.attributes("-alpha", value)

    slider = ttk.Scale(
        tab_1,
        from_=40,
        to=99,
        orient="horizontal",
        command=slider_changed,
    )
    slider.set(float(config["transperency"] * 100))
    slider.place(x=325, y=75)

    sound_button = ttk.Checkbutton(tab_2, style="Switch.TCheckbutton")
    if config["sound"]:
        sound_button.state(["!alternate", "selected"])
    else:
        sound_button.state(["!alternate"])
    sound_button.place(x=360, y=25)

    notify_button = ttk.Checkbutton(tab_2, style="Switch.TCheckbutton")
    if config["notify"]:
        notify_button.state(["!alternate", "selected"])
    else:
        notify_button.state(["!alternate"])
    notify_button.place(x=360, y=75)

    ontop_button = ttk.Checkbutton(tab_1, style="Switch.TCheckbutton")
    if config["ontop"]:
        ontop_button.state(["!alternate", "selected"])
    else:
        ontop_button.state(["!alternate"])
    ontop_button.place(x=360, y=125)

    def browse():
        filedialog = askopenfile(mode="r", filetypes=[("Audio Files", ["*.mp3", "*.wav"])])
        if not filedialog == None:
            sound_path_entry.delete(0, END)
            sound_path_entry.insert(1, filedialog.name)

    sound_path_entry = ttk.Entry(tab_2, width=35)
    sound_path_entry.insert(1, config["sound_path"])
    sound_path_entry.place(x=130, y=115)
    spe_error_lbl = tkinter.Label(tab_2, fg="red", font=("", 10), text="")
    spe_error_lbl.place(x=130, y=150)

    browse_btn = ttk.Button(tab_2, text="Browse", command=lambda: browse())
    browse_btn.place(x=410, y=115)

    default_secs_entry = ttk.Entry(tab_3)
    default_secs_entry.insert(1, config["default_seconds"])
    default_secs_entry.place(x=280, y=15)
    dse_error_lbl = tkinter.Label(tab_3, fg="red", font=("", 10), text="")
    dse_error_lbl.place(x=280, y=50)

    default_mins_entry = ttk.Entry(tab_3)
    default_mins_entry.insert(1, config["default_minutes"])
    default_mins_entry.place(x=280, y=85)
    dme_error_lbl = tkinter.Label(tab_3, fg="red", font=("", 10), text="")
    dme_error_lbl.place(x=280, y=120)

    default_hours_entry = ttk.Entry(tab_3)
    default_hours_entry.insert(1, config["default_hours"])
    default_hours_entry.place(x=280, y=155)
    dhe_error_lbl = tkinter.Label(tab_3, fg="red", font=("", 10), text="")
    dhe_error_lbl.place(x=280, y=190)

    def ApplyChanges():
        global theme

        config["theme"] = theme = theme_combobox.get()
        if theme == "System":
            if darkdetect.isDark():
                theme = "Dark"
            else:
                theme = "Light"

        config["transperency"] = float(slider.get()) / 100
        config["sound"] = sound_button.instate(["selected"])
        config["notify"] = notify_button.instate(["selected"])
        config["ontop"] = ontop_button.instate(["selected"])

        setAlwaysOnTop(app)
        saveConfig(config)

        sv_ttk.set_theme(theme.lower())

        if theme == "Dark":
            settings_btn.configure(image=settings_image_dark)
            time_display.configure(fg="white")
            time_selected_display.configure(fg="white")
        elif theme == "Light":
            settings_btn.configure(image=settings_image_light)
            time_display.configure(fg="black")
            time_selected_display.configure(fg="black")

        settings_window.destroy()

    def VerifyEntrys():
        global sp

        def ErrorDefaultSecs(reason):
            if reason == "wv":
                default_secs_entry.state(["invalid"])
                dse_error_lbl.configure(text="Enter a number below 60")
            elif reason == "not_int":
                default_secs_entry.state(["invalid"])
                dse_error_lbl.configure(text="Enter a number")
            elif reason == "wv-":
                default_secs_entry.state(["invalid"])
                dse_error_lbl.configure(text="Enter a number above 0")

        def ErrorDefaultMins(reason):
            if reason == "wv":
                default_mins_entry.state(["invalid"])
                dme_error_lbl.configure(text="Enter a number below 60")
            elif reason == "not_int":
                default_mins_entry.state(["invalid"])
                dme_error_lbl.configure(text="Enter a number")
            elif reason == "wv-":
                default_mins_entry.state(["invalid"])
                dme_error_lbl.configure(text="Enter a number above -1")

        def ErrorDefaultHours(reason):
            if reason == "wv":
                default_hours_entry.state(["invalid"])
                dhe_error_lbl.configure(text="Enter a number below 60")
            elif reason == "not_int":
                default_hours_entry.state(["invalid"])
                dhe_error_lbl.configure(text="Enter a number")
            elif reason == "wv-":
                default_hours_entry.state(["invalid"])
                dhe_error_lbl.configure(text="Enter a number above -1")

        def ErrorSoundPath():
            sound_path_entry.state(["invalid"])
            dse_error_lbl.configure(text="This file doesnt exist.")                

        validated = True

        try:
            void = int(default_secs_entry.get())
            if not void <= 60:               
                validated = False
                ErrorDefaultSecs("wv")
            if not void > 0:
                validated = False
                ErrorDefaultSecs("wv-")
        except ValueError:
            ErrorDefaultSecs("not_int")
            validated = False

        try:
            void = int(default_mins_entry.get())
            if not void <= 60:
                validated = False
                ErrorDefaultMins("wv")
            if not void > -1:
                validated = False
                ErrorDefaultMins("wv-")
        except ValueError:
            ErrorDefaultMins("not_int")
            validated = False

        try:
            void = int(default_hours_entry.get())
            if not void <= 24:
                validated = False
                ErrorDefaultHours("wv")
            if not void > -1:
                validated = False
                ErrorDefaultHours("wv-")
        except ValueError:
            ErrorDefaultHours("not_int")
            validated = False

        sp = sound_path_entry.get()
        sp = sp.replace("\\", "/")

        if not os.path.isfile(sp):
            ErrorSoundPath()
            validated = False

        if validated == True:
            ApplyChanges()

    okbtn = ttk.Button(
        tab_1,
        text="Apply Changes",
        command=lambda: VerifyEntrys(),
        style="Accent.TButton",
    )
    okbtn.place(x=250, y=230)

    cancelbtn = ttk.Button(
        tab_1, text="Cancel", command=lambda: settings_window.destroy()
    )
    cancelbtn.place(x=125, y=230)

    okbtn_2 = ttk.Button(
        tab_2,
        text="Apply Changes",
        command=lambda: VerifyEntrys(),
        style="Accent.TButton",
    )
    okbtn_2.place(x=250, y=230)

    cancelbtn_2 = ttk.Button(
        tab_2, text="Cancel", command=lambda: settings_window.destroy()
    )
    cancelbtn_2.place(x=125, y=230)

    okbtn_3 = ttk.Button(
        tab_3,
        text="Apply Changes",
        command=lambda: VerifyEntrys(),
        style="Accent.TButton",
    )
    okbtn_3.place(x=250, y=230)

    cancelbtn_3 = ttk.Button(
        tab_3, text="Cancel", command=lambda: settings_window.destroy()
    )
    cancelbtn_3.place(x=125, y=230)

    if not system() == "Windows" or system() == "win":
        notify_button.configure(state=DISABLED)

    def reset_dse(e):
        default_secs_entry.state(["!invalid"])
        dse_error_lbl.configure(text="")

    def reset_dme(e):
        default_mins_entry.state(["!invalid"])
        dme_error_lbl.configure(text="")

    def reset_dhe(e):
        default_hours_entry.state(["!invalid"])
        dhe_error_lbl.configure(text="")

    def reset_spe(e):
        sound_path_entry.state(["!invalid"])
        spe_error_lbl.configure(text="")

    default_secs_entry.bind("<FocusOut>", reset_dse)
    default_secs_entry.bind("<FocusIn>", reset_dse)
    default_secs_entry.bind("<KeyRelease>", reset_dse)

    default_mins_entry.bind("<FocusOut>", reset_dme)
    default_mins_entry.bind("<FocusIn>", reset_dme)
    default_mins_entry.bind("<KeyRelease>", reset_dme)

    default_hours_entry.bind("<FocusOut>", reset_dhe)
    default_hours_entry.bind("<FocusIn>", reset_dhe)
    default_hours_entry.bind("<KeyRelease>", reset_dhe)

    sound_path_entry.bind("<FocusOut>", reset_spe)
    sound_path_entry.bind("<FocusIn>", reset_spe)
    sound_path_entry.bind("<KeyRelease>", reset_spe)

    settings_window.mainloop()


# APP TRANSPERENCY
app.attributes("-alpha", config["transperency"])
    if system() not in {"Windows", "win"}:
        notify_button.configure(state=DISABLED)


# KEYBINDS
app.bind("<KeyPress-space>", startstopButtonPressed)

app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(2, weight=1)
app.grid_columnconfigure(1, weight=1)

# IMAGES
settings_image_light = PhotoImage(file="./assets/images/light/settings.png")
settings_image_dark = PhotoImage(file="./assets/images/dark/settings.png")

# WINDOW FRAME
window = Frame(app)

# WINDOW ELEMENTS
time_selected_display = tkinter.Label(
    master=app,
    text=f"{timer_hours} Hours, {timer_minutes} Minutes, {timer_seconds} Seconds",
    font=("Segoe UI Variable", 10),
    bg=bg_color,
    fg="white",
)
time_selected_display.grid(column=1, row=0, sticky="N", pady=10)

time_display = tkinter.Label(
    master=app,
    text=f"{timer_hours} : {timer_minutes} : {timer_seconds}",
    font=("Segoe UI Variable", 30),
    bg=bg_color,
    fg="white",
)
time_display.grid(column=1, row=0, sticky="", rowspan=2, pady=20)

play_button = ttk.Button(
    master=app,
    text="Play",
    width=25,
    command=startstopButtonPressed,
    style="Accent.TButton",
)
play_button.grid(column=1, row=0, sticky="S", rowspan=2)

manager_button = ttk.Button(
    master=app,
    text="Edit Timer",
    command=lambda: createManagerWindow(
        saveTimer, timer_minutes, timer_seconds, timer_hours
    ),
    width=25,
)
manager_button.grid(column=1, row=2, sticky="N", pady=10)

settings_btn = ttk.Button(
    master=app,
    image=settings_image_dark,
    command=lambda: createSettingsWindow(),
    style="Toolbutton",
)


def sizechanged(e):
    settings_btn.place(x=5, y=app.winfo_height() - 45)
    if app.winfo_height() >= 220:
        if app.winfo_height() > 250:
            if app.winfo_height() > 270:
                if app.winfo_height() > 290:
                    if app.winfo_height() > 330:
                        if app.winfo_height() > 350:
                            if app.winfo_height() > 370:
                                if app.winfo_height() > 390:
                                    if app.winfo_width() > 420:
                                        time_display.configure(
                                            font=("Segoe UI Variable", 100)
                                        )
                                        time_selected_display.configure(
                                            font=("Segoe UI Variable", 25)
                                        )
                            else:
                                if app.winfo_width() > 420:
                                    time_display.configure(
                                        font=("Segoe UI Variable", 90)
                                    )
                                    time_selected_display.configure(
                                        font=("Segoe UI Variable", 25)
                                    )
                        else:
                            if app.winfo_width() > 400:
                                time_display.configure(font=("Segoe UI Variable", 80))
                                time_selected_display.configure(
                                    font=("Segoe UI Variable", 25)
                                )
                    else:
                        if app.winfo_width() > 360:
                            time_display.configure(font=("Segoe UI Variable", 70))
                            time_selected_display.configure(
                                font=("Segoe UI Variable", 23)
                            )
                else:
                    if app.winfo_width() > 360:
                        time_display.configure(font=("Segoe UI Variable", 60))
                        time_selected_display.configure(font=("Segoe UI Variable", 20))
            else:
                if app.winfo_width() >= 300:
                    time_display.configure(font=("Segoe UI Variable", 50))
                    time_selected_display.configure(font=("Segoe UI Variable", 17))
        else:
            if app.winfo_width() >= 300:
                time_display.configure(font=("Segoe UI Variable", 40))
                time_selected_display.configure(font=("Segoe UI Variable", 13))
    else:
        time_display.configure(font=("Segoe UI Variable", 30))
        time_selected_display.configure(font=("Segoe UI Variable", 10))

    play_button.configure(width=int(app.winfo_width() / 12))
    manager_button.configure(width=int(app.winfo_width() / 12))


def makeWindowsBlur(window):
    from ctypes import windll

    from BlurWindow.blurWindow import GlobalBlur

    GlobalBlur(
        windll.user32.GetParent(window.winfo_id()),
        Acrylic=True,
        Dark=(theme == "Dark"),
        hexColor=bg_color,
    )


# LOAD IMAGES
theme_dark = PhotoImage(file="./assets/images/dark/dark_theme.png")
theme_light = PhotoImage(file="./assets/images/light/dark_theme.png")

transparency_dark = PhotoImage(file="./assets/images/dark/transparency.png")
transparency_light = PhotoImage(file="./assets/images/light/transparency.png")

speaker_dark = PhotoImage(file="./assets/images/dark/speaker.png")
speaker_light = PhotoImage(file="./assets/images/light/speaker.png")

bell_dark = PhotoImage(file="./assets/images/dark/bell.png")
bell_light = PhotoImage(file="./assets/images/light/bell.png")

pin_dark = PhotoImage(file="./assets/images/dark/pin.png")
pin_light = PhotoImage(file="./assets/images/light/pin.png")

github_logo_dark = PhotoImage(file="./assets/images/dark/github.png")
github_logo_light = PhotoImage(file="./assets/images/light/github.png")

globe_dark = PhotoImage(file="./assets/images/dark/globe.png")
globe_light = PhotoImage(file="./assets/images/light/globe.png")

logo = PhotoImage(file="./assets/logo_new_150x150.png")


if theme == "Dark":
    settings_btn.configure(image=settings_image_dark)
elif theme == "Light":
    settings_btn.configure(image=settings_image_light)
    time_display.configure(fg="black")
    time_selected_display.configure(fg="black")

if system() == "Windows":
    makeWindowsBlur(app)

app.bind("<Configure>", sizechanged)
app.wait_visibility()  # Needed on Linux
app.attributes("-alpha", config["transperency"])

# UPDATE
app.after(
    500, Thread(target=checkForUpdates, args=(ver,)).start
)  # Doesn't freeze the GUI while checking for updates

# TKINTER MAINLOOP
app.mainloop()
