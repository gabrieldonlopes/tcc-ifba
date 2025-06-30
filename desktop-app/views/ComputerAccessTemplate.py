import customtkinter as ctk
from tkinter import messagebox
from schemas import SessionResponse
from typing import List
from config import get_local_config
from api import post_session, get_sessions_for_machine
from views.SessionViewTemplate import SessionViewTemplate

class ComputerAccessTemplate:
    def __init__(self,machine_name,classes,lab_name):

        self.COMPUTER_NAME = machine_name
        self.CLASS_LIST = classes
        self.LAB_NAME = lab_name
        self.allow_close = False
        self.session_view = None

        self.root = ctk.CTk()
        self._init_window()

    def _init_window(self):
        self.root.title("Login")
        self.root.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root.attributes('-topmost', True)
        self.root.protocol("WM_DELETE_WINDOW", self._handle_window_close)
        self.root.bind("<Unmap>", self._prevent_minimize)

        self._build_ui()
        self._center_window(400, 350)  # Aumentei um pouco o tamanho para melhor visualização

    def _build_ui(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Título
        title = ctk.CTkLabel(
            main_frame, 
            text=f"Acesso ao Computador {self.COMPUTER_NAME} do laboratório {self.LAB_NAME}", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(10, 20))

        # Frame dos campos de entrada
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(pady=10, padx=10, fill="x")

        # Nome
        ctk.CTkLabel(input_frame, text="Nome:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, padx=5, pady=(10, 5), sticky="w")
        self.name_entry = ctk.CTkEntry(
            input_frame, 
            placeholder_text="Digite seu nome completo",
            width=250,
            height=35,
            font=ctk.CTkFont(size=14)
        )
        self.name_entry.grid(row=0, column=1, padx=5, pady=(10, 5))

        # Turma
        ctk.CTkLabel(input_frame, text="Turma:", font=ctk.CTkFont(weight="bold")).grid(
            row=1, column=0, padx=5, pady=5, sticky="w")
        self.class_var = ctk.StringVar(value="Selecione sua turma")
        class_menu = ctk.CTkOptionMenu(
            input_frame, 
            values=self.CLASS_LIST, 
            variable=self.class_var, 
            width=250,
            height=35,
            font=ctk.CTkFont(size=14),
            dropdown_font=ctk.CTkFont(size=14)
        )
        class_menu.grid(row=1, column=1, padx=5, pady=5)

        # Senha (substituindo o CPF)
        ctk.CTkLabel(input_frame, text="Senha:", font=ctk.CTkFont(weight="bold")).grid(
            row=2, column=0, padx=5, pady=(5, 10), sticky="w")
        self.password_entry = ctk.CTkEntry(
            input_frame, 
            placeholder_text="Digite sua senha",
            width=250,
            height=35,
            font=ctk.CTkFont(size=14),
            show="*"  # Mostrar asteriscos para a senha
        )
        self.password_entry.grid(row=2, column=1, padx=5, pady=(5, 10))

        # Botão de login
        login_btn = ctk.CTkButton(
            main_frame,
            text="Entrar",
            command=self._handle_login,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8
        )
        login_btn.pack(pady=(20, 10))

    def _handle_login(self):
        name = self.name_entry.get().strip()
        class_var = self.class_var.get()
        password = self.password_entry.get()

        # Login de administrador
        if name == "admin" and password == "admin" and class_var == "Selecione sua turma":
            self.allow_close = True
            try:
                data: List[SessionResponse] = get_sessions_for_machine()
                #print(data)
                self._open_session_view(data)
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao obter dados: {str(e)}")
                self.allow_close = False
            return

        # Validação dos campos
        if not name or not password or class_var == "Selecione sua turma":
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return

        try:
         #   user = verify_user(name, class_name, password)  # Modificado para usar senha
            post_session(student_name=name,password=password,class_var=class_var)
            self.allow_close = True
            self._close_window()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha no login: {str(e)}")

    def _open_session_view(self, data):
        if not self.session_view:
            self.session_view = SessionViewTemplate(machine_name=self.COMPUTER_NAME,session_responses=data,parent_window=self)
            self.root.withdraw()

    def _handle_window_close(self):
        if not self.allow_close:
            messagebox.showwarning("Atenção", "Realize o login para fechar.")
        else:
            self._close_window()

    def _prevent_minimize(self, _):
        if not self.allow_close:
            self.root.deiconify()

    def _close_window(self):
        if self.session_view:
            self.session_view.root.destroy()  # Modificado para fechar corretamente
        self.root.destroy()

    def _on_session_view_closed(self):
        self.session_view = None
        self.root.deiconify()

    def _center_window(self, width, height):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def run(self):
        self.root.mainloop()