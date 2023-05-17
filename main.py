import openai
import speech_recognition as sr
import pyttsx3
import tkinter as tk
import threading
from audio import Input
from keys import api_key

# from keys import API_KEY
from audio import Input

openai.api_key = api_key

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

prompt = ""
user_name = 'User'
bot_name = 'Assistant'
convo = ""

BG_GRAY = "#ABB289"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


def text():
    global convo
    user_input = input_text.get("1.0", tk.END).strip()  # 5 sec
    convo += user_name + ":" + " " + user_input + "\n" + bot_name + ":"
    input_text.delete("1.0", tk.END)

    # openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=convo,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    response_str = response['choices'][0]['text'].replace("\n", "")
    response_str = response_str.split(
        user_name + ":", 1)[0].split(bot_name + ":", 1)[0]

    convo += response_str + "\n"
    conservation_text.delete("1.0", tk.END)
    conservation_text.insert(tk.END, convo)

    engine.say(response_str)
    engine.runAndWait()


def audio_input():
    global convo
    user_input = Input()  # 5 sec
    convo += user_name + ":" + user_input + "\n" + bot_name + ":"

    # openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=convo,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    response_str = response['choices'][0]['text'].replace("\n", "")
    response_str = response_str.split(
        user_name + ":", 1)[0].split(bot_name + ":", 1)[0]

    convo += response_str + "\n"
    conservation_text.delete("1.0", tk.END)
    conservation_text.insert(tk.END, convo)

    engine.say(response_str)
    engine.runAndWait()


window = tk.Tk()
window.title("Bot")
window.configure(width=470, height=550, bg=BG_COLOR)

# head label
head_label = tk.Label(window, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10)
head_label.place(relwidth=1)

# tiny divider
line = tk.Label(window, width=450, bg=BG_GRAY)
line.place(relwidth=1, rely=0.07, relheight=0.012)

# text widget
conservation_text = tk.Text(window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=5, pady=5)
conservation_text.place(relheight=0.745, relwidth=1, rely=0.08)
conservation_text.configure(cursor="arrow")

# scroll bar
scrollbar = tk.Scrollbar(conservation_text)
scrollbar.place(relheight=1, relx=0.974)
scrollbar.configure(command=conservation_text.yview)


# bottom label
bottom_label = tk.Label(window, bg=BG_GRAY, height=80)
bottom_label.place(relwidth=1, rely=0.825)

input_text = tk.Text(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
input_text.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
input_text.focus()

text_button = tk.Button(bottom_label, text="Text", font=FONT_BOLD, bg=BG_GRAY, width=20,
                        command=lambda: threading.Thread(target=text).start())
text_button.place(relx=0.77, rely=0.008, relheight=0.03, relwidth=0.22)

audio_button = tk.Button(bottom_label, text="Audio", font=FONT_BOLD, bg=BG_GRAY, width=20,
                         command=lambda: threading.Thread(target=audio_input).start())
audio_button.place(relx=0.77, rely=0.04, relheight=0.03, relwidth=0.22)


window.mainloop()
