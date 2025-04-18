import customtkinter as ctk
from tkinter import messagebox

class ConfigMachineTemplate:
    def __init__(self, parent_window=None):
        self.parent = parent_window
        self.root = ctk.CTkToplevel()
        self._init_window()

    def _init_window(self):
        self.root.title("Configuração da Máquina")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.resizable(False, False)
        self._build_ui()
        self._center_window(550, 500)

    def _build_ui(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="Configuração da Máquina",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # Frame dos campos
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="x", padx=10, pady=10)

        # Configurações comuns
        label_style = {"font": ctk.CTkFont(size=14, weight="bold"), "anchor": "w"}
        entry_style = {"width": 300, "height": 35, "font": ctk.CTkFont(size=12)}

        # Placa-mãe
        ctk.CTkLabel(form_frame, text="Placa-mãe:", **label_style).grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        self.motherboard_entry = ctk.CTkEntry(form_frame, placeholder_text="Modelo da placa-mãe", **entry_style)
        self.motherboard_entry.grid(row=0, column=1, padx=10, pady=5)

        # Memória
        ctk.CTkLabel(form_frame, text="Memória:", **label_style).grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.memory_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: 8GB DDR4", **entry_style)
        self.memory_entry.grid(row=1, column=1, padx=10, pady=5)

        # Armazenamento
        ctk.CTkLabel(form_frame, text="Armazenamento:", **label_style).grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.storage_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: 256GB SSD", **entry_style)
        self.storage_entry.grid(row=2, column=1, padx=10, pady=5)

        # Estado de limpeza
        ctk.CTkLabel(form_frame, text="Estado de Limpeza:", **label_style).grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.clean_state_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: Limpo, Empoeirado", **entry_style)
        self.clean_state_entry.grid(row=3, column=1, padx=10, pady=5)

        # Última checagem
        ctk.CTkLabel(form_frame, text="Última Checagem:", **label_style).grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        self.last_check_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: 2025-04-18", **entry_style)
        self.last_check_entry.grid(row=4, column=1, padx=10, pady=5)

        # Lab ID
        ctk.CTkLabel(form_frame, text="Lab ID:", **label_style).grid(row=5, column=0, padx=10, pady=5, sticky="ew")
        self.lab_id_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: Lab01", **entry_style)
        self.lab_id_entry.grid(row=5, column=1, padx=10, pady=5)

        # Frame dos botões
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=20)

        # Botões
        btn_style = {
            "width": 120,
            "height": 40,
            "font": ctk.CTkFont(size=14),
            "corner_radius": 8
        }

        ctk.CTkButton(
            btn_frame,
            text="Salvar",
            command=self._handle_save,
            fg_color="#2E8B57",  # Verde
            hover_color="#3CB371",
            **btn_style
        ).pack(side="left", padx=15)

        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=self.close,
            fg_color="#B22222",  # Vermelho
            hover_color="#CD5C5C",
            **btn_style
        ).pack(side="right", padx=15)

    def _handle_save(self):
        data = {
            "motherboard": self.motherboard_entry.get().strip(),
            "memory": self.memory_entry.get().strip(),
            "storage": self.storage_entry.get().strip(),
            "clean_state": self.clean_state_entry.get().strip(),
            "last_check": self.last_check_entry.get().strip(),
            "lab_id": self.lab_id_entry.get().strip(),
        }

        if not all(data.values()):
            messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")
            return

        try:
            # Lógica para salvar os dados
            print("Dados da máquina:", data)
            messagebox.showinfo("Sucesso", "Configuração salva com sucesso!")
            self.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar configuração:\n{str(e)}")

    def _center_window(self, width, height):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def close(self):
        if self.parent:
            self.parent.deiconify()
        self.root.destroy()