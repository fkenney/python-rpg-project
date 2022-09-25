
#!/usr/bin/python3
from tkinter import *
from PIL import Image, ImageTk

"""Felicia Kenney - Project 2 - RPG Game"""


# This renders the window
screen = Tk()
screen.title('The Chocolate Factory')
# ------------------- IMAGES ------------------------------------------
# images of map
chocolate_fac = ImageTk.PhotoImage(Image.open("chocolate.png"))
candytopia = ImageTk.PhotoImage(Image.open("candytopia.png"))
hidden_room_1 = ImageTk.PhotoImage(Image.open("hidden_room1.png"))
hidden_room_2 = ImageTk.PhotoImage(Image.open("hidden_room2.png"))
sweet_shop = ImageTk.PhotoImage(Image.open("sweetshop.png"))
gummy_castle = ImageTk.PhotoImage(Image.open("gummy_castle.png"))
sweet_tooth = ImageTk.PhotoImage(Image.open("monster.png"))
sweet_toothv2 = ImageTk.PhotoImage(Image.open("monster-defeated.png"))
treasure = ImageTk.PhotoImage(Image.open("treasure.png"))

# monster health images
health100 = ImageTk.PhotoImage(Image.open("monster-h100.png"))
health75 = ImageTk.PhotoImage(Image.open("monster-h75.png"))
health50 = ImageTk.PhotoImage(Image.open("monster-h50.png"))
health25 = ImageTk.PhotoImage(Image.open("monster-h25.png"))
health0 = ImageTk.PhotoImage(Image.open("monster-h0.png"))
youlose = ImageTk.PhotoImage(Image.open("gameover.png"))
youwin = ImageTk.PhotoImage(Image.open("winner.gif"))

# health
health = 100
monsterHealth = 100

# messages displayed to user
message = 'Welcome to the Chocolate Factory, select a direction to begin'

# inventory items
inventory = []

# current room
currentRoom = 'Chocolate Factory'

fighting = False
gameOver = False

# -------------------- ROOMS --------------------------------------
rooms = {
    'Chocolate Factory': {
        'south': 'Candytopia',
        'image': chocolate_fac
    },
    'Candytopia': {
        'north': 'Chocolate Factory',
        'east': 'Sweet Shop',
        'south': 'Hidden Room 1',
        'image': candytopia
    },
    'Sweet Shop': {
        'north': 'Sweet Tooth Room',
        'east': 'Hidden Room 2',
        'south': 'Gummy Castle',
        'west': 'Candytopia',
        'image': sweet_shop
    },
    'Sweet Tooth Room': {
        'south': 'Sweet Shop',
        'monster':  'monster',
        'item': 'key',
        'image': sweet_tooth
    },
    'Gummy Castle': {
        'north': 'Sweet Shop',
        'east': 'Treasure Room',
        'image': gummy_castle
    },
    'Hidden Room 1': {
        'north': 'Candytopia',
        'item': 'Toothbrush Sword',
        'image': hidden_room_1

    },
    'Hidden Room 2': {
        'west': 'Sweet Shop',
        'item': 'Potion',
        'image': hidden_room_2
    },
    'Treasure Room': {
        'west': 'Gummy Castle',
        'image': treasure
    }
}
# ------------------ MOVES ------------------------------------

# updates the current room


def move(direction):
    global currentRoom
    global message

    if direction in rooms[currentRoom]:
        # updates current room
        currentRoom = rooms[currentRoom][direction]

        # if there is an item in the room it displays a message
        if 'item' in rooms[currentRoom] and not 'monster' in rooms[currentRoom]:
            setUpRiddle()
            # HIDDEN ROOM 1
            if currentRoom == 'Hidden Room 1':
                message = f"You see locked chest made of chocolate, with a secret riddle:\n ' What kind of beans don't grow in a garden? '"
            # HIDDEN ROOM 2
            elif currentRoom == 'Hidden Room 2':
                message = f"You stumbled across a hidden nurses office that has a locked medicine cabinet. \nTry to answer the riddle: \n ' What chocolate candy has two female pronouns? '"
        elif currentRoom == 'Sweet Tooth Room':
            if 'monster' in rooms[currentRoom]:
                button_fight.grid(row=6, column=0)
                message = "Ahhhh...You ran into the Sweet Tooth Monster that has the key to escape. Press fight to begin"
            else:
                button_fight.grid_forget()
                message = "Hahaha, I defeated him"
        elif currentRoom == 'Treasure Room' and 'key' not in inventory:
            message = "Looks like there is an exit, but I need a key..."
        elif currentRoom == 'Treasure Room' and 'key' in inventory:
            message = "YOU ESCAPED !!!"
            toggleButtons()
        else:
            message = "Hmmm....another room "
            button_fight.grid_forget()
            input.grid_forget()
            button_submit.grid_forget()
    # no room in that direction
    else:
        message = "You can\'t go that way!"

    # updates the view with information
    updateView()

# ------------------UPDATE VIEW ------------------------------------
# updates the current view displayed


def updateView():
    global currentRoom
    global currentRoomImage
    global currentInventory
    global currentStatus
    global currentMessage
    global inventory
    global message
    global health
    global monsterHealth
    global fighting
    global gameOver

    # selets new image
    image = rooms[currentRoom]['image']

    # updates image on map
    currentRoomImage.grid_forget()

    if fighting == True and gameOver == False:
        if monsterHealth == 100:
            currentRoomImage = Label(image=health100)
        elif monsterHealth == 75:
            currentRoomImage = Label(image=health75)
        elif monsterHealth == 50:
            currentRoomImage = Label(image=health50)
        elif monsterHealth == 25:
            currentRoomImage = Label(image=health25)
        else:
            currentRoomImage = Label(image=health0)
            inventory.append(rooms[currentRoom]['item'])
            # updates map of the room
            rooms['Sweet Tooth Room'].update({'image': sweet_toothv2})

            # updates map of treasure room
            rooms['Treasure Room'].update({'image': youwin})

            # appends end fight button
            button_end_fight.grid(row=6, column=0)

            # removes hit button
            button_hit.grid_forget()

            # deletes item from room
            del rooms[currentRoom]['item']

            # deletes monster from room
            del rooms[currentRoom]['monster']
            fighting = False

    elif gameOver == True:
        currentRoomImage = Label(image=youlose)
    else:
        currentRoomImage = Label(image=image)

    currentRoomImage.grid(row=0, column=0, columnspan=8)

    # updates current status
    currentStatus.grid_forget()
    currentStatus = Label(text=f'{currentRoom}',  font='Helvetica 10 bold')
    currentStatus.grid(row=1, column=0, columnspan=3, sticky="nw")

    # updates inventory
    currentInventory.grid_forget()
    currentInventory = Label(
        text=f'Inventory: {inventory}', font='Helvetica 10 bold')
    currentInventory.grid(row=1, column=3, columnspan=3, sticky="nw")

    # updates message
    currentMessage.grid_forget()
    currentMessage = Label(
        text=f'Message: {message}', font='Helvetica 10 bold', bg='white')
    currentMessage.grid(row=3, column=0, columnspan=6,
                        pady=(10, 20), sticky="nw")

# --------------------- RIDDLE -------------------------------------------------------------
# generates text box and button for riddles


def setUpRiddle():
    # input for riddle
    input.grid(row=4, column=0, columnspan=6, pady=(5, 10))
    # submit button for riddle
    button_submit.grid(row=4, column=4)


def answerRiddle(answer):
    global currentRoom
    global message
    global inventory
    global input
    global button_submit

    answer = answer.lower().strip()

    if currentRoom == 'Hidden Room 1':
        if answer == 'jelly beans':
            message = f"The chest unlocks and you see a {rooms[currentRoom]['item']}, this could be useful"
            # adds item to inventory
            inventory.append(rooms[currentRoom]['item'])

            # deletes item from room
            del rooms[currentRoom]['item']

            # removes button and input box
            button_submit.grid_forget()
            input.delete(0, END)
            input.grid_forget()

        else:
            message = f"Wrong Answer, Try Again: 'What kind of beans don't grow in a garden?'"
        updateView()
    elif currentRoom == 'Hidden Room 2':
        if answer == 'hershey':
            message = f"You found Healing {rooms[currentRoom]['item']} in the cabinet, this could be useful"
            # adds item to inventory
            inventory.append(rooms[currentRoom]['item'])

            # deletes item from room
            del rooms[currentRoom]['item']

            # removes button and input box
            button_submit.grid_forget()
            input.delete(0, END)
            input.grid_forget()
        else:
            message = f"Wrong Answer, Try Again: ' What candy has two female pronouns? '"
        updateView()

# ------------------------ FIGHT -----------------------------------------

# sets up screen to fight


def fight():
    global fighting
    global message
    global button_hit
    global button_fight
    global inventory

    # updates status to fighing
    fighting = True
    # shows health
    message = f"Your Health: ({health})  --------- Monster's Health: ({monsterHealth})"

    # adds button to use potion
    if 'Potion' in inventory:
        button_potion.grid(row=7, column=0)

    # deletes start fight button
    button_fight.grid_forget()
    button_hit.grid(row=6, column=0)
    toggleButtons()
    updateView()


def end_fight():
    global message

    toggleButtons()
    message = "Finally, I got the key!"
    button_end_fight.grid_forget()
    button_potion.grid_forget()
    updateView()


def hit():
    global health
    global monsterHealth
    global inventory
    global gameOver
    global message

    if 'Toothbrush Sword' in inventory:
        monsterHealth -= 75
        health -= 25
    else:
        monsterHealth -= 25
        health -= 50

    if health < 100:
        warning = "Health Getting Low!"
    else:
        warning = ""
    message = f"{warning} Your Health: ({health})  --------- Monster's Health: ({monsterHealth})"

    if health <= 0:
        gameOver = True
        button_hit.grid_forget()
    updateView()


def potion():
    global health
    global message
    # adjust health
    health = 200
    inventory.remove('Potion')
    button_potion.grid_forget()
    message = f"You used Potion! Your Health: ({health})  --------- Monster's Health: ({monsterHealth})"
    updateView()


def toggleButtons():
    if button_north["state"] == "normal":
        button_north["state"] = "disabled"
        button_south["state"] = "disabled"
        button_east["state"] = "disabled"
        button_west["state"] = "disabled"
    else:
        button_north["state"] = "normal"
        button_south["state"] = "normal"
        button_east["state"] = "normal"
        button_west["state"] = "normal"


# ------------- VIEW LABELS/ IMAGES --------------------------------------
# current Image displayed
currentRoomImage = Label(image=chocolate_fac)
currentRoomImage.grid(row=0, column=0, columnspan=6)

# current status
currentStatus = Label(text=f'{currentRoom}',  font='Helvetica 10 bold')
currentStatus.grid(row=1, column=0, columnspan=3, sticky="nw")

# current inventory
currentInventory = Label(
    text=f'Inventory: {inventory}', font='Helvetica 10 bold')
currentInventory.grid(row=1, column=3, columnspan=3, sticky="nw")

# current message

currentMessage = Label(
    text=f'Message: {message}', font='Helvetica 10 bold', bg='white')

currentMessage.grid(row=3, column=0, columnspan=6,
                    pady=(10, 20),  sticky="nw")

# input box
input = Entry(screen, width=20)

# -------------------- BUTTONS --------------------------------------
# exit button
button_quit = Button(screen, text="Quit Game", bg='red',
                     fg='white', command=screen.quit)
button_quit.grid(row=10, column=5)

# north
button_north = Button(screen, text="North", bg='blue',
                      fg='white', command=lambda: move('north'))
button_north.grid(row=6, column=3)

# south button
button_south = Button(screen, text="South",  bg='blue',
                      fg='white', command=lambda: move('south'))
button_south.grid(row=8, column=3)

# west button
button_west = Button(screen, text="West",  bg='blue',
                     fg='white', command=lambda: move('west'))
button_west.grid(row=7, column=2)

# east button
button_east = Button(screen, text="East",  bg='blue',
                     fg='white', command=lambda: move('east'))
button_east.grid(row=7, column=4)

# submit button for input
button_submit = Button(screen, text="Submit",
                       command=lambda: answerRiddle(input.get()))

# fight button
button_fight = Button(screen, text="Start Fight", bg='black',
                      fg='white', width=10, command=lambda: fight())
# fight button
button_end_fight = Button(screen, text="Exit Fight", bg='black',
                          fg='white', width=10, command=lambda: end_fight())
# hit button
button_hit = Button(screen, text="Hit", bg='black',
                    fg='white', width=10, command=lambda: hit())
# Potion button
button_potion = Button(screen, text="Use Potion", bg='green',
                       fg='white', width=10, command=lambda: potion())

# opens window
screen.mainloop()
