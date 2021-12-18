import tkinter
from tkinter import ttk

def createManagerWindow(saveTimer, current_mins, current_secs, current_hrs):
    manager_app_window = tkinter.Tk()
    manager_app_window.geometry('235x162')
    manager_app_window.title('TimerX Timer Manager')

    manager_app_window.resizable(False, False)

    # APP THEME
    manager_app_window.tk.call("source", "sun-valley.tcl")
    manager_app_window.tk.call("set_theme", "light")

    # WINDOW FRAME
    manager_window = ttk.Frame(manager_app_window)
    manager_window.pack(fill="both", expand=True)

    timer_hr_label = ttk.Label(manager_window, text = 'Hours: ')
    #timer_hr_label.grid(row = 1, column = 1, pady = 5)
    timer_hr_label.place(x=17, y=17)
    timer_hr_input = ttk.Entry(manager_window)
    #timer_hr_input.grid(row = 1, column = 2, pady = 5, padx=10)
    timer_hr_input.place(x=65, y=10)
    timer_hr_input.insert(1, current_hrs)

    timer_min_label = ttk.Label(manager_window, text = 'Minutes: ')
    #timer_min_label.grid(row = 2, column = 1, pady = 5)
    timer_min_label.place(x=13, y=57)
    timer_min_input = ttk.Entry(manager_window)
    #timer_min_input.grid(row = 2, column = 2, pady = 5, padx=10)
    timer_min_input.place(x=65, y=50)
    timer_min_input.insert(1, current_mins)

    timer_sec_label = ttk.Label(manager_window, text = 'Seconds: ')
    #timer_sec_label.grid(row = 3, column = 1, pady = 5)
    timer_sec_label.place(x=12, y=97)
    timer_sec_input = ttk.Entry(manager_window)
    #timer_sec_input.grid(row = 3, column = 2, pady = 5, padx=10)
    timer_sec_input.place(x=65, y=90)
    timer_sec_input.insert(1, current_secs)

    ok_button = ttk.Button(manager_window, text = 'Ok!', command = lambda:saveTimer(timer_sec_input, timer_min_input, timer_hr_input, manager_app_window))
    #ok_button.grid(row = 4, column = 2, pady = 5)
    ok_button.place(x=95, y=126)

def createAboutWindow():
    about_window = tkinter.Tk()
    about_window.geometry('300x200')
    about_window.title('TimerX Timer Manager')

    logo = tkinter.PhotoImage(file = 'assets/images/logo.jpeg')

    about_window = tkinter.ttk(about_window, image = logo, bd = 0)
    about_window.grid(pady = 20)
