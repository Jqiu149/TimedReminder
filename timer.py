import tkinter
from tkinter import Tk
from tkinter import ttk
import time
import random
import os
import json
from supabase import create_client, Client
import socket
import sched 
from functools import partial

MAX_VAL_SIGNED_INT_2BYTES = (2**15) - 1

scheduler = sched.scheduler()
add_on_messages = []

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

#recursively schedules the given tkinter window to be redrawn in time_to_redraw milliseconds. 
def schedule_redraw_r(window, time_to_redraw):
    window.after(time_to_redraw, lambda:[window.withdraw(), window.deiconify(), schedule_redraw_r(window, time_to_redraw)])

# sets the next pop-up's break-message to input. "" if empty
def set_break_message(message_addon, reminder_num):
    add_on_messages[reminder_num] = message_addon        


# precondition: the user is connected to the internet
# stores the duration the pop-up existed for, and the user's id in our DB 
def storeData(startTime, endTime):
    if(not has_internet()):
         return;

    time_elapsed = int(endTime - startTime)
    user_id = state["user_id"]; 

    try:
        if(time_elapsed > MAX_VAL_SIGNED_INT_2BYTES):
            time_elapsed =  MAX_VAL_SIGNED_INT_2BYTES
        supabase.table('user_data').insert({"user_id": user_id, "time_elapsed_seconds": time_elapsed}).execute(); 
    except Exception as e:
        print(e)
        pass

#creates a popup for the given reminder.
def CreatePopUpReminder(timer, timer_number):
    #store the time of creation of the timer
    timer_start_time = time.time()

    #creates the window + positions it 
    root = Tk() 
    root.title(timer["timer_name"])


    frame = ttk.Frame(root, padding=10)
    frame.grid()

    #window contents
    
    #break message
    for currentRow, message in enumerate(timer["timer_base_messages"]):
        ttk.Label(frame, text = message).grid(column =0, row = currentRow)
    
    currentRow+=1


    if add_on_messages[timer_number] != "":
        ttk.Label(frame, text = add_on_messages[timer_number]).grid(column =0, row = currentRow, pady = (20,20))
        currentRow+=1

    # section to enter a custom message for the next pop-up. 
    ttk.Label(frame, text = "enter a custom message for next popUp if you want").grid(column = 0, row = currentRow)
    entryBox = ttk.Entry(frame)
    entryBox.grid(column = 1, row = currentRow)

    # 'again' button to schedule next pop-up
    ttk.Button(
        frame, 
        text="set next reminder",
        command=lambda:[ set_break_message(entryBox.get(), timer_number),
            setTimer(timer, timer_number),
            root.destroy(),
            storeData(timer_start_time, time.time())]
        ).grid(column=3, row=currentRow)    

        #hey REMMEBER THE ORDER OF THE FUCNTIONS PASSED IN HERE MATTER

    #quit button, means we don't schedule another pop-up
    ttk.Button(frame, 
        text="quit program",
        command= lambda:[
            root.destroy(), 
            storeData(timer_start_time, time.time())]
        ).grid(column=4, row=currentRow)    

    currentRow+= 1

    #potentially adds an extra message (that i think is cute or funny but uh.... might be cringe .______. ) 
    if(random.randint(0,20) == 7):
        ttk.Label(frame, text = random.choice(state["extra_messages"])).grid(column =0, row = currentRow, pady = (40, 0))

    schedule_redraw_r(root, 1000000)

    root.mainloop()

def create_menu(timer_list):
    #create root window 
    window = Tk()

    #list storing buttons corresponding to each reminder telling us whether to create the correspodning reminder 
    timer_buttonState_list = []

    alarm_section_frame = ttk.Frame(window)
    alarm_section_frame.grid()
    #for each alarm in settings list, create a frame for it ig. 
        #display it's name/purpose, duration, whetehr or not it's currently in use / start button. 
    for alarm_num, alarm in enumerate(timer_list):
        timer_name = ttk.Label(alarm_section_frame, text=alarm["timer_name"])
        timer_name.grid(row = alarm_num, column = 0, padx = (0,100) )

        timer_duration = ttk.Label(alarm_section_frame, text=alarm["timer_duration_min"])
        timer_duration.grid(row = alarm_num, column = 1, padx = 20)

        state = tkinter.IntVar()
        select_button = ttk.Checkbutton(alarm_section_frame, var = state)
        select_button.grid(row = alarm_num, column = 2, padx = (20, 0))

        timer_buttonState_list.append((state, alarm))

    #create a 'plus button' thing that has behavior allow to add alarm to user settings. 
    #!!!
    frame = ttk.Frame(alarm_section_frame)
    frame.grid(row = alarm_num+1, column = 0,columnspan = 3)
    add_alarm_button = ttk.Button(frame, text = "add reminder")
    add_alarm_button.grid()

    add_alarm_button['command']  = lambda b = add_alarm_button: b.grid_forget()

    #... maybe way use image instead. want + thingy. 

    start_timers_button = ttk.Button(window, text = "start timers", command=lambda:[start_selected_timers(timer_buttonState_list), window.destroy(),scheduler.run()])
    start_timers_button.grid()

    window.mainloop()

def start_selected_timers(timer_buttonState_list):
    for timer_buttonState_pair in timer_buttonState_list:
        if(timer_buttonState_pair[0].get() == 1):
            setTimer(timer_buttonState_pair[1], len(add_on_messages))
            add_on_messages.append("")
        
#adds the timer to the scheduler queue 
def setTimer(timer, timer_number):
    scheduler.enter(timer["timer_duration_min"] * 60, 1, CreatePopUpReminder, argument=(timer,timer_number))


#create database connection client.
url: str = "https://wtzpvgzfdimeanwqofil.supabase.co" #os.environ.get("SUPABASE_URL")
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind0enB2Z3pmZGltZWFud3FvZmlsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTczNjQyNjUsImV4cCI6MjAzMjk0MDI2NX0.xjftldTnwLSoVKkKsBAdAmWJ5LKIex0_zJAOqPvMDE0"#os.environ.get("SUPABASE_KEY") 
supabase: Client = create_client(url, key)

#initialize program state using user_settings
settings_path = os.path.join( os.path.dirname(__file__), 'user_settings.json' )
user_settings_file = open(settings_path,"r")
state = json.load(user_settings_file)
user_settings_file.close()


#precondition: internet connection
#get the next availible userID for the user if they don't have one yet. 
if(has_internet()):
    try:
        if(state["user_id"] is None):

            #(we attempt getting data from db first, so if it fails then we won't overwrite the file and stuff but not have smth to put in. )

            #try to get next availible id from our database and update the database. 
            new_user_id = supabase.table("user_id").select("*").execute().data[0]["next_user_id"]
            state["user_id"] = new_user_id
            supabase.table("user_id").update({'next_user_id': state["user_id"] + 1}).eq('next_user_id', state["user_id"] ).execute()
            
            #store in local userdata
            user_settings_file = open('state.json',"w")
            json.dump(state, user_settings_file) 
            user_settings_file.close()
    except Exception as e:
        print(e)
        pass

create_menu(state["reminder_list"])