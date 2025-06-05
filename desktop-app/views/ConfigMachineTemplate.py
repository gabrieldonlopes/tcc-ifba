from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox

from pydantic import ValidationError
from schemas import MachineConfig,StateCleanliness
from config import get_machine_config,post_config_from_ui
from utils.DatePicker import DatePicker

class ConfigMachineTemplate:
    def __init__(self, parent_window=None):
        self.parent = parent_window
        self.root = ctk.CTkToplevel()
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
            # Assume que get_machine_config é agora uma função síncrona
            config_data = get_machine_config() 
            
            if hasattr(self, 'loading_label') and self.loading_label.winfo_exists():
                self.loading_label.destroy()
            
            self._build_ui() # Constrói a UI
            
            if config_data:
                # Converte o dicionário para o objeto MachineConfig (se necessário)
                # Se get_machine_config já retorna um objeto MachineConfig, isso não é necessário.
                if isinstance(config_data, dict) and not isinstance(config_data, MachineConfig):
                    config_data = MachineConfig(**config_data)
                self._fill_form_fields(config_data)
            else:
                # Se não houver config_data, pode-se preencher com valores padrão ou deixar em branco
                print("Nenhuma configuração existente encontrada.")
                
        except Exception as e:
            if hasattr(self, 'loading_label') and self.loading_label.winfo_exists():
                self.loading_label.destroy()
            
            # É importante construir a UI mesmo em caso de erro para o usuário poder interagir
            # ou para exibir uma mensagem de erro mais clara na própria UI, se desejado.
            if not hasattr(self, 'name_entry'): # Verifica se a UI já foi construída
                self._build_ui()

            messagebox.showerror("Erro de Carregamento", f"Não foi possível carregar as configurações: {e}")
            # print(f"Erro ao carregar configurações: {e}") # Para debug

    def _fill_form_fields(self, config: MachineConfig):
        # Garante que os widgets da UI existam antes de tentar preenchê-los
        if not hasattr(self, 'name_entry'):
            print("Atenção: Tentativa de preencher campos antes da UI ser construída.")
            return

        self.name_entry.insert(0, getattr(config, 'name', getattr(config, 'machine_name', ''))) # Adicionado fallback para 'machine_name'
        self.motherboard_entry.insert(0, getattr(config, 'motherboard', ''))
        self.memory_entry.insert(0, getattr(config, 'memory', ''))
        self.storage_entry.insert(0, getattr(config, 'storage', ''))
        self.lab_id_entry.insert(0, getattr(config, 'lab_id', ''))

        cleanliness_value = getattr(config, 'state_cleanliness', None)
        if isinstance(cleanliness_value, StateCleanliness): # Se for uma instância do Enum
            self.clean_state_combobox.set(cleanliness_value.value)
        elif isinstance(cleanliness_value, str): # Se for uma string (valor do Enum)
             # Garante que o valor é um dos valores válidos do combobox
            if cleanliness_value in self.clean_state_combobox.cget("values"):
                self.clean_state_combobox.set(cleanliness_value)
            else:
                print(f"Valor de limpeza '{cleanliness_value}' inválido, usando padrão.")
                self.clean_state_combobox.set(StateCleanliness.BOM) # Define um padrão
        else:
            self.clean_state_combobox.set(StateCleanliness.BOM) # Define um padrão se não houver valor
        
        last_checked_date = getattr(config, 'last_checked', None)
        if last_checked_date and hasattr(self, 'date_picker'):
            self.date_picker.entry.delete(0, "end")
            # Formata a data se necessário, aqui assumimos que já é uma string "DD/MM/AAAA"
            # Se for um objeto datetime, formate: datetime.strptime(last_checked_date, "%Y-%m-%d").strftime("%d/%m/%Y")
            self.date_picker.entry.insert(0, str(last_checked_date))

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
        # if self.parent and self.parent.winfo_exists(): # Verifica se a janela pai existe
        #    self.parent.deiconify()
        if self.root and self.root.winfo_exists():
            self.root.destroy()
            self.root = None # Ajuda o garbage collector
    
    def run(self):
        # Certifica-se de que a janela principal ainda não foi destruída
        if self.root and self.root.winfo_exists():
            self.root.mainloop()
