import customtkinter as ctk
from tkinter import messagebox, ttk
import Archivos as Arc
import ArchivosXML as ArcXML
import ArchivosMongo as ArcM

# Configuración global del tema y apariencia
ctk.set_appearance_mode("Dark")  # Opciones: "Dark", "Light"
ctk.set_default_color_theme("blue")  # Opciones: "blue", "green", "dark-blue"

class VentanaProveedor(ctk.CTkFrame):
    def __init__(self, parent,tipo_archivo):
        super().__init__(parent)
        self.tipo_archivo = tipo_archivo
        self.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.configure(fg_color="gray15")  # Fondo oscuro

        # Configuración de la grilla
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        # Título
        lbl_titulo = ctk.CTkLabel(self, text="Registro de Proveedor", font=ctk.CTkFont(size=20, weight="bold"))
        lbl_titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Sección de datos del proveedor
        proveedor_frame = ctk.CTkFrame(self, fg_color="gray20", corner_radius=10)
        proveedor_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        self.add_tipo_archivo_combobox(proveedor_frame)  # Agrega el combobox
        self.add_proveedor_fields(proveedor_frame)

        # Botones de acciones
        btn_register = ctk.CTkButton(self, text="Registrar", command=self.crearProveedor)
        btn_register.grid(row=2, column=0, padx=5, pady=10, sticky="e")

        btn_show_last_providers = ctk.CTkButton(self, text="Mostrar Últimos Proveedores", command=self.mostrar_ultimos_proveedores)
        btn_show_last_providers.grid(row=2, column=1, padx=5, pady=10, sticky="w")

        # Sección de eliminación de proveedor
        delete_frame = ctk.CTkFrame(self, fg_color="gray20", corner_radius=10)
        delete_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.add_delete_fields(delete_frame)

        # Tabla para mostrar últimos proveedores
        self.tree = ttk.Treeview(self, columns=("ID", "Nombre"), show="headings")
        self.setup_treeview()
        self.tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.mainloop()

    def add_tipo_archivo_combobox(self, frame):
        """Añade un combobox para seleccionar el tipo de archivo."""
        self.lbl_tipo_archivo = ctk.CTkLabel(frame, text="Tipo de Archivo:")
        self.lbl_tipo_archivo.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.combobox_tipo_archivo = ctk.CTkComboBox(frame, values=["txt", "xml","MongoDB"])
        self.combobox_tipo_archivo.set(self.tipo_archivo)  # Establece el valor inicial
        self.combobox_tipo_archivo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    
    def add_proveedor_fields(self, frame):
        """Añade los campos de datos del proveedor."""
        lbl_codigo = ctk.CTkLabel(frame, text="Código de proveedor:")
        lbl_codigo.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_codProveedor = ctk.CTkEntry(frame)
        self.entry_codProveedor.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.entry_codProveedor.configure(validate="key", validatecommand=(self.register, '%S'))

        lbl_nombre = ctk.CTkLabel(frame, text="Nombre:")
        lbl_nombre.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_nombreProveedor = ctk.CTkEntry(frame)
        self.entry_nombreProveedor.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.entry_nombreProveedor.configure(validate="key", validatecommand=(self.register, '%S'))

    def add_delete_fields(self, frame):
        """Añade los campos de eliminación de proveedor."""
        lbl_delete_id = ctk.CTkLabel(frame, text="ID del Proveedor a Borrar:")
        lbl_delete_id.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_delete_id = ctk.CTkEntry(frame, placeholder_text="Ingrese ID")
        self.entry_delete_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        btn_delete = ctk.CTkButton(frame, text="Borrar Proveedor", command=self.borrar_proveedor)
        btn_delete.grid(row=0, column=2, padx=5, pady=5)

    def setup_treeview(self):
        """Configura la tabla para mostrar los últimos proveedores."""
        self.tree.heading("ID", text="Código")
        self.tree.heading("Nombre", text="Nombre")

        self.tree.column("ID", anchor="center", width=100)
        self.tree.column("Nombre", anchor="center", width=200)

    def crearProveedor(self):
        try:
            
            datosm = {
            "COD_PROV": self.entry_codProveedor.get(),
            "NOMBRE": self.entry_nombreProveedor.get()
            }
            
            
            """Registra un nuevo cliente."""
            sub_elem = ['nombre']
            datos = [self.entry_codProveedor.get(),self.entry_nombreProveedor.get()]
            tipo_archivo = self.combobox_tipo_archivo.get()  # Obtiene el tipo de archivo seleccionado
            if Arc.validar().verificar_ingreso_datos(datos):
                if tipo_archivo == "txt":
                    if Arc.archivos("cliente").registrar_datos(datos):
                        messagebox.showinfo("Confirmación", "Registro exitoso TXT")
                        self.clear_entry_fields()
                    else:
                        messagebox.showerror("Error", "Registro fallido")
                elif tipo_archivo == "xml":
                    if ArcXML.archivosXML("proveedor").registrar_datos('proveedor','cod_prov', sub_elem, datos):
                        messagebox.showinfo("Confirmación", "Registro exitoso XML")
                        self.clear_entry_fields()
                    else:
                        messagebox.showerror("Error", "Registro fallido")
                elif tipo_archivo == "MongoDB":
                    # Conecta con MongoDB y registra los datos
                    mongo_db =ArcM.archivosMongoDB("PROVEEDOR")
                    if mongo_db.registrar_datos(datosm):
                        messagebox.showinfo("Confirmación", "Registro exitoso en MongoDB")
                        self.clear_entry_fields()
                    else:
                        messagebox.showerror("Error", "Registro fallido en MongoDB")
            else:
                messagebox.showerror("Error", "Todos los campos son requeridos")
        except Exception as e:
            messagebox.showerror("Error",f"Error al registrar proveedor: {e}")

    def clear_entry_fields(self):
        """Limpia los campos de entrada de datos."""
        self.entry_codProveedor.delete(0, ctk.END)
        self.entry_nombreProveedor.delete(0, ctk.END)

    def mostrar_ultimos_proveedores(self):
        try:
            """Muestra los últimos proveedores registrados."""
            # Limpiar el Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            tipo_archivo = self.combobox_tipo_archivo.get()
            
            if tipo_archivo == "txt":
                ultimos_proveedores = Arc.archivos("proveedor").leerUltimos()
                for proveedor in ultimos_proveedores:
                    proveedor_data = proveedor.split("-")
                    if len(proveedor_data) == 2:
                        self.tree.insert("", "end", values=proveedor_data)
                        
            elif tipo_archivo == "xml":
                # Leer los datos de proveedores desde un archivo XML
                ultimos_proveedores = ArcXML.archivosXML("proveedor").leerxml("proveedor",'cod_prov', ["nombre"])
                for proveedor in ultimos_proveedores:
                    proveedor_data = [
                        proveedor.get("cod_prov", ""),  # Extrae el ID del proveedor
                        proveedor.get("nombre", "")  # Extrae el nombre del proveedor
                    ]
                    if any(proveedor_data):  # Verifica que al menos un campo contenga datos
                        self.tree.insert("", "end", values=proveedor_data)
                        
            elif tipo_archivo == "MongoDB":
                # Conecta con MongoDB y obtiene los datos
                datos = ArcM.archivosMongoDB("PROVEEDOR").leer_datos()
                for dato in datos:
                    cliente_data = (
                        dato.get('COD_PROV', ''),
                        dato.get('NOMBRE', '')
                    )
                    if any(cliente_data):  # Verifica que al menos un campo contenga datos
                        self.tree.insert("", "end", values=cliente_data)
            
            else:
                messagebox.showwarning("Advertencia", "Seleccione un tipo de archivo válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar los proveedores: {e}")
    def borrar_proveedor(self):
        try:
            """Elimina un proveedor registrado."""
            id_proveedor = self.entry_delete_id.get()
            tipo_archivo = self.combobox_tipo_archivo.get()
            if tipo_archivo == "txt":
                if Arc.archivos("proveedor").borrarDatos(id_proveedor):
                    messagebox.showinfo("Confirmación", "Proveedor borrado exitosamente")
                    self.entry_delete_id.delete(0, ctk.END)
                else:
                    messagebox.showerror("Error", "Error al borrar el proveedor")
            elif tipo_archivo == "xml":
                    if ArcXML.archivosXML("proveedor").borrarDatos("proveedor","cod_prov",id_proveedor):
                        messagebox.showinfo("Confirmación", "Proveedor borrado exitosamente XML")
                        self.entry_delete_id.delete(0, 'end')
                    else:
                        messagebox.showerror("Error", "Proveedor no encontrado XML")
            elif tipo_archivo == "MongoDB":
                # Conecta con MongoDB y elimina el cliente
                mongo_db = ArcM.archivosMongoDB("PROVEEDOR")
                filtro = {"COD_PROV":f"{id_proveedor}"}
                if mongo_db.borrar_datos(filtro):
                    messagebox.showinfo("Confirmación", "Proveedor borrado exitosamente en MongoDB")
                    self.entry_delete_id.delete(0, 'end')
                else:
                    messagebox.showerror("Error", "Proveedor no encontrado en MongoDB")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def validar_string(self, char):
        """Valida que el input sea una cadena de texto."""
        return char.isalpha()

    def validar_number(self, char):
        """Valida que el input sea un número."""
        return char.isdigit()