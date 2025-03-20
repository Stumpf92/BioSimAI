import re
import json
import tkinter as tk
import time


window = tk.Tk()

def greet():
    name = eingabefeld.get()
    greeting = r.get()
    zeit = time.strftime("%H:%M:%S")
    print(f"hallo {name} {greeting}")
    textfeld.insert(tk.END, f"{zeit} : hallo {name} {greeting} \n")

eingabefeld = tk.Entry(window, width=50)  
eingabefeld.pack()

button = tk.Button(window, text="begrüßen", command=greet)
button.pack()

r = tk.StringVar()
r.set("Guten Abend")


radio_1 = tk.Radiobutton(window, text="Guten Morgen", variable = r, value="Guten Morgen").pack()
radio_2 = tk.Radiobutton(window, text="Guten Tag", variable = r, value="Guten Tag").pack()
radio_3 = tk.Radiobutton(window, text="Guten Abend", variable = r, value="Guten Abend").pack()

textfeld = tk.Text(window)
textfeld.pack()




window.mainloop()