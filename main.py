import pandas
from tkinter import *
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
word_dict = {}


def random_word():
    global word_dict
    french_val = choice(french_words)
    index_val = french_words.index(french_val)
    eng_word = eng_translation[index_val]
    word_dict = {"French": french_val, "English": eng_word}
    return french_val


def new_word():
    global screen_flip
    screen.after_cancel(screen_flip)
    word = random_word()
    front_card.itemconfig(card_img, image=card_front_img)
    front_card.itemconfig(rand_word, text=word, fill="black")
    front_card.itemconfig(lang, text="French", fill="black")
    screen_flip = screen.after(3000, flip_card)


def flip_card():
    eng_word = word_dict["English"]
    front_card.itemconfig(card_img, image=card_back_img)
    front_card.itemconfig(rand_word, text=eng_word, fill="white")
    front_card.itemconfig(lang, text="English", fill="white")


def known_word():
    global french_words, eng_translation
    text = front_card.itemcget(rand_word, 'text')
    try:
        index = french_words.index(text)
    except ValueError:
        index = eng_translation.index(text)
    french_words.pop(index)
    eng_translation.pop(index)
    updated_dict = {"French": french_words, "English": eng_translation}
    with open("words_to_learn.csv", "w") as file_1:
        df = pandas.DataFrame(updated_dict)
        df.to_csv(file_1, index=False)
    new_word()


try:
    with open("words_to_learn.csv") as file:
        csv_data = pandas.read_csv(file)
        french_words = csv_data["French"].tolist()
        eng_translation = csv_data["English"].tolist()
except FileNotFoundError:
    with open("french_words.csv") as file:
        csv_data = pandas.read_csv(file)
        french_words = csv_data["French"].tolist()
        eng_translation = csv_data["English"].tolist()


screen = Tk()
screen.title("Flash Card App")
screen.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

screen_flip = screen.after(3000, flip_card)

#Front Flash Card
card_front_img = PhotoImage(file="card_front.png")
card_back_img = PhotoImage(file="card_back.png")
front_card = Canvas(bg=BACKGROUND_COLOR, width=800, height=530, highlightthickness=0)
card_img = front_card.create_image(400, 265, image=card_front_img)
lang = front_card.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
rand_word = front_card.create_text(400, 300, text=random_word(), font=("Ariel", 60, "bold"))
front_card.grid(row=0, column=0, columnspan=2)

#RightButton
right_pic = PhotoImage(file="right.png")
right_button = Button(image=right_pic, bg=BACKGROUND_COLOR, fg=BACKGROUND_COLOR, highlightthickness=0, command=known_word)
right_button.grid(row=1, column=0)

#WrongButton
wrong_pic = PhotoImage(file="wrong.png")
wrong_button = Button(image=wrong_pic, bg=BACKGROUND_COLOR, fg=BACKGROUND_COLOR, highlightthickness=0, command=new_word)
wrong_button.grid(row=1, column=1)


screen.mainloop()
