import customtkinter as ctk
from tkinter import messagebox
import xml.etree.ElementTree as ET
import menuPrincipal_Admin as menuAdmin
import menu_principal_empleado as menuEmpleado

# Configuración de la apariencia y el tema
ctk.set_appearance_mode("Dark")  # Opciones: "Dark", "Light"
ctk.set_default_color_theme("blue")  # Opciones: "blue", "green", "dark-blue"

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.configure_window()
        self.create_widgets()
        self.mainloop()

    def configure_window(self):
        """Configura las propiedades de la ventana principal."""
        self.title("Login")
        self.geometry("400x400")
        self.configure(padx=20, pady=20)

    def create_widgets(self):
        """Crea y organiza los widgets en la ventana."""
        self.create_title_label()
        self.create_username_entry()
        self.create_password_entry()
        self.create_filetype_combobox()
        self.create_login_button()

    def create_title_label(self):
        """Crea el título de la ventana."""
        self.lbl_title = ctk.CTkLabel(self, text="Iniciar Sesión", font=("Arial", 20, "bold"))
        self.lbl_title.pack(pady=10)

    def create_username_entry(self):
        """Crea el campo de entrada para el nombre de usuario."""
        self.lbl_username = ctk.CTkLabel(self, text="Usuario:")
        self.lbl_username.pack(pady=5)
        self.entry_username = ctk.CTkEntry(self, placeholder_text="Introduce tu usuario")
        self.entry_username.insert(0, "brand")
        self.entry_username.pack(pady=5)

    def create_password_entry(self):
        """Crea el campo de entrada para la contraseña."""
        self.lbl_password = ctk.CTkLabel(self, text="Contraseña:")
        self.lbl_password.pack(pady=5)
        self.entry_password = ctk.CTkEntry(self, show="*", placeholder_text="Introduce tu contraseña")
        self.entry_password.insert(0, "root")
        self.entry_password.pack(pady=5)

    def create_filetype_combobox(self):
        """Crea la lista desplegable para seleccionar el tipo de archivo."""
        self.lbl_filetype = ctk.CTkLabel(self, text="Tipo de Archivo:")
        self.lbl_filetype.pack(pady=5)
        self.filetype_combobox = ctk.CTkComboBox(self, values=["TXT", "XML"])
        self.filetype_combobox.set("TXT")
        self.filetype_combobox.pack(pady=5)

    def create_login_button(self):
        """Crea el botón de ingreso."""
        self.btn_login = ctk.CTkButton(self, text="Ingresar", command=self.login)
        self.btn_login.pack(pady=20)

    def get_username(self):
        return self.entry_username.get()

    def get_password(self):
        return self.entry_password.get()

    def get_filetype(self):
        return self.filetype_combobox.get()

    def login(self):
        """Maneja la lógica del inicio de sesión según el tipo de archivo seleccionado."""
        username = self.get_username()
        password = self.get_password(
            
        )
        filetype = self.get_filetype()

        user_type = self.read_user_file(filetype, username, password)

        if user_type == "ADM":
            messagebox.showinfo("Login", "Bienvenido administrador")
            self.destroy()
            menuAdmin.menuPrincipal()
        elif user_type == "VENDEDOR":
            messagebox.showinfo("Login", "Bienvenido vendedor")
            self.destroy()
            menuEmpleado.InvoiceApp()
        else:
            messagebox.showerror("Login", "Usuario o contraseña incorrectos")
            self.destroy()

    def read_user_file(self, filetype, username, password):
        """Lee el archivo de usuarios y devuelve el tipo de usuario."""
        if filetype == "TXT":
            return self.read_user_from_txt(username, password)
        elif filetype == "XML":
            return self.read_user_from_xml(username, password)
        return False

    def read_user_from_txt(self, username, password):
        """Lee el archivo TXT para obtener el tipo de usuario."""
        try:
            with open("Archivos/usuario.txt", "r") as file:
                for linea in file:
                    partes = linea.strip().split("-")
                    if username == partes[1].strip() and password == partes[2].strip():
                        return partes[3].strip()
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo de usuarios no encontrado")
        return False

    def read_user_from_xml(self, username, password):
        """Lee el archivo XML para obtener el tipo de usuario."""
        try:
            tree = ET.parse("XML/usuario.xml")
            root = tree.getroot()

            for usuario in root.findall('usuario'):
                if username == usuario.find('user').text and password == usuario.find('clave').text:
                    return usuario.find('tipo').text
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo XML: {e}")
        return False
LoginApp()
