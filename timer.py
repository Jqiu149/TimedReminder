from tkinter import *
from tkinter import ttk
import time
import random
import os
import json
from supabase import create_client, Client
import threading
import socket
import threading.timer

MAX_VAL_SIGNED_INT_2BYTES = (2**15) - 1


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

# sets the next pop-up's break-message to input if it isn't empty
def set_break_message(message):
    if(message != ""):
        global break_message
        break_message = message

# creates the pop-up after the chosen break time
def setTimer():
    time.sleep(user_settings["default_timer_length"])
    CreatePopUpReminder()

# precondition: the user is connected to the internet
# stores the duration the pop-up existed for, and the user's id in our DB 
def storeData(startTime, endTime):
    if(not has_internet()):
         return;

    time_elapsed = int(endTime - startTime)
    user_id = user_settings["user_id"]; 

    try:
        if(time_elapsed > MAX_VAL_SIGNED_INT_2BYTES):
            time_elapsed =  MAX_VAL_SIGNED_INT_2BYTES
        supabase.table('user_data').insert({"user_id": user_id, "time_elapsed_seconds": time_elapsed}).execute(); 
    except Exception as e:
        print(e)
        pass

#creates the actual pop-up
def CreatePopUpReminder():
    global break_message 
    #store the time of creation of the timer
    timer_start_time = time.time()

    #creates the window + positions it 
    root = Tk() 
    root.geometry()
    xpos = root.winfo_screenwidth() // 2;
    ypos = root.winfo_screenheight() // 2; 
    root.geometry(f"+{xpos}+{ypos}")
    frame = ttk.Frame(root, padding=10)
    frame.grid()
    

    #window contents
    
    #break message
    ttk.Label(frame, text = break_message).grid(column =0, row = 0)
    break_message = user_settings["default_break_message"]

    # section to enter a custom message for the next pop-up. 
    ttk.Label(frame, text = "enter a custom message for next popUp if you want").grid(column = 0, row = 1)
    entryBox = ttk.Entry(frame)
    entryBox.grid(column = 1, row = 1)

    # 'again' button to schedule next pop-up
    ttk.Button(frame, text="set next reminder",command=lambda:[set_break_message(entryBox.get()), root.destroy(), storeData(timer_start_time, time.time()), setTimer()]).grid(column=3, row=1)    
                #hey REMMEBER THE ORDER OF THE FUCNTIONS PASSED IN HERE MATTER

    #quit button, means we don't schedule another pop-up
    ttk.Button(frame, text="quit program",command= lambda:[root.destroy(), storeData(timer_start_time, time.time())]).grid(column=4, row=1)    

    #potentially adds an extra message (that i think is cute or funny but uh.... might be cringe .______. ) 
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

#requires internet connection
#get the next availible userID for the user if they don't have one yet. 
if(has_internet()):
    try:
        if(user_settings["user_id"] is None):

            #(we attempt getting data from db first, so if it fails then we won't overwrite the file and stuff but not have smth to put in. )

            #try to get next availible id from our database and update the database. 
            new_user_id = supabase.table("user_id").select("*").execute().data[0]["next_user_id"]
            user_settings["user_id"] = new_user_id
            supabase.table("user_id").update({'next_user_id': user_settings["user_id"] + 1}).eq('next_user_id', user_settings["user_id"] ).execute()
            
            #store in local userdata
            user_settings_file = open('user_settings.json',"w")
            json.dump(user_settings, user_settings_file) 
            user_settings_file.close()
    except Exception as e:
        print(e)
        pass

#start timer for our first popUP. 
break_message = user_settings["default_break_message"]
setTimer(); 

