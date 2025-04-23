import os
import tkinter as tk
from ttkbootstrap import Style, ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
from cryptography.fernet import Fernet
import json

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Správce hesel")
        self.root.geometry("480x700")

        style = Style("darkly")

        # Cesty
        self.appdata_path = os.path.join(os.environ["LOCALAPPDATA"], "PasswordManager")
        os.makedirs(self.appdata_path, exist_ok=True)
        self.data_file = os.path.join(self.appdata_path, "data.enc")
        self.key_file = os.path.join(self.appdata_path, "key.key")

        # Šifrovací klíč
        if not os.path.exists(self.key_file):
            self.key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(self.key)
        else:
            with open(self.key_file, "rb") as f:
                self.key = f.read()

        self.cipher = Fernet(self.key)
        self.data = self.load_data()

        self.email_var = tk.StringVar()
        self.login_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.show_password = tk.BooleanVar()
        self.show_real_passwords = False  # Přidáno – řízení viditelnosti hesel

        self.create_widgets()
        self.show_entries()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Email:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.email_var, width=30).grid(row=0, column=1, columnspan=2, sticky="w")

        ttk.Label(frame, text="Login:").grid(row=1, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.login_var, width=30).grid(row=1, column=1, columnspan=2, sticky="w")

        ttk.Label(frame, text="Heslo:").grid(row=2, column=0, sticky="w")
        self.password_entry = ttk.Entry(frame, textvariable=self.password_var, width=30, show="*")
        self.password_entry.grid(row=2, column=1, sticky="w")

        ttk.Checkbutton(frame, text="Zobrazit heslo", variable=self.show_password, command=self.toggle_password).grid(row=2, column=2, sticky="w")

        ttk.Button(frame, text="Uložit", bootstyle=SUCCESS, command=self.save_entry).grid(row=3, column=1, pady=10, sticky="w")
        ttk.Button(frame, text="Zobrazit/skrýt hesla", bootstyle=INFO, command=self.toggle_password_visibility).grid(row=3, column=2, sticky="w")

        ttk.Separator(frame).grid(row=4, column=0, columnspan=3, sticky="we", pady=10)

        ttk.Label(frame, text="Vyhledávání:").grid(row=5, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.search_var, width=19).grid(row=5, column=1, sticky="we")
        ttk.Button(frame, text="Hledat", bootstyle=PRIMARY, command=self.show_entries).grid(row=5, column=2, sticky="w")

        self.listbox = tk.Listbox(frame, width=80, height=15)
        self.listbox.grid(row=6, column=0, columnspan=3, pady=10)

        ttk.Button(frame, text="Kopírovat heslo", bootstyle=SUCCESS, command=self.copy_password).grid(row=7, column=0, padx=10, pady=5, sticky="w")
        ttk.Button(frame, text="Smazat vybraný", bootstyle=DANGER, command=self.delete_selected).grid(row=7, column=2, padx=10, pady=5, sticky="e")
        ttk.Button(frame, text="Import", bootstyle=INFO, command=self.import_data).grid(row=8, column=2, padx=10, pady=5, sticky="e")
        ttk.Button(frame, text="Export", bootstyle=INFO, command=self.export_data).grid(row=8, column=0, padx=10, pady=5, sticky="w")

        # Tlačítko pro zobrazení informací o aplikaci
        ttk.Button(frame, text="O aplikaci", bootstyle=SECONDARY, command=self.show_about).grid(row=9, column=1, pady=10)

        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(1, weight=1)

    def show_about(self):
        # Vytvoří nové okno se základními informacemi o aplikaci
        about_window = tk.Toplevel(self.root)  # Vytvoření nového okna (Toplevel = samostatné menší okno)
        about_window.title("O aplikaci")       # Titulek nového okna
        about_window.geometry("300x200")       # Velikost okna (šířka x výška)

        # Nadpis
        ttk.Label(about_window, text="Správce hesel", font=("Arial", 14, "bold")).pack(pady=10)
        # Verze
        ttk.Label(about_window, text="Verze: 1.0.0").pack()
        # Autor
        ttk.Label(about_window, text="Autor: Jan Galba").pack()
        # Popis
        ttk.Label(about_window, text="Popis: Jednoduchý správce hesel\ns exportem, importem a šifrováním.", wraplength=280).pack(pady=10)

    def toggle_password(self):
        self.password_entry.config(show="" if self.show_password.get() else "*")

    def toggle_password_visibility(self):
        self.show_real_passwords = not self.show_real_passwords
        self.show_entries()

    def save_entry(self):
        email = self.email_var.get().strip()
        login = self.login_var.get().strip()
        password = self.password_var.get().strip()

        if not email and not login and not password:
            messagebox.showerror("Chyba", "Vyplň alespoň jedno pole.")
            return

        self.data.append({
            "email": email,
            "login": login,
            "password": password
        })
        self.save_data()
        messagebox.showinfo("Uloženo", "Záznam byl uložen.")

        self.email_var.set("")
        self.login_var.set("")
        self.password_var.set("")
        self.show_entries()

    def show_entries(self):
        self.listbox.delete(0, tk.END)
        search = self.search_var.get().lower()

        if not self.data:
            self.listbox.insert(tk.END, "Žádné uložené záznamy.")
        else:
            for i, entry in enumerate(self.data, 1):
                line = f"{i}. "
                if entry["email"]:
                    line += f"Email: {entry['email']} | "
                if entry["login"]:
                    line += f"Login: {entry['login']} | "
                # Skrytí/odhalení hesla
                if self.show_real_passwords:
                    line += f"Heslo: {entry['password']}"
                else:
                    line += "Heslo: ••••••"

                if not search or search in line.lower():
                    self.listbox.insert(tk.END, line)

    def delete_selected(self):
        index = self.listbox.curselection()
        if not index:
            messagebox.showwarning("Upozornění", "Vyber záznam k odstranění.")
            return

        real_index = index[0]
        if real_index >= len(self.data):
            return

        confirm = messagebox.askyesno("Potvrzení", "Opravdu chceš smazat vybraný záznam?")
        if confirm:
            self.data.pop(real_index)
            self.save_data()
            self.show_entries()
            messagebox.showinfo("Smazáno", "Záznam byl smazán.")

    def copy_password(self):
        index = self.listbox.curselection()
        if not index or index[0] >= len(self.data):
            messagebox.showwarning("Upozornění", "Vyber záznam ke kopírování.")
            return
        password = self.data[index[0]]["password"]
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        messagebox.showinfo("Zkopírováno", "Heslo bylo zkopírováno do schránky.")

    def export_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON soubory", "*.json")])
        if not file_path:
            return
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
            messagebox.showinfo("Export", "Data byla úspěšně exportována.")
        except Exception as e:
            messagebox.showerror("Chyba při exportu", str(e))

    def import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON soubory", "*.json")])
        if not file_path:
            return
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                imported = json.load(f)
            if isinstance(imported, list):
                self.data.extend(imported)
                self.save_data()
                self.show_entries()
                messagebox.showinfo("Import", "Data byla úspěšně importována.")
            else:
                messagebox.showerror("Chyba", "Neplatný formát dat.")
        except Exception as e:
            messagebox.showerror("Chyba při importu", str(e))

    def save_data(self):
        try:
            plain_json = json.dumps(self.data).encode()
            encrypted = self.cipher.encrypt(plain_json)
            with open(self.data_file, "wb") as f:
                f.write(encrypted)
        except Exception as e:
            messagebox.showerror("Chyba při ukládání", str(e))

    def load_data(self):
        if not os.path.exists(self.data_file):
            return []
        try:
            with open(self.data_file, "rb") as f:
                encrypted = f.read()
            decrypted = self.cipher.decrypt(encrypted)
            return json.loads(decrypted.decode())
        except Exception as e:
            print(f"Chyba při načítání dat: {e}")
            return []


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
