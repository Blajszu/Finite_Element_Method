import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from solver import galerkin_method, create_plot

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def on_closing():
    plt.close('all')
    root.destroy()

def back_to_input():
    for widget in frame.grid_slaves():
        widget.grid_forget()
    
    title_label.grid(row=0, column=0, columnspan=3, pady=(5, 20))
    author_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
    input_frame.grid(row=2, column=0, columnspan=3, pady=10)
    button_frame.grid(row=3, column=0, columnspan=3, pady=20)

def start_app():
    entered_value = entry.get()
    try:
        n = int(entered_value)
        if n < 3:
            error_label.config(text="Liczba punktów musi być większa niż 2!")
            return
            
        error_label.config(text="")
        
        x, u = galerkin_method((0,2), n)
        
        title_label.grid_forget()
        author_label.grid_forget()
        input_frame.grid_forget()
        button_frame.grid_forget()
    
        back_button.grid(row=0, column=0, columnspan=3, pady=20)
        
        fig = create_plot(x, u)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=3, column=0, columnspan=3, pady=10)
          
    except ValueError:
        error_label.config(text="Wprowadzona wartość musi być liczbą całkowitą!")

root = tk.Tk()
root.title("Wibracje akustyczne warstwy materiału")
root.minsize(550, 370)

frame = tk.Frame(root)
frame.pack(expand=True, padx=20, pady=20)

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.columnconfigure(2, weight=1)

title_label = tk.Label(frame, text="Wibracje akustyczne warstwy materiału", font=("Arial", 18, "bold"))
title_label.grid(row=0, column=0, columnspan=3, pady=(5, 20))

author_label = tk.Label(frame, text="Autor: Oskar Blajsz", font=("Arial", 13))
author_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))

input_frame = tk.Frame(frame)
input_frame.grid(row=2, column=0, columnspan=3, pady=10)

n_label = tk.Label(input_frame, text="Podaj n:", font=("Arial", 11))
n_label.grid(row=0, column=0, padx=5, sticky="e")

entry = tk.Entry(input_frame, width=20)
entry.grid(row=0, column=1, padx=5, pady=10, sticky="w")

button_frame = tk.Frame(frame)
button_frame.grid(row=3, column=0, columnspan=3, pady=20)

button1 = tk.Button(button_frame, text="Start", command=start_app)
button1.pack(side="left", padx=10)

button2 = tk.Button(button_frame, text="Wyjdź", command=on_closing)
button2.pack(side="right", padx=10)

error_label = tk.Label(frame, text="", font=("Arial", 11), fg="red")
error_label.grid(row=4, column=0, columnspan=3, pady=10)

back_button = tk.Button(frame, text="Powrót", command=back_to_input)

center_window(root)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
