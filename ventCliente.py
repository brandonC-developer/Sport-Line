import customtkinter as ctk
from tkinter import messagebox, ttk
import Archivos as arch
import ArchivosXML as archXML 
import ArchivosMongo as archMongo
# Configuración global del tema y apariencia
ctk.set_appearance_mode("Dark")  # Opciones: "Dark", "Light"
ctk.set_default_color_theme("blue")  # Opciones: "blue", "green", "dark-blue"

class Cliente(ctk.CTkFrame):
    def __init__(self, parent, tipo_archivo):
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
        lbl_titulo = ctk.CTkLabel(self, text="Registro de Cliente", font=ctk.CTkFont(size=20, weight="bold"))
        lbl_titulo.grid(row=0, column=0, columnspan=4, pady=10)

        # Sección de datos del cliente
        cliente_frame = ctk.CTkFrame(self, fg_color="gray20", corner_radius=10)
        cliente_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        self.add_cliente_fields(cliente_frame)
        self.add_tipo_archivo_combobox(cliente_frame)  # Agrega el combobox

        # Botones de acciones
        btn_register = ctk.CTkButton(self, text="Registrar", command=self.crear_usuario)
        btn_register.grid(row=2, column=1, padx=5, pady=10, sticky="e")

        btn_show_last_clients = ctk.CTkButton(self, text="Mostrar Últimos Clientes", command=self.mostrar_ultimos_clientes)
        btn_show_last_clients.grid(row=2, column=2, padx=5, pady=10, sticky="w")

        # Sección de eliminación de cliente
        delete_frame = ctk.CTkFrame(self, fg_color="gray20", corner_radius=10)
        delete_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        self.add_delete_fields(delete_frame)

        # Tabla para mostrar últimos clientes
        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Apellido", "Correo"), show="headings")
        self.setup_treeview()
        self.tree.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.mainloop()
        
    def add_tipo_archivo_combobox(self, frame):
        """Añade un combobox para seleccionar el tipo de archivo."""
        self.lbl_tipo_archivo = ctk.CTkLabel(frame, text="Tipo de Archivo:")
        self.lbl_tipo_archivo.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.combobox_tipo_archivo = ctk.CTkComboBox(frame, values=["txt", "xml","MongoDB"])
        self.combobox_tipo_archivo.set(self.tipo_archivo)  # Establece el valor inicial
        self.combobox_tipo_archivo.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    def add_cliente_fields(self, frame):
        """Añade los campos de datos del cliente."""
        self.lbl_id = ctk.CTkLabel(frame, text="Cédula:")
        self.lbl_id.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_id = ctk.CTkEntry(frame,)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.entry_id.configure(validate="key", validatecommand=(self.register(self.validar_number), "%S"))

        self.lbl_nombre = ctk.CTkLabel(frame, text="Nombre:")
        self.lbl_nombre.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_nombre = ctk.CTkEntry(frame)
        self.entry_nombre.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.entry_nombre.configure(validate="key", validatecommand=(self.register(self.validar_string), "%S"))

        self.lbl_apellido = ctk.CTkLabel(frame, text="Apellido:")
        self.lbl_apellido.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_reg_apellido = ctk.CTkEntry(frame)
        self.entry_reg_apellido.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.entry_reg_apellido.configure(validate="key", validatecommand=(self.register(self.validar_string), "%S"))

        self.lbl_correo = ctk.CTkLabel(frame, text="Correo:")
        self.lbl_correo.grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.entry_reg_correo = ctk.CTkEntry(frame)
        self.entry_reg_correo.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    def add_delete_fields(self, frame):
        """Añade los campos de eliminación de cliente."""
        lbl_delete_id = ctk.CTkLabel(frame, text="ID del Cliente a Borrar:")
        lbl_delete_id.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_delete_id = ctk.CTkEntry(frame, placeholder_text="Ingrese ID")
        self.entry_delete_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        btn_delete = ctk.CTkButton(frame, text="Borrar Cliente", command=self.borrar_cliente)
        btn_delete.grid(row=0, column=2, padx=5, pady=5)

    def setup_treeview(self):
        """Configura la tabla para mostrar los últimos clientes."""
        self.tree.heading("ID", text="Cédula")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Correo", text="Correo")

        self.tree.column("ID", anchor="center", width=70)
        self.tree.column("Nombre", anchor="center", width=120)
        self.tree.column("Apellido", anchor="center", width=120)
        self.tree.column("Correo", anchor="center", width=150)

    def crear_usuario(self):
        
        try:
            
            datosm = {
            "ID_CLIENTE": self.entry_id.get(),
            "NOMBRE": self.entry_nombre.get(),
            "APELLIDO": self.entry_reg_apellido.get(),
            "CORREO": self.entry_reg_correo.get()
            }
            
            """Registra un nuevo cliente."""
            sub_elem = ['nombre', 'apellido', 'correo']
            datos = [self.entry_id.get(), self.entry_nombre.get(), self.entry_reg_apellido.get(), self.entry_reg_correo.get()]
            tipo_archivo = self.combobox_tipo_archivo.get()  # Obtiene el tipo de archivo seleccionado
            if arch.validar().verificar_ingreso_datos(datos):
                if tipo_archivo == "txt":
                    if arch.archivos("cliente").registrar_datos(datos):
                        messagebox.showinfo("Confirmación", "Registro exitoso TXT")
                        self.clear_entry_fields()
                    else:
                        messagebox.showerror("Error", "Registro fallido")
                elif tipo_archivo == "xml":
                    if archXML.archivosXML("cliente").registrar_datos('cliente','id_cliente', sub_elem, datos):
                        messagebox.showinfo("Confirmación", "Registro exitoso XML")
                        self.clear_entry_fields()
                    else:
                        messagebox.showerror("Error", "Registro fallido")
                elif tipo_archivo == "MongoDB":
                    # Conecta con MongoDB y registra los datos
                    mongo_db =archMongo.archivosMongoDB("CLIENTE")
                    if mongo_db.registrar_datos(datosm):
                        messagebox.showinfo("Confirmación", "Registro exitoso en MongoDB")
                        self.clear_entry_fields()
                    else:
                        messagebox.showerror("Error", "Registro fallido en MongoDB")
            else:
                messagebox.showerror("Error", "Todos los campos son requeridos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al Registrar los clientes: {e}")
            
    def clear_entry_fields(self):
        """Limpia los campos de entrada de datos."""
        self.entry_id.delete(0, ctk.END)
        self.entry_nombre.delete(0, ctk.END)
        self.entry_reg_apellido.delete(0, ctk.END)
        self.entry_reg_correo.delete(0, ctk.END)

    def mostrar_ultimos_clientes(self):
        """Muestra los últimos clientes registrados, según el tipo de archivo."""
        try:
            # Limpiar el Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Obtén el tipo de archivo seleccionado desde el combobox
            tipo_archivo = self.combobox_tipo_archivo.get()

            if tipo_archivo == "txt":
                # Leer los últimos clientes desde un archivo de texto
                ultimos_clientes = arch.archivos("cliente").leerUltimos()
                for cliente in ultimos_clientes:
                    cliente_data = cliente.split("-")
                    if len(cliente_data) == 4:  # Asegúrate de que haya exactamente 4 elementos
                        self.tree.insert("", "end", values=cliente_data)
                    
            elif tipo_archivo == "xml":
                # Leer los datos de clientes desde un archivo XML
                ultimos_clientes = archXML.archivosXML("cliente").leerxml("cliente","id_cliente", ["nombre", "apellido", "correo"])
                for cliente in ultimos_clientes:
                    cliente_data = [
                        cliente.get("id_cliente", ""),  # Extraer el id_cliente desde el atributo
                        cliente.get("nombre", ""),
                        cliente.get("apellido", ""),
                        cliente.get("correo", "")
                    ]
                    if any(cliente_data):  # Verifica que al menos un campo contenga datos
                        self.tree.insert("", "end", values=cliente_data)
            elif tipo_archivo == "MongoDB":
                # Conecta con MongoDB y obtiene los datos
                datos = archMongo.archivosMongoDB("CLIENTE").leer_datos()
                for dato in datos:
                    cliente_data = (
                        dato.get('ID_CLIENTE', ''),
                        dato.get('NOMBRE', ''),
                        dato.get('APELLIDO', ''),
                        dato.get('CORREO', '')
                    )
                    if any(cliente_data):  # Verifica que al menos un campo contenga datos
                        self.tree.insert("", "end", values=cliente_data)
            else:
                messagebox.showwarning("Advertencia", "Seleccione un tipo de archivo válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar los clientes: {e}")


    def borrar_cliente(self):
        try:
            """Borra un cliente."""
            id_cliente = self.entry_delete_id.get()
            tipo_archivo = self.combobox_tipo_archivo.get()  # Obtiene el tipo de archivo seleccionado

            if tipo_archivo == "txt":
                if arch.archivos("cliente").borrarDatos(id_cliente):
                    messagebox.showinfo("Confirmación", "Cliente borrado exitosamente TXT")
                    self.entry_delete_id.delete(0, 'end')
                else:
                    messagebox.showerror("Error", "Cliente no encontrado TXT")
            elif tipo_archivo == "xml":
                if archXML.archivosXML("cliente").borrarDatos("cliente","id_cliente",id_cliente):
                    messagebox.showinfo("Confirmación", "Cliente borrado exitosamente XML")
                    self.entry_delete_id.delete(0, 'end')
                else:
                    messagebox.showerror("Error", "Cliente no encontrado XML")
            elif tipo_archivo == "MongoDB":
                # Conecta con MongoDB y elimina el cliente
                mongo_db = archMongo.archivosMongoDB("CLIENTE")
                filtro = {"ID_CLIENTE":f"{id_cliente}"}
                if mongo_db.borrar_datos(filtro):
                    messagebox.showinfo("Confirmación", "Cliente borrado exitosamente en MongoDB")
                    self.entry_delete_id.delete(0, 'end')
                else:
                    messagebox.showerror("Error", "Cliente no encontrado en MongoDB")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def validar_string(self, char):
        """Valida que el input sea una cadena de texto."""
        return char.isalpha()

    def validar_number(self, char):
        """Valida que el input sea un número."""
        return char.isdigit()
