import tkinter as tk
import random
import paho.mqtt.client as mqtt

window = tk.Tk()
window.geometry("800x300")
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

def send_user_choice(choice, player):
    client.publish(f"rps/game/player{player}_choice", choice)

def on_message(client, userdata, message):
    global USER_CHOICE, COMP_CHOICE, USER_SCORE, COMP_SCORE

    if message.topic == "rps/game/player2_choice":
        comp_choice = message.payload.decode()
        COMP_CHOICE = choice_to_number(comp_choice)
    elif message.topic == "rps/game/result":
        result_data = message.payload.decode().split(",")
        USER_SCORE, COMP_SCORE = map(int, result_data)
    
    USER_CHOICE = choice_to_number(USER_CHOICE)

    if USER_CHOICE == COMP_CHOICE:
        print("Tie")
    elif (USER_CHOICE - COMP_CHOICE) % 3 == 1:
        print("You win")
        USER_SCORE += 1
    else:
        print("Comp wins")
        COMP_SCORE += 1

    update_display()

def update_display():
    text_area.delete(1.0, tk.END)
    text_area2.delete(1.0, tk.END)
    answer = "Your Choice: {uc} \nComputer's Choice : {cc} \nYour Score : {u} \nComputer Score : {c} ".format(
        uc=number_to_choice(USER_CHOICE), cc=number_to_choice(COMP_CHOICE), u=USER_SCORE, c=COMP_SCORE)
    text_area.insert(tk.END, answer)

# MQTT Callbacks
client.on_message = on_message
client.subscribe("rps/game/player2_choice")
client.subscribe("rps/game/result")

# GUI Buttons for Player 1
button1 = tk.Button(text="Rock", bg="skyblue", command=lambda: send_user_choice('rock', 1))
button1.grid(column=0, row=1)
button2 = tk.Button(text="Paper", bg="pink", command=lambda: send_user_choice('paper', 1))
button2.grid(column=0, row=2)
button3 = tk.Button(text="Scissor", bg="lightgreen", command=lambda: send_user_choice('scissor', 1))
button3.grid(column=0, row=3)

# Text Area for Player 1
text_area = tk.Text(master=window, height=12, width=30, bg="#FFFF99")
text_area.grid(column=0, row=4)

# GUI Buttons for Player 2
button1_p2 = tk.Button(text="Rock", bg="skyblue", command=lambda: send_user_choice('rock', 2))
button1_p2.grid(column=1, row=1)
button2_p2 = tk.Button(text="Paper", bg="pink", command=lambda: send_user_choice('paper', 2))
button2_p2.grid(column=1, row=2)
button3_p2 = tk.Button(text="Scissor", bg="lightgreen", command=lambda: send_user_choice('scissor', 2))
button3_p2.grid(column=1, row=3)

# Text Area for Player 2
text_area2 = tk.Text(master=window, height=12, width=30, bg="#FFFF99")
text_area2.grid(column=1, row=4)

window.mainloop()
