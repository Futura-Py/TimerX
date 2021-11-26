import tkinter
from tkinter import ttk

def createManagerWindow(saveTimer, current_mins, current_secs, current_hrs):
    manager_app_window = tkinter.Tk()
    manager_app_window.geometry('200x150')
    manager_app_window.title('TimerX Timer Manager')
    
    # APP THEME
    manager_app_window.tk.call("source", "sun-valley.tcl")
    manager_app_window.tk.call("set_theme", "light")

    # WINDOW FRAME
    manager_window = ttk.Frame(manager_app_window)
    manager_window.pack(fill="both", expand=True)

    timer_hr_label = ttk.Label(manager_window, text = 'Hours: ')
    timer_hr_label.grid(row = 1, column = 1, pady = 5)
    timer_hr_input = tkinter.Entry(manager_window)
    timer_hr_input.grid(row = 1, column = 2, pady = 5)
    timer_hr_input.insert(1, current_hrs)

    timer_min_label = ttk.Label(manager_window, text = 'Minutes: ')
    timer_min_label.grid(row = 2, column = 1, pady = 5)
    timer_min_input = tkinter.Entry(manager_window)
    timer_min_input.grid(row = 2, column = 2, pady = 5)
    timer_min_input.insert(1, current_mins)

    timer_sec_label = ttk.Label(manager_window, text = 'Seconds: ')
    timer_sec_label.grid(row = 3, column = 1, pady = 5)
    timer_sec_input = tkinter.Entry(manager_window)
    timer_sec_input.grid(row = 3, column = 2, pady = 5)
    timer_sec_input.insert(1, current_secs)

    ok_button = ttk.Button(manager_window, text = 'Ok!', command = lambda:saveTimer(timer_sec_input, timer_min_input, timer_hr_input, manager_app_window))
    ok_button.grid(row = 4, column = 2, pady = 5)

def createAboutWindow():
    about_window = tkinter.Tk()
    about_window.geometry('300x200')
    about_window.title('TimerX Timer Manager')

    logo = tkinter.PhotoImage(file = 'assets/images/logo.jpeg')

    about_window = tkinter.ttk(about_window, image = logo, bd = 0)
    about_window.grid(pady = 20)
