import customtkinter as ctk
from tkinter import messagebox
from api import post_user, get_all_sessions
from utils.data_handler import verify_user
from views.SessionViewTemplate import SessionViewTemplate

class ComputerAccessTemplate:
    def __init__(self):
        self.COMPUTER_NAME = "ifba01"
        self.CLASS_LIST = ["1ano", "2ano", "3ano"]
        self.root = ctk.CTk()
        self.session_view = None
        self.allow_close = False  # Controle para permitir fechamento
        self._setup_main_window()

    def _setup_main_window(self):
        self.root.title("Login")
        self.root.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configurações para impedir minimização e gerenciar fechamento
        self.root.attributes('-topmost', True)
        self.root.protocol("WM_DELETE_WINDOW", self._verify_close)
        self.root.bind("<Unmap>", self._prevent_minimize)  # Evento de minimização
        
        # Configuração da interface
        self._setup_ui()
        self._center_root()

    def _setup_ui(self):
        title_label = ctk.CTkLabel(self.root, text=f"Acesso ao Computador {self.COMPUTER_NAME}", 
                                 font=("Arial", 16))
        title_label.pack(pady=20)

        # Frame para os campos de entrada
        input_frame = ctk.CTkFrame(self.root)
        input_frame.pack(pady=10, padx=20, fill="x")

        # Entrada do nome
        ctk.CTkLabel(input_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ctk.CTkEntry(input_frame, placeholder_text="Nome", width=200)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Entrada de turma
        ctk.CTkLabel(input_frame, text="Turma:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.class_var = ctk.StringVar(value="Selecione sua turma")
        class_menu = ctk.CTkOptionMenu(input_frame, values=self.CLASS_LIST, 
                                     variable=self.class_var, width=200)
        class_menu.grid(row=1, column=1, padx=5, pady=5)
    
        # Entrada da senha
        ctk.CTkLabel(input_frame, text="Senha:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.password_entry = ctk.CTkEntry(input_frame, show="*", placeholder_text="Senha", width=200)
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
    
        # Botão de confirmação
        enter_button = ctk.CTkButton(self.root, text="Entrar", command=self._handle_login, width=120)
        enter_button.pack(pady=20)

    def _handle_login(self):
        name = self.name_entry.get().strip()
        class_name = self.class_var.get()
        password = self.password_entry.get()

        # Modo admin
        if name == "admin" and password == "admin" and class_name == "Selecione sua turma":
            self.allow_close = True  # Permite fechar a janela
            try:
                data = get_all_sessions()
                self._open_session_view(data)
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao obter dados: {str(e)}")
                self.allow_close = False
            return

        # Validação normal
        if not name or not password or class_name == "Selecione sua turma":
            messagebox.showwarning("Atenção", "Por favor adicione todas suas informações.")
            return

        try:
            new_user = verify_user(name, class_name, password)
            post_user(new_user)
            self.allow_close = True
            self._safe_close()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha no login: {str(e)}")

    def _open_session_view(self, data):
        if self.session_view is None:
            self.session_view = SessionViewTemplate(self.COMPUTER_NAME, data, self)
            self.root.withdraw()  # Esconde a janela de login

    def _on_session_view_closed(self):
        self.session_view = None
        self.root.deiconify()  # Mostra novamente a janela de login

    def _verify_close(self):
        if not self.allow_close:
            messagebox.showwarning(
                "Atenção", 
                "Por favor faça login primeiro ou insira credenciais válidas."
            )
        else:
            self._safe_close()

    def _prevent_minimize(self, event):
        if not self.allow_close:
            self.root.deiconify()  # Restaura a janela se tentar minimizar

    def _safe_close(self):
        if self.session_view:
            self.session_view.close()
        self.root.destroy()

    def _center_root(self):
        self.root.update_idletasks()
        width = 350
        height = 300
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def run(self):
        self.root.mainloop()