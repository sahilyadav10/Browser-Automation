import os
import sys
import threading
import tkinter as tk
import tkinter.font
from threading import Thread
from time import sleep
from project_backend import session, close

# make a directory if it is not present
if not (os.path.isdir("./BrowserAutomation")):
    os.mkdir("./BrowserAutomation")

contact = ""
message = ""
scheduleTimeValue = ""

window = tk.Tk()
window.title("Browser Automation")
window.geometry('450x500')
window.resizable(False, False)
window.config(bg="#D8D8D8")

fontStyle = tk.font.Font(size=17)
contactName = tk.StringVar()
messageText = tk.StringVar()
timeValue = tk.StringVar()

name_label = tk.Label(window, text="Contact Name", fg="#FF5E5B", bg="#D8D8D8", font=fontStyle)
name_entry = tk.Entry(window, textvariable=contactName, width=60)
name_entry.insert(0, 'Enter the same name as saved on your device')
name_entry.bind("<FocusIn>", lambda args: name_entry.delete('0', 'end'))

message_label = tk.Label(window, text="Message", fg="#FF5E5B", bg="#D8D8D8", font=fontStyle)
message_text = tk.Text(width=45, height=10)
message_text.insert(1.0, 'Enter a message you want to send')
message_text.bind("<FocusIn>", lambda args: message_text.delete(1.0, 'end'))

time_label = tk.Label(window, text="Time", fg="#FF5E5B", bg="#D8D8D8", font=fontStyle)
time_entry = tk.Entry(window, textvariable=timeValue, width=60)
time_entry.insert(0, 'Repeat everyday at HH:MM (24 hour format). Example- 22:22')
time_entry.bind("<FocusIn>", lambda args: time_entry.delete('0', 'end'))

# placements
name_label.place(x=30, y=50)
name_entry.place(x=40, y=80)
message_label.place(x=30, y=110)
message_text.place(x=40, y=140)
time_label.place(x=30, y=320)
time_entry.place(x=40, y=350)

# checks if the time entered is valid or not
def isvalidtime():
    if (scheduleTimeValue[0] == '3' or scheduleTimeValue[0] == '4' or scheduleTimeValue[0] == '5'
            or scheduleTimeValue[0] == '6' or scheduleTimeValue[0] == '7'
            or scheduleTimeValue[0] == '8' or scheduleTimeValue[0] == '9'):
        return 0
    if (scheduleTimeValue[0] == '2' and (scheduleTimeValue[1] == '5' or scheduleTimeValue[0] == '6'
                                         or scheduleTimeValue[0] == '7' or scheduleTimeValue[0] == '8' or scheduleTimeValue[0] == '9')):
        return 0
    if scheduleTimeValue[2] != ':':
        return 0
    if scheduleTimeValue[3] == '7' or scheduleTimeValue[3] == '8' or scheduleTimeValue[3] == '9' \
            or (scheduleTimeValue[3] == '6' and scheduleTimeValue[4] != '0'):
        return 0
    return 1


def submit():
    # removes focus from input widgets
    window.focus()

    global contact
    global message
    global scheduleTimeValue
    contact = contactName.get()
    message = message_text.get("1.0", "end-1c")
    scheduleTimeValue = timeValue.get()

    """ shows error is the fields are empty or incorrect """
    if len(contact) == 0 or contact.isspace() or contact == 'Enter the same name as saved on your device':
        name_entry.delete('0', 'end')
        name_entry.insert('0', 'Enter the same name as saved on your device')
        name_entry.config(highlightthickness=2, highlightbackground="red", highlightcolor="red")
        name_entry.bind("<FocusIn>", lambda args: name_entry.delete('0', 'end'))
    else:
        name_entry.config(highlightthickness=0)

    if len(message_text.get("1.0", 'end-1c')) == 0 or message_text.get("1.0", "end-1c").isspace() or message_text.get("1.0", "end-1c") == 'Enter the message you want to send':
        message_text.delete(1.0, 'end')
        message_text.insert(1.0, 'Enter the message you want to send')
        message_text.config(highlightthickness=2, highlightbackground="red", highlightcolor="red")
        message_text.bind("<FocusIn>", lambda args: message_text.delete(1.0, 'end'))
    else:
        message_text.config(highlightthickness=0)

    if len(scheduleTimeValue) == 0 or len(scheduleTimeValue) != 5 or scheduleTimeValue.isspace() or scheduleTimeValue == 'Repeat everyday at HH:MM (24 hour format). Example- 22:22':
        time_entry.delete('0', 'end')
        time_entry.insert('0', 'Repeat everyday at HH:MM (24 hour format). Example- 22:22')
        time_entry.config(highlightthickness=2, highlightbackground="red", highlightcolor="red")
    else:
        time_entry.config(highlightthickness=0)
        if not isvalidtime():
            time_entry.delete('0', 'end')
            time_entry.insert('0', 'Repeat everyday at HH:MM (24 hour format). Example- 22:22')
            time_entry.config(highlightthickness=2, highlightbackground="red", highlightcolor="red")

    # browser is opened if all the fields are correct
    if (len(contactName.get()) != 0 and contactName.get() != 'Enter the same name as saved on your device') and (len(message_text.get("1.0", "end-1c")) != 0 and message_text.get("1.0", "end-1c") != 'Enter the message you want to send') and len(timeValue.get()) != 0 and timeValue.get() != 'Repeat everyday at HH:MM (24 hour format). Example- 22:22':
        if submitButton['state'] == tk.NORMAL:
            submitButton['state'] = tk.DISABLED
            popup = tk.Message(window, text="Only one reminder can be set at a time. \nCancel to set another", bg="#FF5E5B", width="450",
                               font=tk.font.Font(size=18))
            popup.pack()

        threading.Thread(target=session, args=(contact, message, scheduleTimeValue, popup)).start()


def restart_program():
    if submitButton['state'] == tk.DISABLED:
        close()
    python = sys.executable
    os.execl(python, python, * sys.argv)


submitButton = tk.Button(window, width='30', text='Set Reminder!', bg="#FF5E5B", state=tk.NORMAL, command=submit)
submitButton.place(x=115, y=400)
cancelButton = tk.Button(window, width='30', text='Cancel', bg="#FF5E5B", command=restart_program)
cancelButton.place(x=115, y=430)
window.mainloop()
