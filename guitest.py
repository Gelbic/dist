import os
import json
from cryptography.fernet import Fernet
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListView, QCheckBox, QInputDialog, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QStringListModel

class PasswordManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Správce hesel")
        self.setGeometry(100, 100, 600, 600)

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

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Formulář pro zadání údajů
        form_layout = QVBoxLayout()

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        form_layout.addWidget(self.email_input)

        self.login_input = QLineEdit(self)
        self.login_input.setPlaceholderText("Login")
        form_layout.addWidget(self.login_input)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Heslo")
        form_layout.addWidget(self.password_input)

        self.show_password_checkbox = QCheckBox("Zobrazit heslo", self)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)
        form_layout.addWidget(self.show_password_checkbox)

        self.save_button = QPushButton("Uložit", self)
        self.save_button.clicked.connect(self.save_entry)
        form_layout.addWidget(self.save_button)

        layout.addLayout(form_layout)

        # Vyhledávání
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Vyhledávání")
        self.search_input.textChanged.connect(self.show_entries)
        layout.addWidget(self.search_input)

        # Seznam uložených záznamů
        self.list_view = QListView(self)
        self.list_model = QStringListModel(self)
        self.list_view.setModel(self.list_model)
        layout.addWidget(self.list_view)

        # Akční tlačítka
        action_layout = QHBoxLayout()

        self.delete_button = QPushButton("Smazat vybraný", self)
        self.delete_button.clicked.connect(self.delete_selected)
        action_layout.addWidget(self.delete_button)

        self.copy_button = QPushButton("Kopírovat heslo", self)
        self.copy_button.clicked.connect(self.copy_password)
        action_layout.addWidget(self.copy_button)

        self.import_button = QPushButton("Import", self)
        self.import_button.clicked.connect(self.import_data)
        action_layout.addWidget(self.import_button)

        self.export_button = QPushButton("Export", self)
        self.export_button.clicked.connect(self.export_data)
        action_layout.addWidget(self.export_button)

        layout.addLayout(action_layout)

        # O aplikaci
        self.about_button = QPushButton("O aplikaci", self)
        self.about_button.clicked.connect(self.show_about)
        layout.addWidget(self.about_button)

        self.setLayout(layout)

    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def save_entry(self):
        email = self.email_input.text().strip()
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()

        if not email and not login and not password:
            QMessageBox.critical(self, "Chyba", "Vyplň alespoň jedno pole.")
            return

        self.data.append({
            "email": email,
            "login": login,
            "password": password
        })
        self.save_data()
        QMessageBox.information(self, "Uloženo", "Záznam byl uložen.")

        self.email_input.clear()
        self.login_input.clear()
        self.password_input.clear()
        self.show_entries()

    def show_entries(self):
        search = self.search_input.text().lower()
        filtered_data = [f"Email: {entry['email']} | Login: {entry['login']} | Heslo: {entry['password']}" for entry in self.data if search in entry['email'].lower() or search in entry['login'].lower()]

        self.list_model.setStringList(filtered_data)

    def delete_selected(self):
        selected_index = self.list_view.selectedIndexes()
        if not selected_index:
            QMessageBox.warning(self, "Upozornění", "Vyber záznam k odstranění.")
            return

        real_index = selected_index[0].row()
        if real_index >= len(self.data):
            return

        confirm = QMessageBox.question(self, "Potvrzení", "Opravdu chceš smazat vybraný záznam?")
        if confirm == QMessageBox.Yes:
            self.data.pop(real_index)
            self.save_data()
            self.show_entries()
            QMessageBox.information(self, "Smazáno", "Záznam byl smazán.")

    def copy_password(self):
        selected_index = self.list_view.selectedIndexes()
        if not selected_index or selected_index[0].row() >= len(self.data):
            QMessageBox.warning(self, "Upozornění", "Vyber záznam ke kopírování.")
            return

        password = self.data[selected_index[0].row()]["password"]
        QApplication.clipboard().setText(password)
        QMessageBox.information(self, "Zkopírováno", "Heslo bylo zkopírováno do schránky.")

    def export_data(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export", "", "JSON soubory (*.json)")
        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
            QMessageBox.information(self, "Export", "Data byla úspěšně exportována.")
        except Exception as e:
            QMessageBox.critical(self, "Chyba při exportu", str(e))

    def import_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import", "", "JSON soubory (*.json)")
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                imported = json.load(f)
            if isinstance(imported, list):
                self.data.extend(imported)
                self.save_data()
                self.show_entries()
                QMessageBox.information(self, "Import", "Data byla úspěšně importována.")
            else:
                QMessageBox.critical(self, "Chyba", "Neplatný formát dat.")
        except Exception as e:
            QMessageBox.critical(self, "Chyba při importu", str(e))

    def save_data(self):
        try:
            plain_json = json.dumps(self.data).encode()
            encrypted = self.cipher.encrypt(plain_json)
            with open(self.data_file, "wb") as f:
                f.write(encrypted)
        except Exception as e:
            QMessageBox.critical(self, "Chyba při ukládání", str(e))

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

    def show_about(self):
        about_message = "Správce hesel\nVerze: 1.0.0\nAutor: Jan Galba\nPopis: Jednoduchý správce hesel s exportem, importem a šifrováním."
        QMessageBox.information(self, "O aplikaci", about_message)


if __name__ == "__main__":
    app = QApplication([])
    window = PasswordManager()
    window.show()
    app.exec()
