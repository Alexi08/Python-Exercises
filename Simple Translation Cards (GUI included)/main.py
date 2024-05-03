BACKGROUND_COLOR = "#B1DDC6"
import pandas
from tkinter import *
import random
import time
#-----------------------Random Word---------------------------#

random_english_word = ""
try:
    data = pandas.read_csv("./data/Words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("./data/french_words.csv")
except IndexError:
    data = pandas.read_csv("./data/french_words.csv")



words = data.to_dict(orient="records")
random_key = {}

def random_word():
    global random_key, timer
    root.after_cancel(timer)
    canvas.itemconfig(white_card, image=front_card)
    random_key = random.choice(words)
    canvas.itemconfig(title_word, text="French")
    canvas.itemconfig(word, text=random_key["French"])
    timer = root.after(3000, func=update)


def update():
    global random_key
    canvas.itemconfig(title_word, text="English")
    canvas.itemconfig(word, text=random_key["English"])
    canvas.itemconfig(white_card, image=back_card)


def is_known():
    words.remove(random_key)
    print(len(words))

    new_data = pandas.DataFrame(words)
    new_data.to_csv("data/Words_to_learn.csv", index=False)

    random_word()

#---------------------------UI-------------------------------#

root = Tk()
root.title("Translation cards")
root.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

timer = root.after(3000, func=update)

canvas = Canvas(width=800, height=526)
front_card = PhotoImage(file="./images/card_front.png")
back_card = PhotoImage(file="./images/card_back.png")
white_card = canvas.create_image(400, 263, image=front_card)

title_word = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="word", font=("Ariel", 60, "italic"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2, sticky=W+E)

right_img = PhotoImage(file="./images/right.png")
wrong_img = PhotoImage(file="./images/wrong.png")

right_button = Button(image=right_img, command=is_known)
right_button.config(highlightthickness=0, bg=BACKGROUND_COLOR)
right_button.grid(row=1, column=0)

wrong_button = Button(image=wrong_img, command=random_word)
wrong_button.config(highlightthickness=0, bg=BACKGROUND_COLOR)
wrong_button.grid(row=1, column=1)

random_word()


root.mainloop()
