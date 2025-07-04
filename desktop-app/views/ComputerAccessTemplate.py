import customtkinter as ctk
from tkinter import messagebox
from typing import List, Optional
import platform

# Supondo que estes imports existam e estejam corretos
from schemas import SessionResponse
from config import get_local_config
from api import post_session, get_sessions_for_machine
from views.SessionViewTemplate import SessionViewTemplate

class ComputerAccessTemplate:
    """
    Template para a tela de login de acesso ao computador.
    Controla o acesso de alunos e administradores, bloqueando a tela até
    que um login válido seja realizado.
    Aplicação: InfoDomus
    """
    # --- Constantes da Classe para fácil manutenção ---
    APP_NAME = "InfoDomus"
    AUTHOR = "by: gabriel.lopes"
    VERSION = "versão teste 0.1v"  # <-- NOVO
    ADMIN_USER = "admin"
    MASTER_PASS = "EFASE2025"
    DEFAULT_CLASS_TEXT = "Selecione sua turma"

    def __init__(self, machine_name: str, classes: List[str], lab_name: str):
        self.COMPUTER_NAME = machine_name
        self.CLASS_LIST = classes
        self.LAB_NAME = lab_name
        
        # --- Controle de estado ---
        self.allow_close = False
        self.is_logging_in = False
        self.session_view: Optional[SessionViewTemplate] = None
    
        # --- Configuração da janela principal ---
        self.root = ctk.CTk()
        self._init_window()

    def _init_window(self):
        """Configura as propriedades iniciais da janela de forma robusta e multiplataforma."""
        self.root.title("Controle de Acesso")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root.resizable(False, False)

        self._create_widgets()
        self._setup_layout()
        self._center_window(500, 420) # Altura ajustada para a remoção de um campo

        self.root.update_idletasks()

        try:
            self.root.focus_force()
        except:
            pass

        self._apply_platform_specific_window_flags()

        self.root.protocol("WM_DELETE_WINDOW", self._handle_window_close)
        self.root.bind("<Unmap>", self._prevent_minimize)
        self.root.bind("<Return>", lambda event: self._handle_login())

    def _apply_platform_specific_window_flags(self):
        """Aplica flags específicas dependendo do sistema operacional."""
        system = platform.system()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)

        if system == "Linux":
            try:
                self.root.attributes('-type', 'splash')
            except Exception as e:
                print("Aviso: '-type splash' não suportado:", e)

    def _create_widgets(self):
        """Cria todos os widgets da interface."""
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)

        self.title_label = ctk.CTkLabel(
            self.main_frame, text=f"Acesso ao Laboratório {self.LAB_NAME}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.subtitle_label = ctk.CTkLabel(
            self.main_frame, text=f"Computador: {self.COMPUTER_NAME}",
            font=ctk.CTkFont(size=14), text_color="gray60"
        )
        self.separator = ctk.CTkFrame(self.main_frame, height=2, fg_color="gray25")

        # --- Label para o campo de nome ---
        self.name_label = ctk.CTkLabel(
            self.main_frame, text="Nome Completo",
            font=ctk.CTkFont(size=13)
        )
        
        # --- Campo de nome com novo placeholder ---
        self.name_entry = ctk.CTkEntry(
            self.main_frame, placeholder_text="ex: João da Silva", width=300, height=40
        )
        
        # --- O campo de senha foi removido ---

        self.class_var = ctk.StringVar(value=self.DEFAULT_CLASS_TEXT)
        self.class_menu = ctk.CTkOptionMenu(
            self.main_frame, values=self.CLASS_LIST, variable=self.class_var,
            height=40, font=ctk.CTkFont(size=14),
            dropdown_font=ctk.CTkFont(size=14), corner_radius=8
        )
        
        self.login_btn = ctk.CTkButton(
            self.main_frame, text="Entrar", command=self._handle_login,
            height=45, font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=8
        )

        # --- Footer com versão ---
        self.footer_label = ctk.CTkLabel(
            self.main_frame, text=f"{self.APP_NAME} | {self.AUTHOR} | {self.VERSION}",
            font=ctk.CTkFont(size=10), text_color="gray50"
        )


    def _setup_layout(self):
        """Posiciona os widgets na janela."""
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.footer_label.pack(side="bottom", pady=10)

        self.title_label.pack(pady=(20, 5), padx=20)
        self.subtitle_label.pack(pady=(0, 15), padx=20)
        self.separator.pack(fill="x", padx=30, pady=10)

        # Layout modificado para a nova label e remoção da senha
        self.name_label.pack(pady=(8, 0), padx=30, anchor="w")
        self.name_entry.pack(pady=(2, 8), padx=30, fill="x")
        # A linha para o `password_entry.pack()` foi removida
        self.class_menu.pack(pady=8, padx=30, fill="x")
        
        self.login_btn.pack(pady=(20, 15), padx=30, fill="x")

    def _handle_login(self):
        """Valida as entradas e tenta realizar o login usando a senha padrão."""
        if self.is_logging_in:
            return

        name = self.name_entry.get().strip()
        password = self.MASTER_PASS  # <-- SENHA PADRÃO USADA AQUI
        class_name = self.class_var.get()
        
        # O login de admin agora apenas checa o nome do usuário
        if name.lower() == self.ADMIN_USER:
            self._perform_admin_login()
            return
        
        # Validação para login de aluno
        if not name or class_name == self.DEFAULT_CLASS_TEXT:
            messagebox.showwarning("Atenção", "Por favor, preencha seu nome completo e selecione sua turma.")
            return

        # A senha não precisa mais ser validada aqui, pois é sempre a mesma
        self._perform_student_login(name, password, class_name)

    def _toggle_login_state(self, is_logging_in: bool):
        """Ativa/desativa o estado de 'carregando' no botão de login."""
        self.is_logging_in = is_logging_in
        if is_logging_in:
            self.login_btn.configure(state="disabled", text="Entrando...")
        else:
            self.login_btn.configure(state="normal", text="Entrar")
        self.root.update_idletasks()

    def _perform_admin_login(self):
        """Lógica para o login de administrador."""
        self._toggle_login_state(True)
        try:
            data: List[SessionResponse] = get_sessions_for_machine()
            self.allow_close = True
            self._open_session_view(data)
        except Exception as e:
            messagebox.showerror("Erro de Administrador", f"Falha ao obter dados da sessão: {e}")
        finally:
            # Não reativa o botão aqui, pois a janela de sessão deve abrir
            pass

    def _perform_student_login(self, student_name: str, password: str, class_var: str):
        """Lógica para o login de estudante via API."""
        self._toggle_login_state(True)
        try:
            success, message = post_session(
                student_name=student_name,
                password=password, # A MASTER_PASS será enviada aqui
                class_var=class_var
            )
            if success:
                self.allow_close = True
                self._close_window()
            else:
                error_title = "Falha no Login"
                error_message = f"Não foi possível entrar: {message}"
                if "401" in message:
                    error_message = "Nome de usuário ou turma estão incorretos. A senha é automática."
                messagebox.showerror(error_title, error_message)
                self._toggle_login_state(False)
                
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao servidor: {e}")
            self._toggle_login_state(False)

    def _open_session_view(self, data: List[SessionResponse]):
        """Abre a janela de visualização de sessões e esconde a de login."""
        if not self.session_view:
            self.session_view = SessionViewTemplate(
                machine_name=self.COMPUTER_NAME,
                session_responses=data,
                parent_window=self
            )
            self.root.withdraw()

    def _handle_window_close(self):
        """Controla a tentativa de fechar a janela."""
        if not self.allow_close:
            messagebox.showwarning("Acesso Negado", "Você precisa realizar o login para continuar.")
        else:
            self._close_window()

    def _prevent_minimize(self, _):
        """Impede que a janela seja minimizada."""
        if not self.allow_close:
            self.root.deiconify()

    def _close_window(self):
        """Fecha a janela de sessão (se existir) e a janela principal."""
        if self.session_view and self.session_view.root:
            try:
                self.session_view.root.destroy()
            except: # Pode já ter sido destruída
                pass
        self.root.destroy()

    def _on_session_view_closed(self):
        """Chamado quando a janela de sessão é fechada para restaurar a de login."""
        self.session_view = None
        self.allow_close = False
        self.is_logging_in = False
        self._toggle_login_state(False)
        self.root.deiconify()
        self.root.focus_force()

    def _center_window(self, width: int, height: int):
        """Centraliza a janela na tela."""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def run(self):
        """Inicia o loop principal da aplicação."""
        self.root.mainloop()