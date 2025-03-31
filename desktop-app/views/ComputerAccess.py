import os
import sys
#import views.AccessDataTemplate
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from api import post_user
from utils.data_handler import verify_user

class ComputerAccess:
    def __init__(self):
        # esses dados devem ser recebidos da api
        self.COMPUTER_NAME = "ifba01"
        self.CLASS_LIST = ["1ano","2ano","3ano"]
        
        self.registered = None
        self.root = None
        
        # entradas do usuario
        self.name_entry = None
        self.password_entry = None
        self.class_var = None

    def render(self):
        self.root = ctk.CTk()
        self.root.title("Login")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)  
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        default_font = ("Arial", 12)
        self.root.option_add("*Font", default_font)

        title_label = ctk.CTkLabel(self.root, text=f"Acesso ao Computador {self.COMPUTER_NAME}", font=("Arial", 16))
        title_label.place(x=20, y=20)

        # entrada do nome
        name_label = ctk.CTkLabel(self.root, text="Name:")
        name_label.place(x=20, y=60)
        self.name_entry = ctk.CTkEntry(self.root, placeholder_text="Nome", width=200)
        self.name_entry.place(x=100, y=60)
        
        # entrada de turma
        class_label = ctk.CTkLabel(self.root, text="Turma:")
        class_label.place(x=20, y=100)
        self.class_var = ctk.StringVar(value="Selecione sua turma")
        class_menu = ctk.CTkOptionMenu(self.root, values=self.CLASS_LIST, variable=self.class_var, width=200)
        class_menu.place(x=100, y=100)
    
        # entrada do nome
        password_label = ctk.CTkLabel(self.root, text="Password:")
        password_label.place(x=20, y=140)
        self.password_entry = ctk.CTkEntry(self.root,show="*", placeholder_text="Senha", width=200)
        self.password_entry.place(x=100, y=140)
    
        # botao de confirmacao
        enter_button = ctk.CTkButton(self.root, text="Entrar", command=self.enter, width=120)
        enter_button.place(x=120, y=200)

        self.root.protocol("WM_DELETE_WINDOW", self.verify_close)
        self.center_root(self.root)
        self.root.mainloop()

    def enter(self):
        name = self.name_entry.get()
        class_name = self.class_var.get()
        password = self.password_entry.get()

        # TODO: adicionar vericação de dados do aluno
        if name == "admin" and class_name == "Selecione sua turma" and password == "admin":
            self.root.withdraw()
            #self.root.destroy()
            #views.AccessDataTemplate.AccessDataTemplate(self.COMPUTER_NAME).render()   
        elif name and password and class_name != "Selecione sua turma":
            new_user = verify_user(name, class_name, password)
            post_user(new_user)
            sys.exit()
            self.root.destroy()
        else:
            messagebox.showwarning("Atenção", "Por favor adicione todas suas informações.")

    def verify_close(self):  # TODO: this method may present problems in the future
        name = self.name_entry.get()
        password = self.password_entry.get()
        class_name = self.class_var.get()

        # TODO: impedir que a tela seja minimizada
        if not name or not password or class_name == "Selecione sua turma":
            messagebox.showwarning("Atenção", "Por favor adicione todas suas informações.")
        else:
            self.root.destroy()

    @staticmethod
    def center_root(root):
        root.update_idletasks()
        root_width = 350
        root_height = 250
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (root_width // 2)
        y = (screen_height // 2) - (root_height // 2)
        root.geometry(f"{root_width}x{root_height}+{x}+{y}")
