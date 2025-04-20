from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox
import asyncio

from pydantic import ValidationError
from schemas import MachineConfig,StateCleanliness
from config import get_config,post_config_from_ui
from utils.DatePicker import DatePicker

class ConfigMachineTemplate:
    def __init__(self, parent_window=None):
        self.parent = parent_window
        self.root = ctk.CTkToplevel()
        self._init_window()
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._load_configurations())

    def _init_window(self):
        self.root.title("Configuração da Máquina")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.resizable(False, False)
        self._center_window(600, 500)
        
        # Adiciona um label de carregamento inicial
        self.loading_label = ctk.CTkLabel(
            self.root, 
            text="Carregando configurações...", 
            font=ctk.CTkFont(size=14)
        )
        self.loading_label.pack(pady=200)

    async def _load_configurations(self):
        try:
            config_data = await get_config()
            
            self.loading_label.destroy()
            self._build_ui()
            
            if config_data:
                self._fill_form_fields(config_data)
                
        except Exception as e:
            self.loading_label.destroy()
            messagebox.showerror("Erro", f"Falha ao carregar configurações:\n{str(e)}")
            self._build_ui()  # Constrói a UI mesmo com erro

    def _fill_form_fields(self, config: MachineConfig):
        self.name_entry.insert(0, config.name)
        self.motherboard_entry.insert(0, config.motherboard)
        self.memory_entry.insert(0, config.memory)
        self.storage_entry.insert(0, config.storage)
        self.lab_id_entry.insert(0, config.lab_id)

        if isinstance(config.state_cleanliness, StateCleanliness):
            self.clean_state_combobox.set(config.state_cleanliness.value)
        else:
            self.clean_state_combobox.set(str(config.state_cleanliness))

        
        if hasattr(self, 'date_picker'):  # Se estiver usando DatePicker
            self.date_picker.entry.delete(0, "end")
            self.date_picker.entry.insert(0, config.last_checked)    

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

        # Nome do Computador
        ctk.CTkLabel(form_frame, text="Nome do Computador:", **label_style).grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.name_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: PC-LAB01", **entry_style)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)

        # Memória
        ctk.CTkLabel(form_frame, text="Memória:", **label_style).grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.memory_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: 8GB DDR4", **entry_style)
        self.memory_entry.grid(row=2, column=1, padx=10, pady=5)

        # Armazenamento
        ctk.CTkLabel(form_frame, text="Armazenamento:", **label_style).grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.storage_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: 256GB SSD", **entry_style)
        self.storage_entry.grid(row=3, column=1, padx=10, pady=5)

        # Estado de limpeza
        combobox_style = {
            "width": 300,
            "height": 35,
            "font": ctk.CTkFont(size=12),
            "dropdown_font": ctk.CTkFont(size=12),
            "button_color": "#3b3b3b",
            "dropdown_fg_color": "#2b2b2b",
            "dropdown_hover_color": "#3b3b3b"
        }
        ctk.CTkLabel(form_frame, text="Estado de Limpeza:", **label_style).grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        self.clean_state_combobox = ctk.CTkComboBox(
            form_frame,
            values=[e.value for e in StateCleanliness],
            state="readonly",
            **combobox_style
        )
        self.clean_state_combobox.grid(row=4, column=1, padx=10, pady=5)
        self.clean_state_combobox.set("BOM") 

        # Última checagem
        ctk.CTkLabel(form_frame, text="Última Checagem:", **label_style).grid(row=5, column=0, padx=10, pady=5, sticky="ew")
        self.date_picker = DatePicker(form_frame)
        self.date_picker.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Lab ID
        ctk.CTkLabel(form_frame, text="Lab ID:", **label_style).grid(row=6, column=0, padx=10, pady=5, sticky="ew")
        self.lab_id_entry = ctk.CTkEntry(form_frame, placeholder_text="Ex: Lab01", **entry_style)
        self.lab_id_entry.grid(row=6, column=1, padx=10, pady=5)

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
        try:
            data = {
                "motherboard": self.motherboard_entry.get().strip(),
                "name": self.name_entry.get().strip(),
                "memory": self.memory_entry.get().strip(),
                "storage": self.storage_entry.get().strip(),
                "state_cleanliness": self.clean_state_combobox.get(), 
                "last_checked": self.date_picker.get_date_string(),
                "lab_id": self.lab_id_entry.get().strip(),
            }

            # Validação de campos vazios
            if not all(data.values()):
                raise ValueError("Todos os campos devem ser preenchidos")
                
            if not self.date_picker.get_date_string():
                raise ValueError("Selecione uma data válida")

            success, message = post_config_from_ui(data)
            if success:
                messagebox.showinfo("Sucesso", message)
                self.close()
            else:
                messagebox.showerror("Erro", message)

        except ValueError as e:
            messagebox.showwarning("Atenção", str(e))
        except ValidationError as e:
            errors = "\n".join([f"{'->'.join(str(loc) for loc in error['loc'])}: {error['msg']}" 
                            for error in e.errors()])
            messagebox.showerror("Erro de Validação", f"Corrija os campos:\n{errors}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar:\n{str(e)}")


    def _center_window(self, width, height):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def close(self):
        if self.parent:
            self.parent.deiconify()
        self.root.destroy()