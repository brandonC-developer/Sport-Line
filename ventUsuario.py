import customtkinter as ctk
from tkinter import messagebox,ttk
import Archivos as arch
import ArchivosXML as archXML
import ArchivosMongo as archM
# Configuración global del tema y apariencia
ctk.set_appearance_mode("Dark")  # Opciones: "Dark", "Light"
ctk.set_default_color_theme("blue")  # Opciones: "blue", "green", "dark-blue"

class VentanaUsuario(ctk.CTkFrame):
    def __init__(self, parent,tipo_archivo):
        super().__init__(parent)
        self.tipo_archivo = tipo_archivo
        self.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.configure(fg_color="gray15")  # Fondo oscuro

        # Configuración de la grilla
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        # Título
        lbl_titulo = ctk.CTkLabel(self, text="Gestión de Usuarios", font=ctk.CTkFont(size=20, weight="bold"))
        lbl_titulo.grid(row=0, column=0, columnspan=3, pady=10)
        
        register_frame = ctk.CTkFrame(self, fg_color="gray20", corner_radius=10)
        register_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        self.create_register_frame(register_frame)  # Mostrar la sección de registro por defecto
        
        #Botones de acciones
        btn_register = ctk.CTkButton(self, text="Registrar", command=self.crear_usuario)
        btn_register.grid(row=2, column=1, padx=5, pady=10,sticky="e")
        
        # Botón para mostrar los últimos usuarios
        btn_show_users = ctk.CTkButton(self, text="Mostrar Últimos Usuarios", command=self.mostrar_ultimos_usuarios)
        btn_show_users.grid(row=2, column=2, padx=5, pady=10, sticky="w")
        
        delete_frame = ctk.CTkFrame(self, fg_color="gray20", corner_radius=10)
        delete_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        
        self.create_delete_frame(delete_frame)
        
        view_frame = ctk.CTkFrame(self, fg_color="gray20", corner_radius=10)
        view_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        
        self.create_view_frame(view_frame)
        
    def create_register_frame(self,frame):
        """Crea la sección de registro de usuarios."""

        lbl_id = ctk.CTkLabel(frame, text="Cédula:")
        lbl_id.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_id = ctk.CTkEntry(frame)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        lbl_username = ctk.CTkLabel(frame, text="Usuario:")
        lbl_username.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_reg_username = ctk.CTkEntry(frame)
        self.entry_reg_username.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        lbl_password = ctk.CTkLabel(frame, text="Contraseña:")
        lbl_password.grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.entry_reg_password = ctk.CTkEntry(frame,show="*")
        self.entry_reg_password.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        lbl_tipo = ctk.CTkLabel(frame, text="Tipo:")
        lbl_tipo.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.lista_desplegable = ctk.CTkComboBox(frame, values=["ADM", "VENDEDOR"], state="readonly")
        self.lista_desplegable.grid(row=0, column=3, padx=5, pady=5, sticky="w")


        self.add_tipo_archivo_combobox(frame)
        
    def add_tipo_archivo_combobox(self, frame):
        """Añade un combobox para seleccionar el tipo de archivo."""
        self.lbl_tipo_archivo = ctk.CTkLabel(frame, text="Tipo de Archivo:")
        self.lbl_tipo_archivo.grid(row=3, column=0, padx=5, pady=5, sticky="e")

        self.combobox_tipo_archivo = ctk.CTkComboBox(frame, values=["txt", "xml","MongoDB"])
        self.combobox_tipo_archivo.set(self.tipo_archivo)  # Establece el valor inicial
        self.combobox_tipo_archivo.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
    def create_delete_frame(self,frame):
        """Crea la sección de eliminación de usuarios."""
        

        lbl_delete_id = ctk.CTkLabel(frame, text="ID del Usuario a Borrar:")
        lbl_delete_id.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_delete_id = ctk.CTkEntry(frame, placeholder_text="Ingrese ID")
        self.entry_delete_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        btn_delete = ctk.CTkButton(frame, text="Borrar Usuario", command=self.borrar_usuario)
        btn_delete.grid(row=0, column=2, padx=5, pady=5)

    def create_view_frame(self,frame):
        """Crea la sección para mostrar los usuarios."""
        

        # Tabla para mostrar usuarios
        self.tree = ttk.Treeview(frame, columns=("ID", "Usuario", "Contraseña", "Tipo"), show="headings")
        self.tree.heading("ID", text="Cédula")
        self.tree.heading("Usuario", text="Usuario")
        self.tree.heading("Contraseña", text="Contraseña")
        self.tree.heading("Tipo", text="Tipo")

        # Configurar el ancho de las columnas
        self.tree.column("ID", width=100, anchor="center", stretch=ctk.NO)
        self.tree.column("Usuario", width=120, anchor="center", stretch=ctk.YES)
        self.tree.column("Contraseña", width=120, anchor="center", stretch=ctk.YES)
        self.tree.column("Tipo", width=150, anchor="center", stretch=ctk.YES)

        self.tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    def crear_usuario(self):
        try:
            
            datosm = {
            "ID": self.entry_id.get(),
            "USER": self.entry_reg_username.get(),
            "CLAVE": self.entry_reg_password.get(),
            "TIPO": self.lista_desplegable.get()
            }
            
            """Registra un nuevo usuario."""
            sub_elem = ['user', 'clave', 'tipo']
            datos = [self.entry_id.get(), self.entry_reg_username.get(), self.entry_reg_password.get(), self.lista_desplegable.get()]
            tipo_archivo = self.combobox_tipo_archivo.get()
            if arch.validar().verificar_ingreso_datos(datos):
                if tipo_archivo == "txt":        
                    if arch.archivos("usuario").registrar_datos(datos):
                        messagebox.showinfo("Confirmación", "Usuario registrado")
                        self.clear_entry_fields()
                    else:
                        messagebox.showerror("Error", "Registro fallido")
                elif tipo_archivo == "xml":
                    if archXML.archivosXML("usuario").registrar_datos('usuario','id', sub_elem, datos):
                        messagebox.showinfo("Confirmación", "Registro exitoso XML")
                        self.clear_entry_fields()
                    else:
                        messagebox.showerror("Error", "Registro fallido")
                elif tipo_archivo == "MongoDB":
                    # Conecta con MongoDB y registra los datos
                    mongo_db =archM.archivosMongoDB("USUARIO")
                    if mongo_db.registrar_datos(datosm):
                        messagebox.showinfo("Confirmación", "Registro exitoso en MongoDB")
                        self.clear_entry_fields()
                    else:
                        messagebox.showerror("Error", "Registro fallido en MongoDB")
            else:
                messagebox.showerror("Error", "Por favor llene todos los campos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar los clientes: {e}")
            
    def clear_entry_fields(self):
        """Limpia los campos de entrada de datos."""
        self.entry_id.delete(0, ctk.END)
        self.entry_reg_username.delete(0, ctk.END)
        self.entry_reg_password.delete(0, ctk.END)
        self.lista_desplegable.set("")

    def mostrar_ultimos_usuarios(self):
        try:
            """Muestra los últimos usuarios registrados."""
            for i in self.tree.get_children():
                self.tree.delete(i)
            tipo_archivo = self.combobox_tipo_archivo.get()
            if tipo_archivo == "txt":
                ultimos_usuarios = arch.archivos("usuario").leerUltimos()
                for usuario in ultimos_usuarios:
                    usuario_data = usuario.split("-")
                    if len(usuario_data) == 4:
                        self.tree.insert("", ctk.END, values=usuario_data)
            elif tipo_archivo == "xml":
                # Leer los datos de clientes desde un archivo XML
                ultimos_clientes = archXML.archivosXML("usuario").leerxml("usuario","id", ['user', 'clave', 'tipo'])
                for cliente in ultimos_clientes:
                    cliente_data = [
                        cliente.get("id", ""),  # Extraer el id_cliente desde el atributo
                        cliente.get("user", ""),
                        cliente.get("clave", ""),
                        cliente.get("tipo", "")
                    ]
                    if any(cliente_data):  # Verifica que al menos un campo contenga datos
                        self.tree.insert("", "end", values=cliente_data)
            elif tipo_archivo == "MongoDB":
                # Conecta con MongoDB y obtiene los datos
                datos = archM.archivosMongoDB("USUARIO").leer_datos()
                for dato in datos:
                    cliente_data = (
                        dato.get('ID', ''),
                        dato.get('CLAVE', ''),
                        dato.get('USER', ''),
                        dato.get('TIPO', '')
                    )
                    if any(cliente_data):  # Verifica que al menos un campo contenga datos
                        self.tree.insert("", "end", values=cliente_data)
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar los clientes: {e}")

    def borrar_usuario(self):
        try:
            """Elimina un usuario registrado."""
            id_usuario = self.entry_delete_id.get()
            tipo_archivo = self.combobox_tipo_archivo.get()
            if tipo_archivo == "txt":
                if arch.archivos("usuario").borrarDatos(id_usuario):
                    messagebox.showinfo("Confirmación", "Usuario borrado exitosamente")
                    self.entry_delete_id.delete(0, ctk.END)
                else:
                    messagebox.showerror("Error", "Usuario no encontrado TXT")
            elif tipo_archivo == "xml":
                if archXML.archivosXML("usuario").borrarDatos("usuario","id",id_usuario):
                    messagebox.showinfo("Confirmación", "Usuario borrado exitosamente XML")
                    self.entry_delete_id.delete(0, 'end')
                else:
                    messagebox.showerror("Error", "Usuario no encontrado XML")
            elif tipo_archivo == "MongoDB":
                # Conecta con MongoDB y elimina el cliente
                mongo_db = archM.archivosMongoDB("USUARIO")
                filtro = {"ID":f"{id_usuario}"}
                if mongo_db.borrar_datos(filtro):
                    messagebox.showinfo("Confirmación", "Usuario borrado exitosamente en MongoDB")
                    self.entry_delete_id.delete(0, 'end')
                else:
                    messagebox.showerror("Error", "Usuario no encontrado en MongoDB")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def validar_string(self, char):
        """Valida que el input sea una cadena de texto."""
        return char.isalpha()

    def validar_number(self, char):
        """Valida que el input sea un número."""
        return char.isdigit()
