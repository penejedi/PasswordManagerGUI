import tkinter as tk
from gui_function import *
import threading
from PIL import ImageTk,Image


class PasswordManager(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default=r'.\Image\Graphicloads-Colorful-Long-Shadow-Unlock.ico')
        tk.Tk.title(self, 'Password Manager')
        tk.Tk.geometry(self, "+800+350")

        container = tk.Frame(self)

        container.pack(side='top', fill='both', expand='True')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, MainMenu, SavePassword, RetrievePassword):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = tk.Canvas(self, height=150, width=150)
        canvas.grid(row=0, column=0, columnspan=3)

        self.img = ImageTk.PhotoImage(Image.open(r".\Image\Very-Basic-Lock-icon.png"))
        canvas.create_image(20, 10, anchor='nw', image=self.img)
        canvas.image = self.img

        master_password_input = tk.Entry(self, width=47, borderwidth=1, show='*')
        master_password_input.grid(row=1, column=1, columnspan=2, pady=5, padx=5, sticky='nsew')
        master_password_label = tk.Label(self, text='Password: ')
        master_password_label.grid(row=1, column=0, pady=5, sticky='wns')
        master_password_button = tk.Button(self, text='Enter', padx=40, command=lambda: [threading.Thread(target=controller.show_frame(MainMenu)).start(),
                                                                                         threading.Thread(target=master(master_password_input)).start()])
        master_password_button.grid(row=2, column=0,  sticky='ns', columnspan=3, pady=5)


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = tk.Canvas(self, height=150, width=150)
        canvas.pack()

        self.img = ImageTk.PhotoImage(Image.open(r".\Image\Very-Basic-Lock-icon.png"))
        canvas.create_image(20, 10, anchor='nw', image=self.img)
        canvas.image = self.img

        save_password_button = tk.Button(self, text='Save New Password', padx=40, command=lambda: controller.show_frame(SavePassword))
        save_password_button.pack()

        retrieve_password_button = tk.Button(self, text='Retrieve Password', padx=44, command=lambda: controller.show_frame(RetrievePassword))
        retrieve_password_button.pack()

        exit_button = tk.Button(self, text='Exit', padx=82, command=exit_programme)
        exit_button.pack()


class SavePassword(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = tk.Canvas(self, height=150, width=150)
        canvas.grid(row=0, column=0, columnspan=3)

        self.img = ImageTk.PhotoImage(Image.open(r".\Image\Very-Basic-Lock-icon.png"))
        canvas.create_image(20, 10, anchor='nw', image=self.img)
        canvas.image = self.img

        website_input = tk.Entry(self, width=47, borderwidth=1)
        website_input.grid(row=1, column=1, columnspan=2)
        website_label = tk.Label(self, text='Website: ')
        website_label.grid(row=1, column=0, sticky='w')

        username_input = tk.Entry(self, width=47, borderwidth=1)
        username_input.grid(row=2, column=1, columnspan=2)
        username_label = tk.Label(self, text='Username: ')
        username_label.grid(row=2, column=0, pady=5, sticky='w')

        password_input = tk.Entry(self, width=28, borderwidth=1)
        password_input.grid(row=3, column=1, sticky='w')
        password_label = tk.Label(self, text='Password: ')
        password_label.grid(row=3, column=0, pady=3, sticky='w')

        generate_button = tk.Button(self, text='Generate Password', command=lambda: generate_password(password_input))
        generate_button.grid(row=3, column=2, padx=3)

        save_button = tk.Button(self, text='Save Password', padx=50, command=lambda: save(website_input, username_input, password_input))
        save_button.grid(row=4, column=1, columnspan=2, sticky='w', padx=32, pady=2)

        back_button = tk.Button(self, text='Main Menu', padx=58, command=lambda: controller.show_frame(MainMenu))
        back_button.grid(row=5, column=1, columnspan=2, sticky='w', padx=32, pady=2)


class RetrievePassword(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        canvas = tk.Canvas(self, height=150, width=150)
        canvas.grid(row=0, column=0, columnspan=3)

        self.img = ImageTk.PhotoImage(Image.open(r".\Image\Very-Basic-Lock-icon.png"))
        canvas.create_image(20, 10, anchor='nw', image=self.img)
        canvas.image = self.img

        website_input = tk.Entry(self, width=47, borderwidth=1)
        website_input.grid(row=1, column=1, columnspan=2)
        website_label = tk.Label(self, text='Website: ')
        website_label.grid(row=1, column=0, sticky='w')

        username_input = tk.Entry(self, width=47, borderwidth=1)
        username_input.grid(row=2, column=1, columnspan=2)
        username_label = tk.Label(self, text='Username: ')
        username_label.grid(row=2, column=0, pady=5, sticky='w')

        retrieve_button = tk.Button(self, text='Retrieve Password', padx=33, command=lambda: retrieve(website_input, username_input))
        retrieve_button.grid(row=3, column=1, columnspan=2, sticky='w', padx=32, pady=2)

        back_button = tk.Button(self, text='Main Menu', padx=50,
                                    command=lambda: controller.show_frame(MainMenu))
        back_button.grid(row=4, column=1, columnspan=2, sticky='w', padx=32, pady=2)
