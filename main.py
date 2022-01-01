# TimerX v0.2 by sumeshir26
# IMPORTS
import platform
from time import sleep
from tkinter import  Label, TclError, ttk, Tk, PhotoImage, Frame, StringVar
import tkinter
from tkinter.constants import  LEFT, RIGHT, Y
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

from tkinter.messagebox import showinfo

#Detect System theme & theme config

###############################################################
# Config:
#
# cfg[0] = theme
# cfg[1] = transparency_value
# 
#
###############################################################

global systheme, cfg

if darkdetect.theme() == "Dark":
    systheme = "dark"
else:
    systheme = "light"

theme = f"{systheme}"

use_sys_theme = 0

if os.path.isfile("./config/config.txt"):
    read_cfg = open("./config/config.txt", "r")
    cfg = read_cfg.readlines()

    theme = cfg[0]
    theme = theme.rstrip("\n")

    transparency_value = cfg[1]
    transparency_value = transparency_value.rstrip("\n")

    Play_Buzzer_Setting = cfg[2]
    Play_Buzzer_Setting = Play_Buzzer_Setting.rstrip("\n")

    Show_Notification_Setting = cfg[3]
    Show_Notification_Setting = Show_Notification_Setting.rstrip("\n")

    ontop = cfg[4]
    ontop = ontop.rstrip("\n")

    read_cfg.close()

else:
    if not os.path.isdir("./config"):
        os.makedirs("./config")

    make_cfg = open ("./config/config.txt", "w+")
    make_cfg.write("noconfig\nnoconfig\nnoconfig\nnoconfig\nnoconfig\n") # add another "noconfig\n" for every new setting
    make_cfg.close()

    read_cfg = open("./config/config.txt", "r")
    cfg = read_cfg.readlines()

    theme = cfg[0]
    theme = theme.rstrip("\n")

    transparency_value = cfg[1]
    transparency_value = transparency_value.rstrip("\n")

    Play_Buzzer_Setting = cfg[2]
    Play_Buzzer_Setting = Play_Buzzer_Setting.rstrip("\n")

    Show_Notification_Setting = cfg[3]
    Show_Notification_Setting = Show_Notification_Setting.rstrip("\n")

    ontop = cfg[4]
    ontop = ontop.rstrip("\n")

    read_cfg.close()

if theme == "System":
    if systheme == "dark":
        theme = "Dark"
    elif systheme == "light":
        theme = "Light"
    use_sys_theme = 1
elif theme == "noconfig":
    theme = f"{systheme}"
    use_sys_theme = 1

if theme == "dark":
    theme = "Dark"
if theme == "light":
    theme = "Light"

if theme == "Dark":
    lc_theme = "dark"
elif theme == "Light":
    lc_theme = "light"
elif theme == f"{systheme}":
    lc_theme = f"{systheme}"


if transparency_value == "noconfig":
    transparency_value = ".99"

if Play_Buzzer_Setting == "noconfig":
    Play_Buzzer_Setting = True
elif Play_Buzzer_Setting == "True":
    Play_Buzzer_Setting = True
elif Play_Buzzer_Setting == "False":
    Play_Buzzer_Setting = False

if Show_Notification_Setting == "noconfig":
    Show_Notification_Setting = True
elif Show_Notification_Setting == "True":
    Show_Notification_Setting = True
elif Show_Notification_Setting == "False":
    Show_Notification_Setting = False

print(ontop)

if ontop == "noconfig":
    ontop = False
elif ontop == "True":
    ontop = True
elif ontop == "False":
    ontop = False

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

# FUNCTIONS
def playBuzzer():
    playsound(r".\assets\sounds\sound1.wav")

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

    def shownotif():
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

    try:
        if new_show_notification_setting == True:
            shownotif()
    except:
        if Show_Notification_Setting == True:
            shownotif()

    try:
        if new_play_buzzer_setting == True:
            playBuzzer()
    except:
        if Play_Buzzer_Setting == True:
            playBuzzer()

def toggleAlwaysOnTop(app):
    global ontop, pin_button, theme
    if  ontop == True:
        app.attributes('-topmost', True)
        return
    else:
        app.attributes('-topmost', False)

toggleAlwaysOnTop(app)

################################################################################################

################################################################################################


#WINDOWS

def createManagerWindow(saveTimer, current_mins, current_secs, current_hrs):
    global manager_app_window
    manager_app_window = tkinter.Toplevel()
    manager_app_window.geometry('250x170')
    manager_app_window.title('Edit Timer')
    try:
        manager_app_window.attributes("-alpha", new_transparency_value)
    except:
        manager_app_window.attributes("-alpha", transparency_value)

    manager_app_window.resizable(False, False)

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
    global lc_theme, theme, cfg, value_label, New_Play_Buzzer_Setting

    settings_window = tkinter.Toplevel()
    settings_window.geometry('500x320')
    settings_window.title('Settings')
    settings_window.resizable(False, False)
    try:
        settings_window.attributes("-alpha", new_transparency_value)
    except:
        settings_window.attributes("-alpha", transparency_value)

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

    ###

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


    theme_label = ttk.Label(settings_window, text="  Change theme of the app", image=theme_dark, compound=LEFT)
    theme_label.place(x=23, y=23)

    transparency_label = ttk.Label(settings_window, text="  Adjust Transparency of the app", image=transparency_dark, compound=LEFT)
    transparency_label.place(x=23, y=73)

    speaker_label = ttk.Label(settings_window, text="  Play sound when timer ends", image=speaker_dark, compound=LEFT)
    speaker_label.place(x=23, y=123)

    bell_label = ttk.Label(settings_window, text="  Show notification when timer ends", image=bell_dark, compound=LEFT)
    bell_label.place(x=23, y=173)

    pin_label = ttk.Label(settings_window, text="  Keep app always on top", image=pin_dark, compound=LEFT)
    pin_label.place(x=23, y=223)


    ###

    try:
        if lc_new_theme == "dark":
            theme_label.configure(image=theme_dark)
            transparency_label.configure(image=transparency_dark)
            speaker_label.configure(image=speaker_dark)
            bell_label.configure(image=bell_dark)
            pin_label.configure(image=pin_dark)
        elif lc_new_theme == "light":
            theme_label.configure(image=theme_light)
            transparency_label.configure(image=transparency_light)
            speaker_label.configure(image=speaker_light)
            bell_label.configure(image=bell_light)
            pin_label.configure(image=pin_light)
    except:
        if lc_theme == "dark":
            theme_label.configure(image=theme_dark)
            transparency_label.configure(image=transparency_dark)
            speaker_label.configure(image=speaker_dark)
            bell_label.configure(image=bell_dark)
            pin_label.configure(image=pin_dark)
        elif lc_theme == "light":
            theme_label.configure(image=theme_light)
            transparency_label.configure(image=transparency_light)
            speaker_label.configure(image=speaker_light)
            bell_label.configure(image=bell_light)
            pin_label.configure(image=pin_light)

    ###

    box_current_value= StringVar(settings_window)

    try:
        if new_theme == "Dark" or "Light" or "System":
            box_current_value.set(f"{new_theme}")
    except:
        if use_sys_theme == 1:
            box_current_value.set("System")
        elif theme == "Dark":
            box_current_value.set("Dark")
        elif theme == "Light":
            box_current_value.set("Light")

    theme_combobox = ttk.Spinbox(settings_window, state="readonly", values=("Dark", "Light", "System"), wrap=True, textvariable=box_current_value)
    theme_combobox.place(x=275, y=20)

    ###

    current_value = tkinter.DoubleVar()

    didsliderload = 0

    def get_current_value():
        return ".{:.0f}".format(slider.get())

    def slider_changed(event):
        if didsliderload == 1:
            settings_window.attributes("-alpha", get_current_value())
            app.attributes("-alpha", get_current_value())

    slider = ttk.Scale(settings_window, from_=25, to=99, orient="horizontal", command=slider_changed, variable=current_value)

    transparency_value_nodot = transparency_value.lstrip(".")
    transparency_value_nodot = int(transparency_value_nodot)

    try:
        new_transparency_value_nodot = new_transparency_value.lstrip(".")
        slider.set(new_transparency_value_nodot)
    except:
        slider.set(transparency_value_nodot)
        
    slider.place(x=325, y=75)

    didsliderload = 1

    ###

    btn1 = ttk.Checkbutton(settings_window, style="Switch.TCheckbutton")
    try:
        if new_play_buzzer_setting == True:
            btn1.state(['!alternate', 'selected'])
        elif new_play_buzzer_setting == False:
            btn1.state(['!alternate'])
    except:
        if Play_Buzzer_Setting == True:
            btn1.state(['!alternate', 'selected'])
        elif Play_Buzzer_Setting == False:
            btn1.state(['!alternate'])
    btn1.place(x=360, y=125)

    ###

    btn2 = ttk.Checkbutton(settings_window, style="Switch.TCheckbutton")
    try:
        if new_show_notification_setting == True:
            btn2.state(['!alternate', 'selected'])
        elif new_show_notification_setting == False:
            btn2.state(['!alternate'])
    except:
        if Show_Notification_Setting == True:
            btn2.state(['!alternate', 'selected'])
        elif Show_Notification_Setting == False:
            btn2.state(['!alternate'])
    btn2.place(x=360, y=175)

    ###

    btn3 = ttk.Checkbutton(settings_window, style="Switch.TCheckbutton")
    if ontop == True:
        btn3.state(['!alternate', 'selected'])
    elif ontop == False:
        btn3.state(['!alternate'])
    btn3.place(x=360, y=215)

    def ApplyChanges():
        global theme, lc_theme, new_theme, lc_new_theme, new_transparency_value, new_play_buzzer_setting, new_show_notification_setting, ontop

        new_theme = theme_combobox.get()
        new_transparency_value = get_current_value()
        new_play_buzzer_setting = btn1.instate(['selected'])
        new_show_notification_setting = btn2.instate(["selected"])
        ontop = btn3.instate(["selected"])
        toggleAlwaysOnTop(app)

        cfg[0] = f"{new_theme}\n"
        cfg[1] = f"{new_transparency_value}\n"
        cfg[2] = f"{new_play_buzzer_setting}\n"
        cfg[3] = f"{new_show_notification_setting}\n"
        cfg[4] = f"{ontop}\n"
        
        savethemecfg = open("./config/config.txt", "w+")
        savethemecfg.writelines(cfg[0])
        savethemecfg.writelines(cfg[1])
        savethemecfg.writelines(cfg[2])
        savethemecfg.writelines(cfg[3])
        savethemecfg.writelines(cfg[4])
        savethemecfg.close


        if new_theme == "Dark":
            lc_new_theme = "dark"
        elif new_theme == "Light":
            lc_new_theme = "light"
        elif new_theme == "System":
            lc_new_theme = f"{systheme}"

        if new_theme == "Dark":
            app.tk.call("set_theme", "dark")
            settings_btn.configure(image=settings_image_dark)
        elif new_theme == "Light":
            app.tk.call("set_theme", "light")
            settings_btn.configure(image=settings_image_light)
        elif new_theme == "System":
            app.tk.call("set_theme", f"{systheme}")
            if systheme == "dark":
                settings_btn.configure(image=settings_image_dark)
            elif systheme == "light":
                settings_btn.configure(image=settings_image_light)
       
        settings_window.destroy()

    def CancelSettings():
        settings_window.destroy()

    okbtn = ttk.Button(settings_window, text="Apply Changes", command=lambda:ApplyChanges())
    okbtn.place(x=250, y=270)

    cancelbtn = ttk.Button(settings_window, text="Cancel", command=lambda:CancelSettings()) 
    cancelbtn.place(x=125, y=270)

    settings_window.mainloop() 


######################################################################################################

##################################################################################################



# APP THEME

try:
    app.attributes("-alpha", new_transparency_value)
except:
    app.attributes("-alpha", transparency_value)

app.tk.call("source", "sun-valley.tcl")
app.tk.call("set_theme", f"{lc_theme}")

#KEYBIMDS
app.bind('key-space', startstopButtonPressed)

# IMAGES

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

settings_btn = ttk.Button(master=window, image=settings_image_dark, command=lambda:createSettingsWindow(), style="Toolbutton")
settings_btn.place(x=5, y=163)

# THEMED IMAGES

if lc_theme == "dark":
    settings_btn.configure(image=settings_image_dark)
elif lc_theme == "light":
    settings_btn.configure(image=settings_image_light)   

# TKINTER MAINLOOP
app.mainloop()
