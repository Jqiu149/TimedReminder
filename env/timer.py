from tkinter import *
from tkinter import ttk
import time
import random
import os

from supabase import create_client, Client


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

TIMER_LENGTH = 20*60; # in seconds 
DEFAULT_BREAK_MESSAGE = "20 sec break for eyes. rah >:( .... or longer break if tired/stress."
break_message = DEFAULT_BREAK_MESSAGE; 

MAX_VAL_SINT_4BYTES = (2**30) - 1

messages = [
    "you're doing great >~<",
    "you're slaying !!!!!", 
    "hey, you're super cool btw (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", 
    "\"postive message\"",
    "I apreciate you a lot honey ;---;",
    "thank you for trying your best !!!",
    "尽管你一再让我心碎，我想告诉你，如果有来生，我还是会选择和你一起，报税，开洗衣店 ;-----------; hhhhhhhh",
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

def storeData(startTime, endTime):
    time_elapsed = int(endTime - startTime)
    user_id = 1; 

    if(time_elapsed > MAX_VAL_SINT_4BYTES or time_elapsed < 0):
        time_elapsed = None
    supabase.table('userData').insert({"userId": user_id, "time_elapsed_seconds": time_elapsed}).execute(); 

def CreatePopUpReminder():
    global break_message, timer_start_time

    root = Tk() #initializes tcl/tk interpreter thingy? is the gui interface
                #also creates root window? 
    
    root.geometry()
    xpos = root.winfo_screenwidth() // 2;
    ypos = root.winfo_screenheight() // 2; 

    root.geometry(f"+{xpos}+{ypos}")

    frame = ttk.Frame(root, padding=10)
    frame.grid()
    
    ttk.Label(frame, text = break_message).grid(column =0, row = 0)
    break_message = DEFAULT_BREAK_MESSAGE

    ttk.Label(frame, text = "enter a custom message for next popUp if you want").grid(column = 0, row = 1)
    
    entryBox = ttk.Entry(frame)
    entryBox.grid(column = 1, row = 1)

    ttk.Button(frame, text="again",command=lambda:[storeData(timer_start_time, time.time()), setMessage(entryBox.get()), root.destroy(),setTimer()]).grid(column=3, row=1)    
    #hey REMMEBER TH EORDER OF THE FUCNTIONS PASSED IN HERE MATTER

    ttk.Button(frame, text="quit",command= lambda:[storeData(timer_start_time, time.time()),root.destroy()]).grid(column=4, row=1)    

    if(random.randint(0,20) == 7):
        ttk.Label(frame, text = random.choice(messages)).grid(column =0, row = 3, pady = (40, 0))

    timer_start_time= time.time()
    root.mainloop()

timer_start_time = 0
setTimer(); 

