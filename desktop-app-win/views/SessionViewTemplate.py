import customtkinter as ctk
from tkinter import ttk
from typing import List

from views.ConfigMachineTemplate import ConfigMachineTemplate

class SessionViewTemplate:
    def __init__(self, machine_name: str, machine_responses: List[dict], parent_window):
        self.COMPUTER_NAME = machine_name
        self.responses = machine_responses
        self.parent = parent_window

        self.root = ctk.CTkToplevel()
        self._init_window()

    def _init_window(self):
        self.root.title(f"Acessos da {self.COMPUTER_NAME}")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self._build_ui()
        self._center_window(900, 500)

    def _build_ui(self):
        ctk.CTkLabel(self.root, text=f"Acessos da {self.COMPUTER_NAME}", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        frame = ctk.CTkFrame(self.root)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Criar um frame adicional para a treeview e scrollbar
        tree_frame = ctk.CTkFrame(frame)
        tree_frame.pack(fill="both", expand=True)

        columns = ("session_start", "name", "class_var", "cpf", "cpu_usage", "ram_usage", "cpu_temp")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

        headers = {
            "session_start": "Início da Sessão",
            "name": "Nome",
            "class_var": "Turma",
            "cpf": "CPF",
            "cpu_usage": "Uso CPU (%)",
            "ram_usage": "Uso RAM (%)",
            "cpu_temp": "Temp. CPU (°C)"
        }

        for col, text in headers.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, anchor="center", width=120)

        for r in self.responses:
            self.tree.insert("", "end", values=(
                r.session_start,
                r.user.name,
                r.user.class_var,
                r.user.password,
                r.pc_info.cpu_usage,
                r.pc_info.ram_usage,
                r.pc_info.cpu_temp
            ))

        # Configurar a scrollbar antes de empacotar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Empacotar a treeview e scrollbar no mesmo frame
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=20)

        btn_configure = ctk.CTkButton(
            button_frame, 
            text="Configurar Dados da Máquina", 
            command=self._open_config_machine
        )
        btn_configure.pack(side="left", padx=20)

        self._style_treeview()

    def _style_treeview(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background="#1f1f1f",
                        foreground="white",
                        rowheight=28,
                        fieldbackground="#1f1f1f",
                        font=("Segoe UI", 12))

        style.configure("Treeview.Heading",
                        background="#333333",
                        foreground="white",
                        font=("Segoe UI", 13, "bold"),
                        relief="flat")

        style.map("Treeview.Heading",
                background=[("active", "#444444")])

        style.map("Treeview",
                background=[("selected", "#3A5FCD")],
                foreground=[("selected", "white")])

        self.tree.tag_configure("evenrow", background="#2a2a2a")
        self.tree.tag_configure("oddrow", background="#242424")


    def _center_window(self, width, height):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _open_config_machine(self):
        ConfigMachineTemplate(parent_window=self.root)

    def close(self):
        if self.parent:
            # Em vez de self.parent.destroy(), chamamos o método apropriado
            self.parent._on_session_view_closed()
        self.root.destroy()
        # Se realmente precisar encerrar o programa completamente:
        import sys
        sys.exit(0)
