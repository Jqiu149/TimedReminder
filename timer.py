from tkinter import *
from tkinter import ttk
import threading

def setTimer():
    my_timer = threading.Timer(1200, BreakPopUp)
    my_timer.start()


def BreakPopUp():
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text="5 min break >:(((( !").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    ttk.Button(frm, text="again",command=lambda:[setTimer(),root.destroy()]).grid(column=2, row=0)    
    root.mainloop()


my_timer = threading.Timer(1200, BreakPopUp)
my_timer.start()

