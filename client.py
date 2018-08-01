#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 25 14:54:24 2018

@author: jessicasaini
"""
from tkinter import*
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import filedialog

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(END, msg)
        except OSError:  # Possibly client has left the chat.
            break

def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        root.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

def browsefunc():
    filename = filedialog.askopenfilename()
    pathlabel.config(text=filename)
    
    

# Following will contain the messages.


root=Tk()
root.title("Amazon Efficient File Sharing Application")
root.configure(background='plum4')
messages_frame = Frame(root)
my_msg = StringVar()  # For the messages to be sent.
my_msg.set("Enter your message here")
scrollbar = Scrollbar(messages_frame)  # To navigate through past messages.

# Following will contain the messages.
msg_list = Listbox(messages_frame,height=15, width=50,  yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH,expand=TRUE)

msg_list.configure(background='lavender')
messages_frame.pack(fill=BOTH, expand=True)

entry_field = Entry(root, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack(fill=BOTH,expand=TRUE)
bottom = Frame(root)
bottom.pack(side=BOTTOM, fill=BOTH, expand=True)
bottom.config(borderwidth=2,bg='lavender')
receive_button = Button(root, text="Receive File",bg="lavender")
receive_button.pack(in_=bottom,side=RIGHT,fill=BOTH,expand=True)
send_button = Button(root, text="Send",bg="lavender",command=send)
send_button.pack(in_=bottom,side=LEFT,fill=BOTH, expand=True)
browse_button = Button(root, text="Send Photo",bg="lavender",command=browsefunc)
browse_button.pack(in_=bottom,side=RIGHT,fill=BOTH,expand=True)
pathlabel = Label(root)
pathlabel.pack()
root.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

root.mainloop()