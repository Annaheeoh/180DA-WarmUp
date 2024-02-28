# gui_rps_common.py
import tkinter as tk
import paho.mqtt.client as mqtt

def send_user_choice(choice, player):
    client.publish(f"rps/game/player{player}_choice", choice)

def rock():
    send_user_choice('rock', 1)

def paper():
    send_user_choice('paper', 1)

def scissor():
    send_user_choice('scissor', 1)

root = tk.Tk()
root.title("Rock Paper Scissors - Player 1")

button1 = tk.Button(root, text="Rock", command=rock)
button1.pack()
button2 = tk.Button(root, text="Paper", command=paper)
button2.pack()
button3 = tk.Button(root, text="Scissor", command=scissor)
button3.pack()

root.mainloop()
