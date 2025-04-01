import customtkinter as ctk
from tkinter import ttk
from typing import List

class SessionViewTemplate:
    def __init__(self, machine_name: str, machine_responses: List[dict], parent_window):
        self.machine_responses = machine_responses
        self.parent_window = parent_window
        self.COMPUTER_NAME = machine_name
        self.root = ctk.CTkToplevel()
        self._setup_window()

    def _setup_window(self):
        self.root.title(f"Acessos da {self.COMPUTER_NAME}")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self._setup_ui()
        self._center_window(900, 500)

    def _setup_ui(self):
        title_label = ctk.CTkLabel(
            self.root, 
            text=f"Acessos da {self.COMPUTER_NAME}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)
        
        table_frame = ctk.CTkFrame(self.root)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        columns = ("session_start", "name", "class_var", "password", "cpu_usage", "ram_usage", "cpu_temp")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        headers = {
            "session_start": "Início da Sessão",
            "name": "Nome",
            "class_var": "Turma",
            "password": "Senha",
            "cpu_usage": "Uso CPU (%)",
            "ram_usage": "Uso RAM (%)",
            "cpu_temp": "Temp. CPU (°C)"
        }

        for col, text in headers.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=120, anchor='center')

        for response in self.machine_responses:
            values = (
                response.session_start,
                response.user.name,
                response.user.class_var,
                response.user.password,
                response.pc_info.cpu_usage,
                response.pc_info.ram_usage,
                response.pc_info.cpu_temp
            )
            self.tree.insert("", "end", values=values)

        self.tree.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self._configure_style()

    def _configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                      background="#2E2E2E",
                      foreground="white",
                      rowheight=25,
                      fieldbackground="#2E2E2E",
                      font=("Arial", 12))
        style.configure("Treeview.Heading",
                      background="#1C1C1C",
                      foreground="white",
                      font=("Arial", 13, "bold"))
        style.map("Treeview",
                background=[('selected', '#3A5FCD')],
                foreground=[('selected', 'white')])

    def _center_window(self, width, height):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def close(self):
        """Fecha a janela de forma controlada"""
        if self.parent_window:
            self.parent_window._on_session_view_closed()
        self.root.destroy()