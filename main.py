# TimerX v1.3.0 by sumeshir26
# IMPORTS
from time import sleep
from tkinter import  TclError, ttk, Tk, PhotoImage, Frame
from tkinter.constants import  LEFT, RIGHT, SE, SW
from playsound import playsound
from threading import  Thread
import configurator
import darkdetect
from platform import system

# TKINTER WINDOW
app = Tk()
app.title('TimerX')
app.geometry('300x210')
app.resizable(False, False)

# APP ICON
print(f'Running on {system}')
try:
    if  system() == "darwin":
        app.iconbitmap(r'assets/logo.icns')
    elif  system() == "Windows":
        app.iconphoto(r'assets/logo.ico')
    elif  system() == "win":
        app.iconphoto(r'assets/logo.ico')
    else:
        logo_img = PhotoImage(file = 'assets/images/logo.png')
        app.iconphoto(False, logo_img)
except TclError:
    pass

# VARIABLES
app_on = True

timer_on = False
timer_paused = True

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
    global timer_seconds, timer_minutes, timer_hours, timer_on

    seconds_left = timer_seconds
    minutes_left = timer_minutes
    hours_left = timer_hours
    timer_done = False
    timer_on = True

    while timer_done == False:
        if timer_on:
            time_display.configure(text = f'{hours_left} : {minutes_left} : {seconds_left}')
            if seconds_left == 0 and minutes_left != 0:
                minutes_left -= 1
                seconds_left = 59
            elif seconds_left == 0 and minutes_left == 0 and hours_left != 0:
                hours_left -= 1
            elif seconds_left == 0 and timer_minutes == 0 and hours_left == 0:
                timer_done = True
            else:
                seconds_left -= 1
            sleep(1)

        elif timer_paused == False:
            seconds_left = timer_seconds
            minutes_left = timer_minutes
            hours_left = timer_hours
            time_display.configure(text = f'{timer_hours} : {timer_minutes} : {timer_seconds}')

        else:
            time_display.configure(text = f'{hours_left} : {minutes_left} : {seconds_left}')

    timer_on = False
    time_display.configure(text = f'{hours_left} : {minutes_left} : {seconds_left}')
    play_button.config(text = "Play")
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

# APP THEME

app.tk.call("source", "sun-valley.tcl")
theme = 'light'

if  darkdetect.theme() == "Dark":
    app.tk.call("set_theme", "dark")
    theme = 'dark'
else:
    app.tk.call("set_theme", "light")

def switchTheme():
    global theme, app, pin_button, switch_theme_button
    if  theme == 'light':
        theme = 'dark'
        app.tk.call("set_theme", "dark")
        switch_theme_button.configure(image=switch_theme_image_dark)
        pin_button.configure(image=pin_image_dark)
    else:
        theme = 'light'
        app.tk.call("set_theme", "light")
        pin_button.configure(image=pin_image_light)
        switch_theme_button.configure(image=switch_theme_image_light)

# IMAGES

switch_theme_image_light = PhotoImage(file=f"./assets/images/light/dark_theme.png")
switch_theme_image_dark = PhotoImage(file=f"./assets/images/dark/dark_theme.png")

pin_image_light = PhotoImage(file=f"./assets/images/light/pin.png")
pin_image_dark = PhotoImage(file=f"./assets/images/dark/pin.png")

unpin_image_light = PhotoImage(file=f"./assets/images/light/unpin.png")
unpin_image_dark = PhotoImage(file=f"./assets/images/dark/unpin.png")

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

manager_button = ttk.Button(master =window, text = 'Edit Timer', command = lambda: configurator.createManagerWindow(saveTimer, timer_minutes, timer_seconds, timer_hours), width = 25)
manager_button.pack(pady = 5)

switch_theme_button = ttk.Button(master=window, image=switch_theme_image_light, command=switchTheme, style="Toolbutton")
switch_theme_button.pack(side=LEFT, padx=5, pady=(5, 5))

pin_button = ttk.Button(master=window, image=switch_theme_image_light, command = lambda:toggleAlwaysOnTop(app), style="Toolbutton")
pin_button.pack(side=RIGHT, padx=(0, 5), pady=(5, 5))

# THEMED IMAGES
if  darkdetect.theme() == "Dark":
    switch_theme_button.configure(image=switch_theme_image_dark)
    pin_button.configure(image=pin_image_dark)

# TKINTER MAINLOOP
window.mainloop()
