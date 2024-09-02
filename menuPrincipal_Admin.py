import customtkinter as ctk
from tkinter import messagebox
import ventUsuario as vu
import ventCliente as vc
import ventProveedor as vb
import vent_Orden_Compra as voc
import ventProducto as ven
import login as vl

# Configuración global del tema y apariencia
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class menuPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión")
        self.geometry("900x700")
        self.configure(padx=20, pady=20)

        # Configuración de la grilla principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # Crear ComboBox
        self.create_combobox()

        # Crear los botones del menú y el contenedor
        self.create_menu_buttons()
        self.create_container_frame()

        self.mainloop()

    def create_combobox(self):
        """Crea un ComboBox con opciones 'txt' y 'xml'."""
        self.combobox = ctk.CTkComboBox(self, values=["txt", "xml"])
        self.combobox.grid(row=1, column=0, padx=10, pady=10)
        self.combobox.set("xml")  # Establecer valor predeterminado

    def create_menu_buttons(self):
        """Crea los botones del menú lateral."""
        self.menu_frame = ctk.CTkFrame(self, corner_radius=10)
        self.menu_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        buttons_info = [
            ("Registrar Cliente", self.show_client),
            ("Registrar Proveedor", self.show_provider),
            ("Registrar Usuario", self.show_user),
            ("Orden de Compra", self.show_order),
            ("Registrar Producto", self.show_product),
            ("Cerrar Sesión", self.cerrar_sesion)
        ]

        for text, command in buttons_info:
            btn = ctk.CTkButton(self.menu_frame, text=text, command=command, width=180)
            btn.pack(pady=10)
    def get_tipoArchivo(self):
        return self.combobox.get()
    def create_container_frame(self):
        """Crea el contenedor principal donde se mostrarán las diferentes vistas."""
        self.container = ctk.CTkFrame(self, corner_radius=10)
        self.container.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)

    def clear_container(self):
        """Elimina todos los widgets del contenedor."""
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_client(self):
        self.clear_container()
        cliente_frame = vc.Cliente(self.container,self.get_tipoArchivo())
        cliente_frame.pack(fill="both", expand=True)

    def show_provider(self):
        self.clear_container()
        proveedor_frame = vb.VentanaProveedor(self.container,self.get_tipoArchivo())
        proveedor_frame.pack(fill="both", expand=True)

    def show_user(self):
        self.clear_container()
        usuario_frame = vu.VentanaUsuario(self.container,self.get_tipoArchivo())
        usuario_frame.pack(fill="both", expand=True)

    def show_order(self):
        self.clear_container()
        orden_frame = voc.VentanaOrdenCompra(self.container)
        orden_frame.pack(fill="both", expand=True)

    def show_product(self):
        self.clear_container()
        producto_frame = ven.VentanaProducto(self.container)
        producto_frame.pack(fill="both", expand=True)

    def cerrar_sesion(self):
        """Cierra la sesión y vuelve a la ventana de login."""
        self.destroy()
        vl.LoginApp()
