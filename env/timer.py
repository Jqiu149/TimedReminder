from tkinter import *
from tkinter import ttk
import time
import random
import os
import json
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

MAX_VAL_SINT_4BYTES = (2**30) - 1

def set_break_message(message):
    if(message != ""):
        global break_message
        break_message = message

def setTimer():
    time.sleep(user_settings["default_timer_length"])
    CreatePopUpReminder()

def storeData(startTime, endTime):
    print("hey commented the data storing out for now, uncomment later")
    # time_elapsed = int(endTime - startTime)
    # user_id = user_settings["user_id"]; 

    # if(time_elapsed > MAX_VAL_SINT_4BYTES or time_elapsed < 0):
    #     time_elapsed = None
    # supabase.table('userData').insert({"userId": user_id, "time_elapsed_seconds": time_elapsed}).execute(); 

def CreatePopUpReminder():
    global break_message
    
    timer_start_time = time.time()
    root = Tk() #initializes tcl/tk interpreter thingy? is the gui interface
                #also creates root window? 
    
    root.geometry()
    xpos = root.winfo_screenwidth() // 2;
    ypos = root.winfo_screenheight() // 2; 

    root.geometry(f"+{xpos}+{ypos}")

    frame = ttk.Frame(root, padding=10)
    frame.grid()
    
    ttk.Label(frame, text = break_message).grid(column =0, row = 0)
    break_message = user_settings["default_break_message"]

    ttk.Label(frame, text = "enter a custom message for next popUp if you want").grid(column = 0, row = 1)
    
    entryBox = ttk.Entry(frame)
    entryBox.grid(column = 1, row = 1)

    ttk.Button(frame, text="again",command=lambda:[storeData(timer_start_time, time.time()), set_break_message(entryBox.get()), root.destroy(),setTimer()]).grid(column=3, row=1)    
    #hey REMMEBER THE ORDER OF THE FUCNTIONS PASSED IN HERE MATTER

    ttk.Button(frame, text="quit",command= lambda:[storeData(timer_start_time, time.time()),root.destroy()]).grid(column=4, row=1)    

    if(random.randint(0,20) == 7):
        ttk.Label(frame, text = random.choice(user_settings["extra_messages"])).grid(column =0, row = 3, pady = (40, 0))

    root.mainloop()


#initialize user settings 
user_settings_file = open('user_settings.json',"r")
user_settings = json.load(user_settings_file)
user_settings_file.close()

if(user_settings["user_id"] is None):
    user_settings_file = open('user_settings.json',"w")
    user_settings["user_id"] = supabase.table("user_id").select("*").execute().data[0]["next_user_id"]
    supabase.table("user_id").update({'next_user_id': user_settings["user_id"] + 1}).eq('next_user_id', user_settings["user_id"] ).execute()
    json.dump(user_settings, user_settings_file) #seems like not happenign until program ends? or maybe 
    user_settings_file.close()

break_message = user_settings["default_break_message"]
setTimer(); 

