from tkinter import *
from tkinter import ttk
import time
import random


TIMER_LENGTH = 1; # in seconds 
DEFAULT_BREAK_MESSAGE = "20 sec break for eyes. rah >:( .... or longer break if tired/stress."
break_message = DEFAULT_BREAK_MESSAGE; 

messages = [
    "you're doing great >~<",
    "you're slaying !!!!!", 
    "hey, you're super cool btw (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", 
    "\"postive message\"",
    "I apreciate you a lot honey ;---;",
    "thank you for trying your best !!!",
    "尽管你一再让我心碎，我想告诉你，如果有来生，我还是会选择和你一起，报税，开洗衣店",
    "you make me want to be a better man ;-----;",
    "thank you for being alive and waking up today.",
    "woah you're kinda cute (⁄ ⁄•⁄ω⁄•⁄ ⁄)"
]

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
    break_message = DEFAULT_BREAK_MESSAGE

    ttk.Label(frame, text = "enter a custom message for next time if you want").grid(column = 0, row = 1)
    
    entryBox = ttk.Entry(frame)
    entryBox.grid(column = 1, row = 1)

    ttk.Button(frame, text="again",command=lambda:[setMessage(entryBox.get()), root.destroy(),setTimer()]).grid(column=3, row=1)    
    #hey REMMEBER TH EORDER OF THE FUCNTIONS PASSED IN HERE MATTER

    if(random.randint(0,20) == 7):
        ttk.Label(frame, text = random.choice(messages)).grid(column =0, row = 3, pady = (40, 0))

    root.mainloop()

setTimer(); 

