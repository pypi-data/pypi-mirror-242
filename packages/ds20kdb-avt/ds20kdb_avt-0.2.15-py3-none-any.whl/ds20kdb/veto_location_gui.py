#!/usr/bin/env python3
"""
The GUI permits to add entries in the <object>_location tables in order to update the location of a object.
It performs a check of the QR code, which could by any object.

 Input: a QR code, location details (Institute, timestamp, status, comment)
 Output: history of the object and post on the DB object>_location table

---

Author: P.Franchini - p.franchini@lancaster.ac.uk
"""

import datetime
import re
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

import numpy as np
import pandas as pd
from tkcalendar import Calendar

from ds20kdb import interface;


dbi = interface.Database();

#===========================================

# Functions to check if a timestamp is not in the specified format
def is_valid_date_format(input_string):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(pattern, input_string))

def is_valid_time_format(input_string):
    pattern = r'^\d{2}:\d{2}:\d{2}$'
    return bool(re.match(pattern, input_string))

# Check button
def check_command():
    
    # Clear error, output and history box
    error_label.config(text="")
    output_label.config(text="")
    text_box.delete("1.0", tk.END)
    
    selected_qrcode = qrcode_var.get()

    # check QR code
    vpcb_id = None
    try:
        vpcb_id = dbi.get('vpcb',qrcode=selected_qrcode).data.vpcb_pid.iloc[0]
        object='vpcb'
    except:
        try:
            vmotherboard_id = dbi.get('vmotherboard',qrcode=selected_qrcode).data.vmotherboard_pid.iloc[0]
            object='vmotherboard'
        except:
            error_label.config(text="QR code is not present in the DB")
            return False

    if vpcb_id is not None:
        vpcb_asic_id = None
        try:
            vpcb_asic_id = dbi.get('vpcb_asic',vpcb_id=vpcb_id).data.vpcb_asic_pid.iloc[0]
            object='vpcb_asic'
        except:
            pass

        if vpcb_asic_id is not None:
            try:
                vtile_id = dbi.get('vtile',vpcb_asic_id=vpcb_asic_id).data.vtile_pid.iloc[0]
                object='vtile'
            except:
                pass
    elif vmotherboard_id is not None:
        try:
            vpdu_id = dbi.get('vpdu',vmotherboard_id=vmotherboard_id).data.vpdu_pid.iloc[0]
            object='vpdu'
        except:
            pass

    output_label.config(text=object)

    # Print history of last statuses
    location_df = dbi.get(f"{object}_location",**{f"{object}_id": vars()[f"{object}_id"]}).data
    institute_df = dbi.get('institute').data
    history = pd.merge(location_df, institute_df, left_on='institute_id', right_on='id', how='left') # merge 2 dataframes to get the acronym for each location entry
    history.rename(columns={'acronym': 'location'}, inplace=True)
    print(history[['timestamp', 'location', 'state', 'comment']])
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, history[['timestamp', 'location', 'state', 'comment']].to_string(index=False))

    # One can now submit since the Check was fine
    submit_button.config(state="normal")

    return

# Submit button
def submit_command():

    # reset the error message label
    error_label.config(text="")
    output_label.config(text="")
    
    selected_location = location_var.get()

    selected_date = timestamp_date_var.get()
    selected_time = timestamp_time_var.get()
    timestamp=selected_date+'T'+selected_time

    # check timestamp
    if not is_valid_date_format(selected_date):
        error_label.config(text="Date is not in the specified format")
        return

    if not is_valid_time_format(selected_time):
        error_label.config(text="Time is not in the specified format")
        return

    selected_status = status_var.get()
    selected_qrcode = qrcode_var.get()

    # check QR code
    vpcb_id = None
    try:
        vpcb_id = dbi.get('vpcb',qrcode=selected_qrcode).data.vpcb_pid.iloc[0]
        object='vpcb'
    except:
        try:
            vmotherboard_id = dbi.get('vmotherboard',qrcode=selected_qrcode).data.vmotherboard_pid.iloc[0]
            object='vmotherboard'
        except:
            error_label.config(text="QR code is not present in the DB")
            return False

    if vpcb_id is not None:
        vpcb_asic_id = None
        try:
            vpcb_asic_id = dbi.get('vpcb_asic',vpcb_id=vpcb_id).data.vpcb_asic_pid.iloc[0]
            object='vpcb_asic'
        except:
            pass

        if vpcb_asic_id is not None:
            try:
                vtile_id = dbi.get('vtile',vpcb_asic_id=vpcb_asic_id).data.vtile_pid.iloc[0]
                object='vtile'
            except:
                pass
    elif vmotherboard_id is not None:
        try:
            vpdu_id = dbi.get('vpdu',vmotherboard_id=vmotherboard_id).data.vpdu_pid.iloc[0]
            object='vpdu'
        except:
            pass

    output_label.config(text=object)

    # get institute_id
    try:
        institute_id = dbi.get('institute',name=selected_location).data.id.iloc[0]
    except:
        error_label.config(text="Please select an Institute")
        return

    # comment
    comment = comment_var.get()
    
    # Post the table
    table = {}
    table[object+'_id'] = vars()[object+'_id']
    table['institute_id'] = int(institute_id)
    table['timestamp'] = timestamp
    table['comment'] = comment
    table['state'] = selected_status

    print(table)
    post_successful = dbi.post_item(table,str(object)+'_location')
    if post_successful:
        status = 'succeeded'
        output_label.config(text=f'POST {status}: {object} {selected_qrcode}')
        # Print history of last statuses
        location_df = dbi.get(f"{object}_location",**{f"{object}_id": vars()[f"{object}_id"]}).data
        institute_df = dbi.get('institute').data
        history = pd.merge(location_df, institute_df, left_on='institute_id', right_on='id', how='left') # merge 2 dataframes to get the acronym for each location entry
        history.rename(columns={'acronym': 'location'}, inplace=True)
        print(history[['timestamp', 'location', 'state', 'comment']])
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, history[['timestamp', 'location', 'state', 'comment']].to_string(index=False))
    else:
        status = 'failed'
        error_label.config(text=f'POST {status}')
        
    print(f'POST {status}')

    submit_button.config(state="disabled")
    return 

    
if __name__ == "__main__":
    
    # Create the main window
    root = tk.Tk()
    root.title("Set Veto Location GUI")

    # Set the window size (width x height)
    window_width = 450
    window_height = 750
    root.geometry(f"{window_width}x{window_height}")
    
    # Create a label for error messages
    error_label = tk.Label(root, text="", fg="red")
    error_label.pack()

    # Create a label for output messages
    output_label = tk.Label(root, text="", fg="green")
    output_label.pack()
    
    # Create labels and text boxes for the QR code
    qrcode_label = tk.Label(root, text="QR code:")
    qrcode_label.pack()
    qrcode_var = tk.StringVar(root)
    qrcode_entry = tk.Entry(root, textvariable=qrcode_var)
    qrcode_entry.pack()

    # Create a Text widget
    text_box = scrolledtext.ScrolledText(root, height=10, width=55)
    text_box.pack(pady=10)
    
    # Status
    status_label = tk.Label(root, text="Status:")
    status_label.pack()

    options = ['', 'received', 'unbagged', 'test', 'bagged', 'shipped', 'production', 'storage', 'integration', 'scrapped']
    status_var = tk.StringVar(root)
    status_dropdown = ttk.Combobox(root, textvariable=status_var, values=options)
    status_dropdown.pack()
    
    # comment
    comment_label = tk.Label(root, text="Comment:")
    comment_label.pack()
    comment_var = tk.StringVar(root)
    comment_entry = tk.Entry(root, textvariable=comment_var)
    comment_entry.pack()
    
    # Location: institute
    location_label = tk.Label(root, text="Institute:")
    location_label.pack()

    df = dbi.get('institute').data
    locations = df.name.tolist()
    location_var = tk.StringVar(root)
    location_dropdown = ttk.Combobox(root, textvariable=location_var, values=locations)
    location_dropdown.pack()
    
    timestamp_label = tk.Label(root, text="Timestamp:")
    timestamp_label.pack()

    def open_calendar():
        def set_date():
            selected_date = calendar_widget.get_date()
            # Convert the selected date to a datetime object
            selected_date = datetime.datetime.strptime(selected_date, '%d/%m/%Y')
            selected_date_formatted = selected_date.strftime('%Y-%m-%d')  # Format the date
            timestamp_date_var.set(selected_date_formatted)
            top.destroy()
            
        top = tk.Toplevel(root)
        top.title("Select Date")
        
        calendar_widget = Calendar(top)
        calendar_widget.pack()
        
        set_button = tk.Button(top, text="Set Date", command=set_date)
        set_button.pack()

    timestamp_date_var = tk.StringVar(root)
    timestamp_date_var.set(datetime.datetime.now().strftime('%Y-%m-%d'))
    timestamp_date_entry = tk.Entry(root, textvariable=timestamp_date_var)
    timestamp_date_entry.pack()
    timestamp_date_button = tk.Button(root, text="Select Date", command=open_calendar)
    timestamp_date_button.pack()
        
    def open_time_selection():
        def set_time():
            selected_time = time_selection_var.get()
            if ':' in selected_time and selected_time.count(':') == 1:
                selected_time += ':00'
            timestamp_time_var.set(selected_time)
            top.destroy()

        top = tk.Toplevel(root)
        top.title("Select Time")

        time_selection_var = tk.StringVar(top)
        time_selection = ttk.Combobox(top, textvariable=time_selection_var, values=[f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in range(0, 60, 15)])
        time_selection.pack()
        
        set_button = tk.Button(top, text="Set Time", command=set_time)
        set_button.pack()
        
    timestamp_time_var = tk.StringVar(root)
    timestamp_time_var.set(datetime.datetime.now().strftime('%H:%M:%S'))
    timestamp_time_entry = tk.Entry(root, textvariable=timestamp_time_var)
    timestamp_time_entry.pack()
    timestamp_time_button = tk.Button(root, text="Select Time", command=open_time_selection)
    timestamp_time_button.pack()

       
    # Create the check button
    spacer_label = tk.Label(root, text="")
    spacer_label.pack()
    check_font = ("Helvetica", 14)  # Change the font size as needed
    check_button = tk.Button(root, text="Check", command=check_command, font=check_font)
    check_button.pack()

    # Create the submit button
    spacer_label = tk.Label(root, text="")
    spacer_label.pack()
    submit_font = ("Helvetica", 14)  # Change the font size as needed
    submit_button = tk.Button(root, text="Submit", command=submit_command, font=submit_font)
    submit_button.config(state="disabled")
    submit_button.pack()

    
    root.mainloop()
