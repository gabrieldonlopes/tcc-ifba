import customtkinter as ctk
import tkinter as tk
from tkcalendar import DateEntry
from datetime import datetime

class DatePicker(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._create_widgets()
        self.selected_date = None

    def _create_widgets(self):
        self.entry = ctk.CTkEntry(
            self, 
            width=120,
            placeholder_text="DD-MM-AAAA",
            font=ctk.CTkFont(size=12)
        )
        self.entry.pack(side="left", padx=(0, 5))

        self.btn = ctk.CTkButton(
            self,
            text="📅",
            width=30,
            command=self._open_calendar,
            font=ctk.CTkFont(size=14)
        )
        self.btn.pack(side="left")

    def _open_calendar(self):
        top = tk.Toplevel(self)
        top.title("Selecione a Data")
        top.transient(self)
        
        # Garante que a janela seja exibida antes do grab_set
        top.update_idletasks()
        
        # Configuração do calendário
        cal = DateEntry(
            top,
            date_pattern="dd-mm-yyyy",
            background="gray20",
            foreground="white",
            font=("Arial", 10)
        )
        cal.pack(pady=10, padx=10)

        btn_frame = ctk.CTkFrame(top, fg_color="transparent")
        btn_frame.pack(pady=5)
        
        confirm_btn = ctk.CTkButton(
            btn_frame,
            text="Confirmar",
            command=lambda: self._set_date(cal.get_date(), top),
            width=100
        )
        confirm_btn.pack(pady=5)

        # Só faz grab_set depois que a janela estiver pronta
        top.after(100, lambda: self._safe_grab(top))

    def _safe_grab(self, window):
        try:
            window.grab_set()
        except tk.TclError:
            window.after(100, lambda: self._safe_grab(window))

    def _set_date(self, date, window):
        self.selected_date = date
        self.entry.delete(0, "end")
        self.entry.insert(0, date.strftime("%d-%m-%Y"))
        window.grab_release()
        window.destroy()

    def get(self):
        return self.selected_date

    def get_date_string(self):
        return self.entry.get()