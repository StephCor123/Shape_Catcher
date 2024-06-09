from itertools import cycle
from random import randrange, choice
from tkinter import Canvas, Tk, messagebox, font, Button, Label

canvas_width = 1000
canvas_height = 600

root = Tk()
root.title("Shape Catcher")

color_cycle = cycle(["blue", "green", "pink", "yellow", "cyan", "orange", "purple"])
shape_width = 45
shape_height = 55
shape_score = 1
shape_speed = 1 # Normal speed for shape to fall down
shape_interval = 700
difficulty = 1
catcher_color = "White"
catcher_width = 150  # Increase the catcher width
catcher_height = 20
catcher_startx = canvas_width / 2 - catcher_width / 2
catcher_starty = canvas_height - catcher_height - 5

c = Canvas(root, width=canvas_width, height=canvas_height, background="light blue")
c.create_rectangle(-5, canvas_height - 50, canvas_width + 3, canvas_height + 3, fill="purple", width=0)
c.pack()

# Home page setup
home_width = 500
home_height = 300

lives_remaining = 3  # Initialize lives_remaining here

def start_game():
    home_frame.destroy()
    c.pack()
    root.after(1000, create_shape)
    root.after(1000, move_shapes)
    root.after(1000, check_catch)

def increase_speed():
    global shape_speed, shape_interval
    increase_amount = 0.1
    if shape_speed + increase_amount <= 5:
        shape_speed += increase_amount
        shape_interval = 50  # constant delay for smooth animation
        speed_increase_label.config(text=f"Increase Speed: +{increase_amount} (New Speed: {shape_speed:.2f})")
        print(f"Shape speed increased by {increase_amount}! New speed: {shape_speed:.2f}")
    else:
        messagebox.showinfo("Max Speed Reached", "You've reached the maximum speed.")

def decrease_speed():
    global shape_speed, shape_interval
    decrease_amount = 0.02
    if shape_speed - decrease_amount >= 0.1:
        shape_speed -= decrease_amount
        shape_interval = 50  # constant delay for smooth animation
        speed_increase_label.config(text=f"Decrease Speed: -{decrease_amount} (New Speed: {shape_speed:.2f})")
        print(f"Shape speed decreased by {decrease_amount}! New speed: {shape_speed:.2f}")
    else:
        messagebox.showinfo("Min Speed Reached", "You've reached the minimum speed.")

def create_home_frame():
    global home_frame, start_button, speed_increase_button, speed_decrease_button, speed_increase_label
    home_frame = Canvas(root, width=home_width, height=home_height, background="white")
    home_frame.place(relx=0.5, rely=0.5, anchor="center")

    game_font = font.nametofont("TkFixedFont")
    game_font.config(size=14, weight="bold")  # Make the font bold

    start_button = Button(home_frame, text="Start Game", command=start_game, bg="black", fg="white",
                          font=game_font, borderwidth=1)
    start_button.place(relx=0.5, rely=0.3, anchor="center")

    speed_increase_button = Button(home_frame, text="Increase Speed", command=increase_speed, bg="black", fg="white",
                                   font=game_font, borderwidth=1)
    speed_increase_button.place(relx=0.5, rely=0.5, anchor="center")
    speed_increase_button.bind("<Enter>", lambda event: speed_increase_button.config(text="Increase Speed\n(+0.1)"))
    speed_increase_button.bind("<Leave>", lambda event: speed_increase_button.config(text="Increase Speed"))

    speed_decrease_button = Button(home_frame, text="Decrease Speed", command=decrease_speed, bg="black", fg="white",
                                   font=game_font, borderwidth=1)
    speed_decrease_button.place(relx=0.5, rely=0.7, anchor="center")
    speed_decrease_button.bind("<Enter>", lambda event: speed_decrease_button.config(text="Decrease Speed\n(-0.02)"))
    speed_decrease_button.bind("<Leave>", lambda event: speed_decrease_button.config(text="Decrease Speed"))

    global speed_increase_label  # Declare global to avoid UnboundLocalError
    speed_increase_label = Label(home_frame, text="", font=game_font, bg="white")
    speed_increase_label.place(relx=0.5, rely=0.9, anchor="center")

create_home_frame()

game_font = font.nametofont("TkFixedFont")
game_font.config(size=18, weight="bold")  # Make the font bold

score = 0
score_text = c.create_text(10, 10, anchor="nw", font=game_font, fill="darkblue", text="Score: " + str(score))

# Move the lives text to the bottom right
lives_text = c.create_text(canvas_width - 10, canvas_height - 10, anchor="se", font=game_font, fill="darkblue",
                            text="Lives: " + str(lives_remaining))

shapes = []
new_shape = None  # Initialize new_shape before the create_shape function

def create_shape():
    global new_shape  # Declare new_shape as global
    x = randrange(10, canvas_width - shape_width)
    y = -shape_height  # Start from the top of the canvas

    shape_type = choice(["rectangle", "triangle", "circle", "pentagon", "hexagon"])

    if shape_type == "rectangle":
        new_shape = c.create_rectangle(x, y, x + shape_width, y + shape_height, fill=next(color_cycle), width=0)
    elif shape_type == "triangle":
        new_shape = c.create_polygon(x, y + shape_height, x + shape_width / 2, y, x + shape_width, y + shape_height,
                                     fill=next(color_cycle), outline="")
    elif shape_type == "circle":
        new_shape = c.create_oval(x, y, x + shape_width, y + shape_height, fill=next(color_cycle), outline="")

    shapes.append(new_shape)
    root.after(shape_interval, create_shape)

def move_shapes():
    global shapes
    updated_shapes = []

    for shape in shapes:
        if shape is not None:
            coords = c.coords(shape)
            if not coords or len(coords) != 4:
                print(f"Invalid number of coordinates for shape {shape}: {coords}")
                continue

            (_, shapey, _, shapey2) = coords
            c.move(shape, 0, shape_speed * 10)  # Adjust shape speed

            if shapey2 > canvas_height:
                shape_dropped(shape)
            else:
                updated_shapes.append(shape)

    shapes = updated_shapes  # Update the shapes list

    root.after(100, move_shapes)  # Adjust interval


def shape_dropped(shape):
    shapes.remove(shape)
    c.delete(shape)
    lose_a_life()
    if lives_remaining == 0:
        messagebox.showinfo("Game Over!", "Final Score: " + str(score))
        root.destroy()

def lose_a_life():
    global lives_remaining
    lives_remaining -= 1
    c.itemconfigure(lives_text, text="Lives: " + str(lives_remaining))

def check_catch():
    catcher_coords = c.coords(catcher)
    (catcherx, _, catcherx2, catchery2) = catcher_coords
    
    for shape in shapes:
        if shape is not None:  # Check if shape is not None
            coords = c.coords(shape)
            if len(coords) != 4:
                print(f"Invalid number of coordinates for shape {shape}: {coords}")
                continue

            (shapex, shapey, shapex2, shapey2) = coords
            if catcherx < shapex and shapex2 < catcherx2 and catchery2 - shapey2 < 40:
                shapes.remove(shape)
                c.delete(shape)
                increase_score(shape_score)

    root.after(100, check_catch)

def increase_score(points):
    global score, shape_speed, shape_interval
    score += points
    shape_speed = max(shape_speed * difficulty, 0.1)  # Adjusted min speed
    shape_interval = int(shape_interval * (1 / shape_speed))  # Adjusted interval based on speed
    c.itemconfigure(score_text, text="Score: " + str(score))

def move_left(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x1 > 0:
        c.move(catcher, -80, 0)  # Increase the movement distance

def move_right(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher, 80, 0)  # Increase the movement distance

c.bind("<Left>", move_left)
c.bind("<Right>", move_right)
c.focus_set()

# Create a 2D flat surface catcher using a rectangle
catcher = c.create_rectangle(catcher_startx, catcher_starty, catcher_startx + catcher_width,
                             catcher_starty + catcher_height, fill=catcher_color, outline=catcher_color)

root.mainloop()
