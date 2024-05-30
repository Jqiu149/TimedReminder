from tkinter import *
from tkinter import ttk
import time

TIMER_LENGTH = 20; 
DEFAULT_BREAK_MESSAGE = "take a small break for eyes at aleast. maybe a longer break if been working for a bit or stressed"

def setTimer():
    time.sleep(TIMER_LENGTH)
    CreatePopUpReminder()


def CreatePopUpReminder():
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Label(frm, text = DEFAULT_BREAK_MESSAGE).grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    ttk.Button(frm, text="again",command=lambda:[root.destroy(),setTimer()]).grid(column=2, row=0)    
    root.mainloop()


setTimer(); 

