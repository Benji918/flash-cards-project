from tkinter import *
from tkinter import messagebox
import pandas as pd
import random
from gtts import gTTS
import playsound
import os
from pathlib import Path

BACKGROUND_COLOR = "#B1DDC6"
# reading the French data file
try:
    data_file = pd.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pd.read_csv('data/french_words.csv')
    french_word = original_data.to_dict(orient='records')

else:
    french_word = data_file.to_dict(orient='records', )
    current_card = {}


def random_word():
    language = 'fr'
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(french_word)
    flash_card.itemconfig(flash_title, text='French', fill='black')
    flash_card.itemconfig(flash_text, text=current_card['French'], fill='black')
    audio_text = gTTS(text=current_card['French'], lang=language)
    audio_text.save('french_word.mp3')
    audio_file = r'C:\\Users\BENJAMIN\Downloads\flash-card-project-start\french_word.mp3'
    playsound.playsound(audio_file)
    os.remove('french_word.mp3')
    flash_card.itemconfig(flash_img, image=front_image)
    flip_timer = window.after(3000, func=flip_card)


def is_known():
    # remove word if the user already knows it
    try:
        french_word.remove(current_card)
    except ValueError:
        pass
    else:
        data = pd.DataFrame(french_word)
        data.to_csv('data/words_to_learn.csv', index=False)
        random_word()


# Flip the flash card after 3000ms
def flip_card():
    language = 'en'
    flash_card.itemconfig(flash_title, text='English', fill='white')
    try:
        flash_card.itemconfig(flash_text, text=current_card['English'], fill='white')
    except KeyError:
        messagebox.showinfo(title="Error", message='Please click on the X button first')
    else:
        flash_card.itemconfig(flash_img, image=back_img)
    # audio_text = gTTS(text=current_card['English'], lang=language)
    # audio_text.save('english_word.mp3')
    # playsound.playsound('english_word.mp3', True)
    # os.remove('english_word.mp3')


window = Tk()
window.title('Flash card app')
window.config(pady=50, padx=50, background=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

# Flash objects
front_image = PhotoImage(file='images/card_front.png')
back_img = PhotoImage(file='images/card_back.png')
flash_card = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
flash_img = flash_card.create_image(400, 263, image=front_image)
flash_title = flash_card.create_text(400, 150, text='Title', font=('Arial', 40, 'italic'))
flash_text = flash_card.create_text(400, 263, text='word', font=('Arial', 60, 'bold'))
flash_card.grid(column=0, row=0, columnspan=2)

# button
btn_img1 = PhotoImage(file='images/right.png')
btn_img2 = PhotoImage(file='images/wrong.png')
button = Button(image=btn_img1, highlightthickness=0, command=is_known)
button.grid(column=0, row=1)
button2 = Button(image=btn_img2, highlightthickness=0, command=random_word)
button2.grid(column=1, row=1)

window.mainloop()
