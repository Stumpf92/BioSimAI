import customtkinter as ctk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure
import threading
import time

import numpy as np

class Display():
    def __init__(self):

        ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        self.root = ctk.CTk()  
        self.root.geometry("500x500")
        self.root.title("BioSim")

        fig = Figure( dpi=100, frameon=True)
        fig.set_size_inches(2,2)
        self.t = np.arange(0, 3, .01)
        self.i = 2
        self.graph = fig.add_subplot(111)
        self.graph.plot(self.t, self.i * np.sin(self.i * np.pi * self.t))

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=30, y=5)


        self.box = ctk.CTkCanvas(self.root, width=200, height=200)
        self.box.place(x=400, y=400)
        



        threading.Thread(target=self.update).start()

        self.root.mainloop()

    
    def update(self):
        self.update_shit()
        self.i /= 1.5
        print(self.i)
        self.graph.clear()
        self.graph.plot(self.t, self.i * np.sin(self.i * np.pi * self.t))
        self.canvas.draw()
        time.sleep(2)
        self.update()

    def update_shit(self):
        self.box.delete("all")       
        self.box.create_rectangle(self.i*100, self.i*100, 50, 50, fill="blue")
        self.box.after(1000, self.update_shit)

display = Display()





