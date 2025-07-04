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
    ADMIN_USER = "admin"
    ADMIN_PASS = "admin"
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
        self._center_window(500, 450)

        # Atualiza para garantir que a geometria seja reconhecida antes de aplicar foco
        self.root.update_idletasks()

        # Força foco e traz janela à frente (pode falhar no Linux dependendo do WM)
        try:
            self.root.focus_force()
        except:
            pass

        self.name_entry.focus_set()

        # Aplica propriedades específicas conforme o SO
        self._apply_platform_specific_window_flags()

        self.root.protocol("WM_DELETE_WINDOW", self._handle_window_close)
        self.root.bind("<Unmap>", self._prevent_minimize)
        self.root.bind("<Return>", lambda event: self._handle_login())

    def _apply_platform_specific_window_flags(self):
        """Aplica flags específicas dependendo do sistema operacional."""
        system = platform.system()

        # Remove bordas e coloca janela sempre no topo
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)

        if system == "Linux":
            # Compatível apenas com X11 (não funciona no Wayland!)
            try:
                self.root.attributes('-type', 'splash')
            except Exception as e:
                print("Aviso: '-type splash' não suportado:", e)

    def _create_widgets(self):
        """Cria todos os widgets da interface."""
        # --- Frame principal ---
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)

        # --- Título e subtítulo ---
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Acesso ao Laboratório {self.LAB_NAME}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Computador: {self.COMPUTER_NAME}",
            font=ctk.CTkFont(size=14),
            text_color="gray60"
        )
        self.separator = ctk.CTkFrame(self.main_frame, height=2, fg_color="gray25")

        # --- Campos de entrada ---
        self.name_entry = ctk.CTkEntry(
            self.main_frame, placeholder_text="Nome Completo", width=300, height=40
        )
        self.password_entry = ctk.CTkEntry(
            self.main_frame, placeholder_text="Senha", show="*", width=300, height=40
        )
        self.class_var = ctk.StringVar(value=self.DEFAULT_CLASS_TEXT)
        self.class_menu = ctk.CTkOptionMenu(
            self.main_frame,
            values=self.CLASS_LIST,
            variable=self.class_var,
            height=40,
            font=ctk.CTkFont(size=14),
            dropdown_font=ctk.CTkFont(size=14),
            corner_radius=8
        )
        
        # --- Botão de Login ---
        self.login_btn = ctk.CTkButton(
            self.main_frame,
            text="Entrar",
            command=self._handle_login,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=8
        )

        # --- Footer ---
        self.footer_label = ctk.CTkLabel(
            self.main_frame,
            text=f"{self.APP_NAME} | {self.AUTHOR}",
            font=ctk.CTkFont(size=10),
            text_color="gray50"
        )


    def _setup_layout(self):
        """Posiciona os widgets na janela."""
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Empacota o footer primeiro com side='bottom' para fixá-lo na base
        self.footer_label.pack(side="bottom", pady=10)

        # Widgets principais
        self.title_label.pack(pady=(20, 5), padx=20)
        self.subtitle_label.pack(pady=(0, 15), padx=20)
        self.separator.pack(fill="x", padx=30, pady=10)

        self.name_entry.pack(pady=8, padx=30, fill="x")
        self.password_entry.pack(pady=8, padx=30, fill="x")
        self.class_menu.pack(pady=8, padx=30, fill="x")
        
        # O padding inferior do botão foi ajustado para dar espaço ao footer
        self.login_btn.pack(pady=(20, 15), padx=30, fill="x")

    def _handle_login(self):
        """Valida as entradas e tenta realizar o login."""
        if self.is_logging_in:
            return

        name = self.name_entry.get().strip()
        password = self.password_entry.get()
        class_name = self.class_var.get()
        
        is_admin_login = (name == self.ADMIN_USER and password == self.ADMIN_PASS)
        is_master_login = (password == self.MASTER_PASS)

        if is_admin_login or is_master_login:
            self._perform_admin_login()
            return
        
        if not name or not password or class_name == self.DEFAULT_CLASS_TEXT:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return

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
        """Lógica para o login de administrador ou com senha mestre."""
        self._toggle_login_state(True)
        try:
            data: List[SessionResponse] = get_sessions_for_machine()
            self.allow_close = True
            self._open_session_view(data)
        except Exception as e:
            messagebox.showerror("Erro de Administrador", f"Falha ao obter dados da sessão: {e}")
            self.allow_close = False
        finally:
            pass

    def _perform_student_login(self, student_name: str, password: str, class_var: str):
        """Lógica para o login de estudante via API."""
        self._toggle_login_state(True)
        try:
            success, message = post_session(
                student_name=student_name,
                password=password,
                class_var=class_var
            )
            if success:
                self.allow_close = True
                self._close_window()
                # Se o login for bem-sucedido, a janela fecha e não fazemos mais nada.
            else:
                error_title = "Falha no Login"
                error_message = f"Não foi possível entrar: {message}"
                if "401" in message:
                    error_message = "Nome de usuário, senha ou turma estão incorretos."
                messagebox.showerror(error_title, error_message)
                self._toggle_login_state(False)
                
        except Exception as e:
            # Houve uma exceção, então mostramos o erro E REATIVAMOS o botão.
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao servidor: {e}")
            self._toggle_login_state(False) # <--- CORREÇÃO AQUI

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
            self.session_view.root.destroy()
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