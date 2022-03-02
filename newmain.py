from tkinter import Tk

class BaseApp:
    def __init__(self, resizable_height:bool=True, resizable_width:bool=True, title:str="TimerX") -> None:
        self.app = Tk()
        self.app.title(title)
        self.app.resizable(resizable_height, resizable_width)