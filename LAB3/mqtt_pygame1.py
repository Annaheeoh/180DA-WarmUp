import tkinter as tk
import random
import paho.mqtt.client as mqtt

window = tk.Tk()
window.geometry("400x300")
window.title("Rock Paper Scissors")

USER_SCORE = 0
COMP_SCORE = 0
USER_CHOICE = ""
COMP_CHOICE = ""

# MQTT Setup
broker_address = "mqtt.eclipseprojects.io"
client = mqtt.Client()
client.connect(broker_address, 1883, 60)
client.loop_start()

def choice_to_number(choice):
    rps = {'rock': 0, 'paper': 1, 'scissor': 2}
    return rps[choice]

def number_to_choice(number):
    rps = {0: 'rock', 1: 'paper', 2: 'scissor'}
    return rps[number]

def random_computer_choice():
    return random.choice(['rock', 'paper', 'scissor'])

def send_user_choice(choice):
    client.publish("rps/game/user_choice", choice)

def on_message(client, userdata, message):
    global USER_CHOICE, COMP_CHOICE, USER_SCORE, COMP_SCORE

    comp_choice = message.payload.decode()
    USER_CHOICE = choice_to_number(USER_CHOICE)
    comp_choice = choice_to_number(comp_choice)

    if USER_CHOICE == comp_choice:
        print("Tie")
    elif (USER_CHOICE - comp_choice) % 3 == 1:
        print("You win")
        USER_SCORE += 1
    else:
        print("Comp wins")
        COMP_SCORE += 1

    update_display()

def update_display():
    text_area.delete(1.0, tk.END)
    answer = "Your Choice: {uc} \nComputer's Choice : {cc} \nYour Score : {u} \nComputer Score : {c} ".format(
        uc=USER_CHOICE, cc=COMP_CHOICE, u=USER_SCORE, c=COMP_SCORE)
    text_area.insert(tk.END, answer)

def rock():
    global USER_CHOICE
    USER_CHOICE = 'rock'
    send_user_choice(USER_CHOICE)

def paper():
    global USER_CHOICE
    USER_CHOICE = 'paper'
    send_user_choice(USER_CHOICE)

def scissor():
    global USER_CHOICE
    USER_CHOICE = 'scissor'
    send_user_choice(USER_CHOICE)

# MQTT Callbacks
client.on_message = on_message
client.subscribe("rps/game/comp_choice")

# GUI Buttons
button1 = tk.Button(text="Rock", bg="skyblue", command=rock)
button1.grid(column=0, row=1)
button2 = tk.Button(text="Paper", bg="pink", command=paper)
button2.grid(column=0, row=2)
button3 = tk.Button(text="Scissor", bg="lightgreen", command=scissor)
button3.grid(column=0, row=3)

# Text Area
text_area = tk.Text(master=window, height=12, width=30, bg="#FFFF99")
text_area.grid(column=0, row=4)

window.mainloop()
