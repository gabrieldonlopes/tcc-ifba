from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox

from pydantic import ValidationError
from schemas import MachineConfig,StateCleanliness
from config import get_machine_config_from_api,post_config_from_ui
from utils.DatePicker import DatePicker
from utils.pc_info import get_machine_config

class ConfigMachineTemplate:
    def __init__(self, parent_window=None):
        self.parent = parent_window
        
        if self.parent is None: # iniciada sozinha
            self.root = ctk.CTk()  # JANELA RAIZ
            self.is_root = True
        else: # iniciada com SessionViewTemplate
            self.root = ctk.CTkToplevel()  # JANELA FILHA
            self.is_root = False

        self._init_window()
        self._load_configurations() # Chamada síncrona

    def _init_window(self):
        self.root.title("Configuração da Máquina")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.resizable(False, False)
        self._center_window(600, 500)
        
        self.loading_label = ctk.CTkLabel(
            self.root, 
            text="Carregando configurações...", 
            font=ctk.CTkFont(size=14)
        )
        self.loading_label.pack(pady=200)

    def _load_configurations(self):
        try:
            config_data = get_machine_config_from_api()
            from_api = True

            if not config_data:
                #print("API não retornou configuração, tentando buscar configuração local.")
                config_data = get_machine_config()
                #print(config_data)
                from_api = False

            if hasattr(self, 'loading_label') and self.loading_label.winfo_exists():
                self.loading_label.destroy()

            self._build_ui()  # Constrói a UI antes de preencher os campos

            if config_data:
                # Apenas converte para MachineConfig se vier da API
                if from_api and isinstance(config_data, dict) and not isinstance(config_data, MachineConfig):
                    try:
                        config_data = MachineConfig(**config_data)
                    except ValidationError as e:
                        print("Erro de validação ao converter config da API:", e)
                        messagebox.showerror("Erro de Dados", "Erro ao validar os dados da API.")
                        return

                self._fill_form_fields(config_data)
            else:
                print("Nenhuma configuração existente encontrada.")

        except Exception as e:
            if hasattr(self, 'loading_label') and self.loading_label.winfo_exists():
                self.loading_label.destroy()

            if not hasattr(self, 'name_entry'):
                self._build_ui()

            messagebox.showerror("Erro de Carregamento", f"Não foi possível carregar as configurações: {e}")
    
    def _fill_form_fields(self, config):
        if not hasattr(self, 'name_entry'):
            return

        def get_value(obj, key):
            if isinstance(obj, dict):
                return obj.get(key)
            else:
                return getattr(obj, key, None)

        name = get_value(config, 'machine_name') or get_value(config, 'name')
        if name:
            self.name_entry.insert(0, name)

        motherboard = get_value(config, 'motherboard')
        if motherboard:
            self.motherboard_entry.insert(0, motherboard)

        memory = get_value(config, 'memory')
        if memory:
            self.memory_entry.insert(0, memory)

        storage = get_value(config, 'storage')
        if storage:
            self.storage_entry.insert(0, storage)

        lab_id = get_value(config, 'lab_id')
        if lab_id:
            self.lab_id_entry.insert(0, lab_id)

        cleanliness_value = get_value(config, 'state_cleanliness')
        if cleanliness_value:
            # Se for enum, pega o valor, se for string já usa direto
            val = cleanliness_value.value if isinstance(cleanliness_value, StateCleanliness) else cleanliness_value
            if val in self.clean_state_combobox.cget("values"):
                self.clean_state_combobox.set(val)
            else:
                self.clean_state_combobox.set(StateCleanliness.BOM)  # padrão

        last_checked = get_value(config, 'last_checked')
        if last_checked and hasattr(self, 'date_picker'):
            self.date_picker.entry.delete(0, "end")
            self.date_picker.entry.insert(0, str(last_checked))
    def _build_ui(self):
        # Destrói o loading_label se ainda existir e a UI principal for construída
        if hasattr(self, 'loading_label') and self.loading_label.winfo_exists():
            self.loading_label.destroy()

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
            "button_color": "#3b3b3b", # Cor do botão original
            "fg_color": "#343638", # Cor de fundo do combobox (padrão do CTkEntry)
            "text_color": "#DCE4EE", # Cor do texto (padrão do CTkEntry)
            "border_color": "#565B5E", # Cor da borda (padrão do CTkEntry)
            "dropdown_fg_color": "#2b2b2b",
            "dropdown_hover_color": "#3b3b3b",
            "dropdown_text_color": "#DCE4EE"
        }
        ctk.CTkLabel(form_frame, text="Estado de Limpeza:", **label_style).grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        self.clean_state_combobox = ctk.CTkComboBox(
            form_frame,
            values=[e.value for e in StateCleanliness],
            state="readonly",
            **combobox_style
        )
        self.clean_state_combobox.grid(row=4, column=1, padx=10, pady=5)
        self.clean_state_combobox.set(StateCleanliness.BOM) 

        # Última checagem
        ctk.CTkLabel(form_frame, text="Última Checagem:", **label_style).grid(row=5, column=0, padx=10, pady=5, sticky="ew")
        self.date_picker = DatePicker(form_frame) # Seu DatePicker customizado
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
            command=self._handle_save, # Chamada síncrona
            fg_color="#2E8B57", 
            hover_color="#3CB371",
            **btn_style
        ).pack(side="left", padx=15)

        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=self.close,
            fg_color="#B22222", 
            hover_color="#CD5C5C",
            **btn_style
        ).pack(side="right", padx=15)

    def _handle_save(self):
        try:
            date_str = self.date_picker.get_date_string()
            if not date_str:
                 raise ValueError("A data da última checagem deve ser preenchida.")
            
            # Validação simples do formato da data (DD/MM/AAAA)
            try:
                datetime.strptime(date_str, "%d/%m/%Y")
            except ValueError:
                raise ValueError("Formato de data inválido. Use DD/MM/AAAA.")

            data = {
                "motherboard": self.motherboard_entry.get().strip(),
                "machine_name": self.name_entry.get().strip(), # 'name' mudou para 'machine_name' para consistência com o exemplo anterior
                "memory": self.memory_entry.get().strip(),
                "storage": self.storage_entry.get().strip(),
                "state_cleanliness": self.clean_state_combobox.get(), 
                "last_checked": date_str,
                "lab_id": self.lab_id_entry.get().strip(),
            }
            
            # Validação de campos vazios, exceto talvez algum campo opcional
            # (Ajuste 'data.values()' se algum campo for opcional)
            if not all(data[key] for key in ["motherboard", "machine_name", "memory", "storage", "lab_id"]): # Verifica campos essenciais
                raise ValueError("Todos os campos obrigatórios devem ser preenchidos (Placa-mãe, Nome, Memória, Armazenamento, Lab ID).")
                
            # Assume que post_config_from_ui é agora uma função síncrona
            success, message = post_config_from_ui(data) 
            if success:
                messagebox.showinfo("Sucesso", message)
                self.close() # Fecha a janela após salvar com sucesso
            else:
                messagebox.showerror("Erro ao Salvar", message)

        except ValueError as e: # Erros de validação de campos
            messagebox.showwarning("Atenção", str(e))
        except ValidationError as e: # Erros de validação do Pydantic (se ocorrerem no `post_config_from_ui`)
            errors = "\n".join([f"{'->'.join(str(loc) for loc in error['loc'])}: {error['msg']}" 
                            for error in e.errors()])
            messagebox.showerror("Erro de Validação de Dados", f"Por favor, corrija os seguintes campos:\n{errors}")
        except Exception as e: # Outros erros inesperados
            messagebox.showerror("Erro Inesperado", f"Ocorreu uma falha ao salvar as configurações:\n{str(e)}")
            # print(f"Erro inesperado em _handle_save: {e}") # Para debug

    def _center_window(self, width, height):
        # self.root.update_idletasks() # Pode não ser necessário antes da janela ser visível
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def close(self):
        if self.root and self.root.winfo_exists():
            self.root.destroy()
            self.root = None
            if self.is_root:
                # Se é a janela raiz principal, encerra o mainloop também
                import sys
                sys.exit()
    
    def run(self):
        if self.is_root:
            self.root.mainloop()
