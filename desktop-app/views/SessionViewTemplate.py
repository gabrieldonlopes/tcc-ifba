import customtkinter as ctk
from tkinter import ttk
from typing import List
from schemas import SessionResponse
from views.ConfigMachineTemplate import ConfigMachineTemplate

class SessionViewTemplate:
    """
    Template para a visualização de sessões de acesso em uma máquina específica.
    Exibe os dados em uma tabela e permite acesso a outras configurações.
    Aplicação: InfoDomus
    """
    # --- Constantes da Classe ---
    APP_NAME = "InfoDomus"
    AUTHOR = "by: gabriel.lopes"

    def __init__(self, machine_name: str, session_responses: List[SessionResponse], parent_window):
        self.COMPUTER_NAME = machine_name
        self.responses: List[SessionResponse] = session_responses
        self.parent = parent_window

        self.root = ctk.CTkToplevel()
        self._init_window()

    def _init_window(self):
        """Configura as propriedades iniciais da janela."""
        self.root.title(f"Acessos do Computador: {self.COMPUTER_NAME}")
        self.root.protocol("WM_DELETE_WINDOW", self.close) # <- O X da janela agora chama o novo método close

        self._create_widgets()
        self._setup_layout()
        self._style_treeview()
        self._populate_treeview()
        self._center_window(950, 550)

    def _create_widgets(self):
        """Cria todos os widgets da interface."""
        self.main_frame = ctk.CTkFrame(self.root)
        self.title_label = ctk.CTkLabel(self.main_frame, text=f"Histórico de Acessos: {self.COMPUTER_NAME}", font=ctk.CTkFont(size=18, weight="bold"))

        self.tree_frame = ctk.CTkFrame(self.main_frame)
        columns = ("session_start", "student_name", "class_var", "cpu_usage", "ram_usage", "cpu_temp", "lab_name")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_configure = ctk.CTkButton(
            self.button_frame,
            text="Configurar Dados da Máquina",
            command=self._open_config_machine
        )
        
        self.footer_label = ctk.CTkLabel(
            self.main_frame,
            text=f"{self.APP_NAME} | {self.AUTHOR}",
            font=ctk.CTkFont(size=10),
            text_color="gray50"
        )

    def _setup_layout(self):
        """Posiciona os widgets na janela."""
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.title_label.pack(pady=(10, 15))

        self.tree_frame.pack(padx=10, pady=5, fill="both", expand=True)
        self.tree.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.button_frame.pack(pady=15)
        self.btn_configure.pack(side="left", padx=10)

        self.footer_label.pack(side="bottom", pady=10)

    def _style_treeview(self):
        """Aplica um estilo escuro e moderno ao ttk.Treeview."""
        style = ttk.Style()
        style.theme_use("clam")

        bg_color = "#242424"
        text_color = "#DCE4EE"
        header_bg = "#2A2D2E"
        selected_bg = "#3A5FCD"
        odd_row_bg = "#2B2B2B"
        even_row_bg = "#242424"

        style.configure("Treeview",
                        background=bg_color,
                        foreground=text_color,
                        fieldbackground=bg_color,
                        font=("Segoe UI", 11),
                        rowheight=28)
        
        style.configure("Treeview.Heading",
                        background=header_bg,
                        foreground=text_color,
                        font=("Segoe UI", 12, "bold"),
                        relief="flat")
        
        style.map("Treeview.Heading", background=[("active", "#323638")])
        style.map("Treeview", background=[("selected", selected_bg)])

        self.tree.tag_configure("oddrow", background=odd_row_bg)
        self.tree.tag_configure("evenrow", background=even_row_bg)


    def _populate_treeview(self):
        """Define os cabeçalhos e insere os dados na tabela."""
        headers = {
            "session_start": "Início da Sessão",
            "student_name": "Estudante",
            "class_var": "Turma",
            "cpu_usage": "Uso CPU (%)",
            "ram_usage": "Uso RAM (%)",
            "cpu_temp": "Temp. CPU (°C)",
            "lab_name": "Laboratório"
        }

        for col, text in headers.items():
            self.tree.heading(col, text=text, anchor="center")
            self.tree.column(col, anchor="center", width=120, stretch=True)

        for i, r in enumerate(self.responses):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(
                r.session_start,
                r.student_name,
                r.class_var,
                r.cpu_usage,
                r.ram_usage,
                r.cpu_temp,
                r.lab_name
            ), tags=(tag,))

    def _center_window(self, width: int, height: int):
        """Centraliza a janela na tela."""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _open_config_machine(self):
        """Abre a janela de configuração da máquina."""
        ConfigMachineTemplate(parent_window=self.root)

    def close(self):
        """
        Fecha a aplicação inteira.

        Conforme solicitado, ao fechar esta janela, o programa é completamente
        encerrado em vez de retornar à tela de login.
        """
        import sys
        sys.exit(0)