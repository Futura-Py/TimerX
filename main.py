# TimerX v1.3.0 by sumeshir26
# IMPORTS
from time import sleep
from tkinter import ttk, Tk, PhotoImage, Frame
from playsound import playsound
import threading
import configurator
import platform

# TKINTER WINDOW
app = Tk()
app.title('TimerX')
app.geometry('300x200')

print(platform.system())
if  platform.system() == "Linux":
    logo_img = PhotoImage(file = 'assets/images/logo.jpeg')
    app.iconphoto(False, logo_img)
elif  platform.system() == "Darwin":
    app.iconbitmap(r'assets/logo.icns')
elif  platform.system() == "Windows":
    app.iconphoto(r'assets/logo.ico')

# VARIABLES
app_on = True

default_font = './assets/fonts/font.ttf'

timer_on = False
timer_paused = True

timer_seconds = 5
timer_minutes = 0
timer_hours = 0

# FUNCTIONS
def playBuzzer():
    playsound('./assets/sounds/sound1.wav')

def startstopButtonPressed():
    global timer_on, timer_paused
    if timer_on:
        timer_on = False
        timer_paused = True
        # play_button.configure(image = play_button_img)
        play_button.configure(text = "Play")
    elif timer_paused == False and timer_on == False:
        #play_button.configure(image = pause_button_img)
        play_button.configure(text = "Pause")
        timer_thread = threading.Thread(target=runTimer, daemon=True)
        timer_thread.start()
    else:
        timer_paused = False

def saveTimer(timer_sec_input, timer_min_input, timer_hr_input, manager_window, manager_app):
    global timer_seconds, timer_minutes, timer_hours
    try:
        timer_seconds = int(timer_sec_input.get())
    except ValueError:
        time_selected_display.configure(text = "Please enter a number!")
        timer_minutes = int(timer_min_input.get())
        timer_hours = int(timer_hr_input.get())
        time_selected_display.configure(text = f'Time Selected : {timer_seconds} Seconds')
        time_display.configure(text = f'{timer_hours} : {timer_seconds} : {timer_seconds}')
        print('DESTRUCTION MODE')
        manager_app.destroy()
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
            sleep(1)
            #execution_start_time = time.time()
            time_display.configure(text = f'{hours_left} : {minutes_left} : {seconds_left}')
            if seconds_left == 0 and minutes_left != 0:
                minutes_left -= 1
                seconds_left = 59
            elif seconds_left == 0 and minutes_left == 0 and hours_left != 0:
                hours_left -= 1
            elif seconds_left == 0 and timer_minutes == 0 and hours_left == 0:
                timer_done = True
            else:
                seconds_left -= 1 #(time.time() - execution_start_time)
        elif timer_paused == False:
            seconds_left = timer_seconds
            minutes_left = timer_minutes
            hours_left = timer_hours
            time_display.configure(text = f'{timer_hours} : {timer_minutes} : {timer_seconds}')
        else:
            time_display.configure(text = f'{hours_left} : {minutes_left} : {seconds_left}')

    timer_on = False
    time_display.configure(text = f'{hours_left} : {minutes_left} : {seconds_left}')
    #play_button.config(image = play_button_img)
    play_button.config(text = "Pause")
    playBuzzer()

# IMAGES


# play_button_img = PhotoImage(file = 'assets/images/play_arrow.png')
# pause_button_img = PhotoImage(file = 'assets/images/pause_bars.png')

# APP THEME
app.tk.call("source", "sun-valley.tcl")
app.tk.call("set_theme", "light")

# WINDOW FRAME
window = Frame(app)
window.pack(fill="both", expand=True)

# WINDOW ELEMENTS
time_selected_display = ttk.Label(master = window, text = f'Time Selected : {timer_seconds} Seconds')
time_selected_display.pack()

time_display = ttk.Label(master = window, text = f'{timer_hours} : {timer_minutes} : {timer_seconds}', font = ("any", 30))
time_display.pack(pady = 5)

# play_button = ttk.Button(master = window, image = play_button_img, width = 20, command = startstopButtonPressed, style="Accent.TButton")
play_button = ttk.Button(master = window, text = "Play", width = 25, command = startstopButtonPressed, style="Accent.TButton")
play_button.pack()

manager_button = ttk.Button(master =window, text = 'Edit Timer', command = lambda: configurator.createManagerWindow(saveTimer, timer_minutes, timer_seconds, timer_hours), width = 25)
manager_button.pack(pady = 5)

about_button = ttk.Button(master =window, text = 'About', command = configurator.createAboutWindow, width = 25)
about_button.pack()

# TKINTER MAINLOOP
window.mainloop()
