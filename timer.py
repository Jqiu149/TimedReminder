from tkinter import *
from tkinter import ttk
import time
import random
import os
import json
from supabase import create_client, Client
import threading
import socket

MAX_VAL_SINT_4BYTES = (2**30) - 1

#thank you internet person
def has_internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except :
        return False

def set_break_message(message):
    if(message != ""):
        global break_message
        break_message = message

def setTimer():
    time.sleep(user_settings["default_timer_length"])
    CreatePopUpReminder()

def storeData(startTime, endTime):
    if(not has_internet()):
         return;

    time_elapsed = int(endTime - startTime)
    user_id = user_settings["user_id"]; 

    try:
        if(time_elapsed > MAX_VAL_SINT_4BYTES or time_elapsed < 0):
            time_elapsed = None
        supabase.table('user_data').insert({"user_id": user_id, "time_elapsed_seconds": time_elapsed}).execute(); 
    except Exception as e:
        print(e)
        pass

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

    ttk.Button(frame, text="again",command=lambda:[set_break_message(entryBox.get()), root.destroy(), storeData(timer_start_time, time.time()), setTimer()]).grid(column=3, row=1)    
    #hey REMMEBER THE ORDER OF THE FUCNTIONS PASSED IN HERE MATTER

    ttk.Button(frame, text="quit",command= lambda:[root.destroy(), storeData(timer_start_time, time.time())]).grid(column=4, row=1)    

    if(random.randint(0,20) == 7):
        ttk.Label(frame, text = random.choice(user_settings["extra_messages"])).grid(column =0, row = 3, pady = (40, 0))

    root.mainloop()


#create database connection client.
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY") 
supabase: Client = create_client(url, key)

#initialize user settings 
settings_path = os.path.join( os.path.dirname(__file__), 'user_settings.json' )
user_settings_file = open(settings_path,"r")
user_settings = json.load(user_settings_file)
user_settings_file.close()

if(has_internet()):
    try:
        if(user_settings["user_id"] is None):
            #attempt getting data from db first, so if it fails then we won't overwrite the file and stuff but not have smth to put in. 
            new_user_id = supabase.table("user_id").select("*").execute().data[0]["next_user_id"]
            user_settings["user_id"] = new_user_id
            supabase.table("user_id").update({'next_user_id': user_settings["user_id"] + 1}).eq('next_user_id', user_settings["user_id"] ).execute()
            
            user_settings_file = open('user_settings.json',"w")
            json.dump(user_settings, user_settings_file) #seems like not happenign until program ends? or maybe 
            user_settings_file.close()
    except Exception as e:
        print(e)
        pass

break_message = user_settings["default_break_message"]
setTimer(); 

