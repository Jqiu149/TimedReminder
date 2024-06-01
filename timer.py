from tkinter import *
from tkinter import ttk
import time

TIMER_LENGTH = 20 * 60; 
DEFAULT_BREAK_MESSAGE = "20 sec break for eyes. rah >:( .... or longer break if tired/stress."
break_message = DEFAULT_BREAK_MESSAGE; 

def setMessage(message):
    if(message != ""):
        global break_message
        break_message = message

def setTimer():
    time.sleep(TIMER_LENGTH)
    CreatePopUpReminder()


def CreatePopUpReminder():
    global break_message 

    root = Tk()
    frame = ttk.Frame(root, padding=10)
    frame.grid()
    
    ttk.Label(frame, text = break_message).grid(column =0, row = 0)
    
    ttk.Label(frame, text = "enter a custom message for next time if you want").grid(column = 0, row = 1)
    
    entryBox = ttk.Entry(frame)
    entryBox.grid(column = 1, row = 1)

    ttk.Button(frame, text="again",command=lambda:[setMessage(entryBox.get()), root.destroy(),setTimer()]).grid(column=3, row=1)    
    #hey REMMEBER TH EORDER OF THE FUCNTIONS PASSED IN HERE MATTER

    root.mainloop()

setTimer(); 

