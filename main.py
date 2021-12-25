# TimerX v0.2 by sumeshir26
# IMPORTS
import platform
from time import sleep
from tkinter import  TclError, ttk, Tk, PhotoImage, Frame, StringVar
import tkinter
from tkinter.constants import  LEFT, RIGHT, SE, SW
from playsound import playsound
from threading import  Thread
from platform import system
import os
"""
# Disabled by default due to module unavailability on Linux
from BlurWindow.blurWindow import GlobalBlur, blur
"""
import ctypes
#from configurator import createManagerWindow, createSettingsWindow 
import darkdetect

global theme

if darkdetect.theme() == "Dark":
    theme = "dark"
else:
    theme = "light"

# TKINTER WINDOW
app = Tk()
app.title('TimerX')
app.geometry('300x210')
app.resizable(False, False)
app.update()
"""
# Disabled by default
HWND = ctypes.windll.user32.GetForegroundWindow()
GlobalBlur(HWND)
blur(HWND, hexColor='#12121240')
"""
# SYSTEM CODE
print(f'Running on {system}')
try:
    if  system() == "darwin":
        app.iconbitmap(r'assets/logo_new.icns')
        app.wm_attributes("-transparent", True)
        app.config(bg="systemTransparent")
    elif  system() == "Windows":
        app.iconbitmap(r'assets/logo_new.ico')
        from win10toast_click import ToastNotifier 
    elif  system() == "win":
        app.iconphoto(r'assets/logo_new.ico')
    else:
        logo_img = PhotoImage(file = 'assets/images/logo_new.png')
        app.iconphoto(False, logo_img)
except TclError:
    pass
    try:
        app.iconphoto(r'assets/logo.ico')
    except TclError:
        pass

# VARIABLES
app_on = True

timer_on = False
timer_paused = False

timer_seconds = 5
timer_minutes = 0
timer_hours = 0

ontop = False

# FUNCTIONS
def playBuzzer():
    playsound('./assets/sounds/sound1.wav')

def startstopButtonPressed():
    global timer_on, timer_paused
    if timer_on:
        timer_on = False
        timer_paused = True
        play_button.configure(text = "Play")
    elif timer_paused == False and timer_on == False:
        play_button.configure(text = "Pause")
        timer_thread = Thread(target=runTimer, daemon=True)
        timer_thread.start()
    else:
        timer_paused = False

def saveTimer(timer_sec_input, timer_min_input, timer_hr_input, manager_app_window):
    global timer_seconds, timer_minutes, timer_hours

    try:
        timer_seconds = int(timer_sec_input.get())
        timer_minutes = int(timer_min_input.get())
        timer_hours = int(timer_hr_input.get())
        time_selected_display.configure(text = f'Time Selected : {timer_hours}:{timer_minutes}:{timer_seconds}')
        time_display.configure(text = f'{timer_hours} : {timer_minutes} : {timer_seconds}')
        manager_app_window.destroy()
    except ValueError:
        time_selected_display.configure(text = "Please enter a number!")

def runTimer():
    global timer_seconds, timer_minutes, timer_hours, timer_on, app

    seconds_left = timer_seconds
    minutes_left = timer_minutes
    hours_left = timer_hours
    timer_on = True

    while True:
        if  timer_on and timer_paused == False:
            time_display.configure(text = f'{hours_left} : {minutes_left} : {seconds_left}')
            if seconds_left == 0 and minutes_left != 0:
                minutes_left -= 1
                seconds_left = 59
            elif seconds_left == 0 and minutes_left == 0 and hours_left != 0:
                hours_left -= 1
                minutes_left = 59
                seconds_left = 59
            elif seconds_left == 0 and timer_minutes == 0 and hours_left == 0:
                break
            else:
                seconds_left -= 1
            sleep(1)

        else:
            time_display.configure(text = f'{hours_left} : {minutes_left} : {seconds_left}')

    timer_on = False
    time_display.configure(text = f'{hours_left} : {minutes_left} : {seconds_left}')
    play_button.config(text = "Play")

    if  system() == "Windows":
        notification = ToastNotifier()
        notification.show_toast(
        "TimerX", 
        "Timer done!", 
        icon_path='./assets/logo.ico', 
        duration='None', 
        threaded=True,
        callback_on_click= app.focus_force() 
        )

    playBuzzer()

def toggleAlwaysOnTop(app):
    global ontop, pin_button, theme
    if  ontop == False:
        app.attributes('-topmost', True)
        ontop = True
        if  theme == 'dark':
            global unpin_image_dark
            pin_button.configure(image=unpin_image_dark)
        else:
            global unpin_image_light
            pin_button.configure(image=unpin_image_light)
        return
    else:
        app.attributes('-topmost', False)
        if  theme == 'dark':
            global pin_image_dark
            pin_button.configure(image=pin_image_dark)
        else:
            global pin_image_light
            pin_button.configure(image=pin_image_light)
        ontop = False


################################################################################################

################################################################################################


#WINDOWS

def createManagerWindow(saveTimer, current_mins, current_secs, current_hrs):
    global manager_app_window
    manager_app_window = tkinter.Tk()
    manager_app_window.geometry('250x170')
    manager_app_window.title('Edit Timer')

    manager_app_window.resizable(False, False)

    # APP THEME

    manager_app_window.tk.call("source", "sun-valley.tcl")

    if os.path.isfile("./config/theme.txt"):
        read_theme_cfg = open("./config/theme.txt", "r")

        theme_cfg = read_theme_cfg.read()

        if theme_cfg == "Dark":
            manager_app_window.tk.call("set_theme", "dark")
        elif theme_cfg == "Light":
            manager_app_window.tk.call("set_theme", "light")
        elif theme_cfg == "System":
            manager_app_window.tk.call("set_theme", f"{theme}")
    else:
        manager_app_window.tk.call("set_theme", f"{theme}")

    read_theme_cfg.close()

    try:
        if system() == "darwin":
            manager_app_window.iconbitmap(r'assets/logo_new.icns')
            manager_app_window.wm_attributes("-transparent", True)
            manager_app_window.config(bg="systemTransparent")
        elif  system() == "Windows":
            manager_app_window.iconbitmap(r'assets/logo_new.ico')
            from win10toast_click import ToastNotifier 
        elif  system() == "win":
            manager_app_window.iconphoto(r'assets/logo_new.ico')
        else:
            logo_img = PhotoImage(file = 'assets/images/logo.png')
            manager_app_window.iconphoto(False, logo_img)
    except TclError:
        pass

    # WINDOW FRAME
    manager_window = ttk.Frame(manager_app_window)
    manager_window.pack(fill="both", expand=True)

    timer_hr_label = ttk.Label(manager_window, text = 'Hours: ')
    timer_hr_label.place(x=17, y=17)
    timer_hr_input = ttk.Entry(manager_window)
    timer_hr_input.place(x=65, y=10)
    timer_hr_input.insert(1, current_hrs)

    timer_min_label = ttk.Label(manager_window, text = 'Minutes: ')
    timer_min_label.place(x=13, y=57)
    timer_min_input = ttk.Entry(manager_window)
    timer_min_input.place(x=65, y=50)
    timer_min_input.insert(1, current_mins)

    timer_sec_label = ttk.Label(manager_window, text = 'Seconds: ')
    timer_sec_label.place(x=12, y=97)
    timer_sec_input = ttk.Entry(manager_window)
    timer_sec_input.place(x=65, y=90)
    timer_sec_input.insert(1, current_secs)

    ok_button = ttk.Button(manager_window, text = 'Ok!', command = lambda:saveTimer(timer_sec_input, timer_min_input, timer_hr_input, manager_app_window))
    ok_button.place(x=95, y=126)

def createSettingsWindow():
    settings_window = tkinter.Tk()
    settings_window.geometry('300x210')
    settings_window.title('Settings')
    settings_window.resizable(False, False)

    settings_window.tk.call("source", "sun-valley.tcl")

    if os.path.isfile("./config/theme.txt"):
        read_theme_cfg = open("./config/theme.txt", "r")

        theme_cfg = read_theme_cfg.read()

        if theme_cfg == "Dark":
            settings_window.tk.call("set_theme", "dark")
        elif theme_cfg == "Light":
            settings_window.tk.call("set_theme", "light")
        elif theme_cfg == "System":
            settings_window.tk.call("set_theme", f"{theme}")
    else:
        settings_window.tk.call("set_theme", f"{theme}")

    read_theme_cfg.close()

    try:
        if system() == "darwin":
            settings_window.iconbitmap(r'assets/logo_new.icns')
            settings_window.wm_attributes("-transparent", True)
            settings_window.config(bg="systemTransparent")
        elif  system() == "Windows":
            settings_window.iconbitmap(r'assets/logo_new.ico')
            from win10toast_click import ToastNotifier 
        elif  system() == "win":
            settings_window.iconphoto(r'assets/logo_new.ico')
        else:
            logo_img = PhotoImage(file = 'assets/images/logo_new.png')
            settings_window.iconphoto(False, logo_img)
    except TclError:
        pass

    box_current_value= StringVar(settings_window)
    box_current_value.set("System")

    if os.path.isfile("./config/theme.txt"):
        read_theme_cfg = open("./config/theme.txt", "r")
        theme_cfg = read_theme_cfg.read()

        if theme_cfg == "Dark":
            box_current_value.set("Dark")
        elif theme_cfg == "Light":
            box_current_value.set("Light")
        elif theme_cfg == "System":
            box_current_value.set("System")

    read_theme_cfg.close()

    combobox = ttk.Spinbox(settings_window, state="readonly", values=("Dark", "Light", "System"), wrap=True, textvariable=box_current_value)
    combobox.pack()

    def ApplyChanges():
        new_theme = combobox.get()

        if os.path.isfile("./config/theme.txt"):
            os.remove("./config/theme.txt")

        if not os.path.isdir("./config"):
            os.makedirs("./config")
        
        savethemecfg = open("./config/theme.txt", "w+")
        savethemecfg.write(new_theme)
        savethemecfg.close

        if new_theme == "Dark":
            #settings_window.tk.call("set_theme", "dark")
            app.tk.call("set_theme", "dark")
            pin_button.configure(image=pin_image_dark)
        elif new_theme == "Light":
            #settings_window.tk.call("set_theme", "light")
            app.tk.call("set_theme", "light")
            pin_button.configure(image=pin_image_light)
        elif new_theme == "System":
            #settings_window.tk.call("set_theme", f"{theme}")
            app.tk.call("set_theme", f"{theme}")
        
        settings_window.destroy()

    def CancelSettings():
        settings_window.destroy()

    okbtn = ttk.Button(settings_window, text="Apply Changes", command=lambda:ApplyChanges())
    okbtn.place(x=150, y=150)

    cancelbtn = ttk.Button(settings_window, text="Cancel", command=lambda:CancelSettings()) 
    cancelbtn.place(x=25, y=150)

    settings_window.mainloop() 


######################################################################################################

##################################################################################################



# APP THEME

app.tk.call("source", "sun-valley.tcl")

if os.path.isfile("./config/theme.txt"):
    read_theme_cfg = open("./config/theme.txt", "r")

    theme_cfg = read_theme_cfg.read()

    if theme_cfg == "Dark":
        app.tk.call("set_theme", "dark")
    elif theme_cfg == "Light":
        app.tk.call("set_theme", "light")
    elif theme_cfg == "System":
        app.tk.call("set_theme", f"{theme}")
else:
    app.tk.call("set_theme", f"{theme}")

read_theme_cfg.close()

def switchTheme():
    global theme, app, pin_button, switch_theme_button
    if  theme == 'light':
        theme = 'dark'
        app.tk.call("set_theme", "dark")
        pin_button.configure(image=pin_image_dark)
    else:
        theme = 'light'
        app.tk.call("set_theme", "light")
        pin_button.configure(image=pin_image_light)

#KEYBIMDS
app.bind('key-space', startstopButtonPressed)

# IMAGES

switch_theme_image_light = PhotoImage(file=f"./assets/images/light/dark_theme.png")
switch_theme_image_dark = PhotoImage(file=f"./assets/images/dark/dark_theme.png")

pin_image_light = PhotoImage(file=f"./assets/images/light/pin.png")
pin_image_dark = PhotoImage(file=f"./assets/images/dark/pin.png")

unpin_image_light = PhotoImage(file=f"./assets/images/light/unpin.png")
unpin_image_dark = PhotoImage(file=f"./assets/images/dark/unpin.png")

settings_image_light = PhotoImage(file=f"./assets/images/light/settings.png")
settings_image_dark = PhotoImage(file=f"./assets/images/dark/settings.png")

# WINDOW FRAME
window = Frame(app)
window.pack(fill="both", expand=True)

# WINDOW ELEMENTS
time_selected_display = ttk.Label(master = window, text = f'Time Selected : {timer_seconds} Seconds')
time_selected_display.pack()

time_display = ttk.Label(master = window, text = f'{timer_hours} : {timer_minutes} : {timer_seconds}', font = ("any", 30))
time_display.pack(pady = 5)

play_button = ttk.Button(master = window, text = "Play", width = 25, command = startstopButtonPressed, style="Accent.TButton")
play_button.pack()

manager_button = ttk.Button(master =window, text = 'Edit Timer', command = lambda: createManagerWindow(saveTimer, timer_minutes, timer_seconds, timer_hours), width = 25)
manager_button.pack(pady = 5)

pin_button = ttk.Button(master=window, image=pin_image_light, command = lambda:toggleAlwaysOnTop(app), style="Toolbutton")
pin_button.pack(side=RIGHT, padx=(0, 5), pady=(5, 5))

settings_btn = ttk.Button(master=window, image=settings_image_dark, command=lambda:createSettingsWindow(), style="Toolbutton")
settings_btn.place(x=5, y=163)

# THEMED IMAGES

if os.path.isfile("./config/theme.txt"):
    read_theme_cfg = open("./config/theme.txt", "r")

    theme_cfg = read_theme_cfg.read()

    if theme_cfg == "Dark":
        pin_button.configure(image=pin_image_dark)
    elif theme_cfg == "Light":
        pin_button.configure(image=pin_image_light)
else:
    if  darkdetect.theme() == "Dark":
        pin_button.configure(image=pin_image_dark)
    else:
        pin_button.configure(image=pin_image_light)   

read_theme_cfg.close()

# TKINTER MAINLOOP
app.mainloop()
