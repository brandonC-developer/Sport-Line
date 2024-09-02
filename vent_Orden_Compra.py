import customtkinter as ctk
from tkinter import messagebox, ttk
import Archivos as arch
import ArchivosXML as archXML
import ArchivosMongo as archM
import random
from tkcalendar import Calendar

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class VentanaOrdenCompra(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.configure(fg_color="gray15")  # Fondo oscuro

        # Configuración de la grilla
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        self.num_orden = random.randint(1000, 9999)

        # Título
        lbl_titulo = ctk.CTkLabel(self, text="Orden de Compra", font=ctk.CTkFont(size=20, weight="bold"))
        lbl_titulo.grid(row=0, column=0, columnspan=4, pady=10)

        # Sección de datos de la orden de compra
        orden_frame = ctk.CTkFrame(self, fg_color="gray20", corner_radius=10)
        orden_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        self.add_orden_fields(orden_frame)

        # Botones de acciones
        btn_register = ctk.CTkButton(self, text="Registrar Orden de Compra", command=self.crear_detalle_oc)
        btn_register.grid(row=2, column=1, padx=5, pady=10, sticky="e")

        # Botón para cargar datos en la tabla
        btn_cargar_datos = ctk.CTkButton(self, text="Cargar Datos en Tabla", command=self.update_treeview)
        btn_cargar_datos.grid(row=2, column=2, padx=5, pady=10, sticky="w")

        # Pestañas para mostrar tablas de orden y detalles
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Tablas para mostrar orden y detalle
        self.setup_tabs()

    def setup_tabs(self):
        """Configura las pestañas para mostrar las tablas de la orden de compra y los detalles."""
        # Crear pestaña de Orden de Compra
        self.tab_orden = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.tab_orden, text="Orden de Compra")

        self.tree_orden = ttk.Treeview(self.tab_orden, columns=("Número Orden", "Código Proveedor", "Fecha", "Estado"), show="headings")
        self.setup_treeview_orden()
        self.tree_orden.pack(fill="both", expand=True, padx=10, pady=10)

        # Crear pestaña de Detalles de Orden
        self.tab_detalle = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.tab_detalle, text="Detalle de Orden")

        self.tree_detalle = ttk.Treeview(self.tab_detalle, columns=("Número Orden", "Código Producto", "Costo", "Cantidad"), show="headings")
        self.setup_treeview_detalle()
        self.tree_detalle.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_treeview_orden(self):
        """Configura la tabla para mostrar la orden de compra."""
        self.tree_orden.heading("Número Orden", text="Número Orden")
        self.tree_orden.heading("Código Proveedor", text="Código Proveedor")
        self.tree_orden.heading("Fecha", text="Fecha")
        self.tree_orden.heading("Estado", text="Estado")

        self.tree_orden.column("Número Orden", anchor="center", width=100)
        self.tree_orden.column("Código Proveedor", anchor="center", width=120)
        self.tree_orden.column("Fecha", anchor="center", width=100)
        self.tree_orden.column("Estado", anchor="center", width=100)

    def setup_treeview_detalle(self):
        """Configura la tabla para mostrar los detalles de la orden de compra."""
        self.tree_detalle.heading("Número Orden", text="Número Orden")
        self.tree_detalle.heading("Código Producto", text="Código Producto")
        self.tree_detalle.heading("Costo", text="Costo")
        self.tree_detalle.heading("Cantidad", text="Cantidad")

        self.tree_detalle.column("Número Orden", anchor="center", width=100)
        self.tree_detalle.column("Código Producto", anchor="center", width=120)
        self.tree_detalle.column("Costo", anchor="center", width=100)
        self.tree_detalle.column("Cantidad", anchor="center", width=100)

    def add_orden_fields(self, frame):
        """Añade los campos de datos de la orden de compra."""

        # Tipo de Archivo
        lbl_estado = ctk.CTkLabel(frame, text="Tipo de Archivo:")
        lbl_estado.grid(row=3, column=2, padx=5, pady=5, sticky="e")
        self.combobox_tipo = ctk.CTkComboBox(frame, values=["txt", "xml", "MongoDB"])
        self.combobox_tipo.set("xml")  # Valor por defecto
        self.combobox_tipo.grid(row=3, column=3, padx=5, pady=5, sticky="w")

        # Cargar Datos del Combobox
        datos_combobox = self.cargarDatosCombobox()

        # Botón para cargar el formato
        btn_cargarFomato = ctk.CTkButton(frame, text="Cargar Formato", command=self.actualizar_combobox_cod_proveedor)
        btn_cargarFomato.grid(row=4, column=3, padx=5, pady=10, sticky="e")

        # Código del Proveedor
        lbl_cod_proveedor = ctk.CTkLabel(frame, text="Código del Proveedor:")
        lbl_cod_proveedor.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.combobox_cod_proveedor = ctk.CTkComboBox(frame, values=datos_combobox)
        self.combobox_cod_proveedor.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Columna 1
        lbl_numero_orden = ctk.CTkLabel(frame, text="Número de Orden:")
        lbl_numero_orden.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.lbl_num_orden = ctk.CTkLabel(frame, text=f"#{random.randint(1000, 9999)}")
        self.lbl_num_orden.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Fecha de Compra (ajustada para ser más pequeña)
        lbl_fecha_compra = ctk.CTkLabel(frame, text="Fecha de Compra:")
        lbl_fecha_compra.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.cal = Calendar(
            frame, 
            selectmode="day", 
            showweeknumbers=False,  # Oculta los números de las semanas
            font=("Arial", 8),  # Fuente más pequeña
            background="gray15", 
            foreground="white", 
            headersbackground="gray25",
            headersforeground="white",
            selectbackground="gray35",
            selectforeground="black"
        )
        self.cal.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Estado de la Compra
        lbl_tipo_archivo = ctk.CTkLabel(frame, text="Estado de Compra:")
        lbl_tipo_archivo.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.combobox_estado = ctk.CTkComboBox(frame, values=["Pendiente", "Terminada", "Cancelada"])
        self.combobox_estado.set("Terminada")  # Valor por defecto
        self.combobox_estado.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Columna 2
        # Código del Producto
        lbl_cod_producto = ctk.CTkLabel(frame, text="Código del Producto:")
        lbl_cod_producto.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_cod_producto = ctk.CTkEntry(frame, placeholder_text="Ingrese Código del Producto")
        self.entry_cod_producto.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Costo
        lbl_costo = ctk.CTkLabel(frame, text="Costo:")
        lbl_costo.grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.entry_costo = ctk.CTkEntry(frame)
        self.entry_costo.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.entry_costo.configure(validate="key", validatecommand=(self.register(self.validate_number_input), '%S'))

        # Tipo de Archivo
        lbl_estado = ctk.CTkLabel(frame, text="Tipo de Archivo:")
        lbl_estado.grid(row=3, column=2, padx=5, pady=5, sticky="e")
        self.combobox_tipo = ctk.CTkComboBox(frame, values=["txt", "xml","MongoDB"])
        self.combobox_tipo.bind("<<ComboboxSelected>>", lambda event: self.actualizar_combobox_cod_proveedor())
        self.combobox_tipo.set("xml")  # Valor por defecto
        self.combobox_tipo.grid(row=3, column=3, padx=5, pady=5, sticky="w")

        # Cantidad
        lbl_cantidad = ctk.CTkLabel(frame, text="Cantidad:")
        lbl_cantidad.grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.entry_cantidad = ctk.CTkEntry(frame)
        self.entry_cantidad.grid(row=2, column=3, padx=5, pady=5, sticky="w")
        self.entry_cantidad.configure(validate="key", validatecommand=(self.register(self.validate_number_input), '%S'))

    def setup_treeview(self):
        """Configura la tabla para mostrar los detalles de la orden de compra."""
        self.tree.heading("Número Orden", text="Número Orden")
        self.tree.heading("Código Proveedor", text="Código Proveedor")
        self.tree.heading("Costo", text="Costo")
        self.tree.heading("Cantidad", text="Cantidad")

        self.tree.column("Número Orden", anchor="center", width=100)
        self.tree.column("Código Proveedor", anchor="center", width=120)
        self.tree.column("Costo", anchor="center", width=100)
        self.tree.column("Cantidad", anchor="center", width=100)

    def cargarDatosCombobox(self):
        try:
            """Cargar nombres y códigos desde el archivo XML para el combobox."""
            tipo_archivo = self.combobox_tipo.get()
            if tipo_archivo == "xml":
                # Obtener nombres y códigos desde XML
                nombres = archXML.archivosXML("proveedor").leerDatosSeleccionados('nombre')
                codigos = archXML.archivosXML("proveedor").leerDatosSeleccionados('proveedor', 'cod_prov')
                datos_combobox = [f"{codigo} - {nombre}" for codigo, nombre in zip(codigos, nombres)]
                
            elif tipo_archivo == "MongoDB":
                # Obtener nombres y códigos desde MongoDB
                nombres = archM.archivosMongoDB("PROVEEDOR").leer_datos_seleccionados('NOMBRE')
                codigos = archM.archivosMongoDB("PROVEEDOR").leer_datos_seleccionados('COD_PROV')
                datos_combobox = [f"{codigo} - {nombre}" for codigo, nombre in zip(codigos, nombres)]
                
            elif tipo_archivo == "txt":
                # Obtener nombres y códigos desde archivo TXT
                nombres = arch.archivos("proveedor").leerUltimos()
                datos_combobox = [f"{proveedor}" for proveedor in nombres]
        
        except Exception as e:
            print(f"Error al cargar datos del combobox: {e}")
            datos_combobox = []
        
        return datos_combobox

    def actualizar_combobox_cod_proveedor(self):
        """Actualiza los datos del combobox de códigos de proveedor según el tipo de archivo seleccionado."""
        datos_combobox = self.cargarDatosCombobox()
        self.combobox_cod_proveedor.configure(values=datos_combobox)

    def crear_orden_compra(self):
        """Genera una lista con la información de la orden de compra."""
        seleccionado = self.combobox_cod_proveedor.get()
        cod_proveedor = seleccionado.split(' - ')[0]
        fecha_compra = self.cal.get_date()
        num_orden_compra = self.lbl_num_orden.cget('text')
        estado = self.combobox_estado.get()
        return [num_orden_compra, cod_proveedor, fecha_compra, estado]

    def crear_detalle_oc(self):
        """Registra el detalle de la orden de compra y actualiza la tabla."""
        num_oc = self.lbl_num_orden.cget('text')
        cod_proveedor = self.combobox_cod_proveedor.get()
        fecha = self.cal.get_date()
        estado = self.combobox_estado.get()
        datosOC = [num_oc, cod_proveedor, fecha, estado]
        sub_elementoOC =  ['codigoProveedor', 'fecha', 'aplicada']
        
        tipo_archivo = self.combobox_tipo.get()
        datosDetalle = [num_oc, self.entry_cod_producto.get(), self.entry_costo.get(), self.entry_cantidad.get()]
        sub_elementoDt = ["codigoProducto","costo","cantidad"]

        detalle_factura = {
            "NUM_FACTURA": num_oc,
            "COD_PRODUCTO": self.entry_cod_producto.get(),
            "CANTIDAD": self.entry_cantidad.get()
            }
        detalle_oc = {
            "NUM_OC" : num_oc,
            "COD_PRODUCTO" : self.entry_cod_producto.get(),
            "COSTO" :  self.entry_costo.get(),
            "CANTIDAD" : self.entry_cantidad.get()
        }
        orden_compra = {
            "NUM_OC" : num_oc,
            "COD_PROVEEDOR" : cod_proveedor,
            "FECHA_OC" : fecha,
            "APLICADA" :estado
        }
        
        # Verificar que todos los campos requeridos estén llenos
        if arch.validar().verificar_ingreso_datos(datosOC) and arch.validar().verificar_ingreso_datos(datosDetalle):
            if tipo_archivo == "txt":
                if arch.archivos("orden_compra").registrar_datos(self.crear_orden_compra()) and arch.archivos("detalle_oc").registrar_datos(datosDetalle):
                    messagebox.showinfo("Confirmación", "Registro exitoso en TXT")
                else:
                    messagebox.showerror("Error", "Registro fallido en TXT")
                    
            elif tipo_archivo == "xml":
                if archXML.archivosXML("orden_compra").registrar_datos('orden', 'id_orden', sub_elementoOC, datosOC) and archXML.archivosXML("detalle_oc").registrar_datos('detalle', 'id_orden', sub_elementoDt, datosDetalle):
                    messagebox.showinfo("Confirmación", "Registro exitoso en XML")
                else:
                    messagebox.showerror("Error", "Registro fallido en XML")
                    
            elif tipo_archivo == "MongoDB":
                    # Conecta con MongoDB y registra los datos
                    mongo_db_DOC = archM.archivosMongoDB("DETALLE_OC")
                    nomgo_ordenCompra = archM.archivosMongoDB("ORDEN_COMPRA")
                    if mongo_db_DOC.registrar_datos(detalle_oc) and nomgo_ordenCompra.registrar_datos(orden_compra):
                        messagebox.showinfo("Confirmación", "Registro exitoso en MongoDB")
                        self.clear_entry_fields()
                    else:
                        messagebox.showerror("Error", "Registro fallido en MongoDB")
        else:
            messagebox.showerror("Error", "Todos los campos son requeridos")

    def update_treeview(self):
        """Actualiza ambos Treeviews con los detalles de la orden de compra y la orden en sí."""
        try:
            # Limpiar ambos Treeviews
            for item in self.tree_orden.get_children():
                self.tree_orden.delete(item)
            for item in self.tree_detalle.get_children():
                self.tree_detalle.delete(item)

            tipo_archivo = self.combobox_tipo.get()

            if tipo_archivo == "txt":
                # Leer datos desde archivo de texto
                detalles = arch.archivos("orden_compra").leerUltimos()
                for detalle in detalles:
                    detalle_data = detalle.split("-")
                    if len(detalle_data) == 4:
                        self.tree_orden.insert("", "end", values=detalle_data)
                # Leer detalles de orden desde archivo de texto
                detalles_oc = arch.archivos("detalle_oc").leerUltimos()
                for detalle in detalles_oc:
                    detalle_data = detalle.split("-")
                    if len(detalle_data) == 4:
                        self.tree_detalle.insert("", "end", values=detalle_data)
            elif tipo_archivo == "xml":
                # Leer datos desde archivo XML
                detalles = archXML.archivosXML("orden_compra").leerxml("orden", "id_orden", ["codigoProveedor", "fecha", "aplicada"])
                for detalle in detalles:
                    detalle_data = [
                        detalle.get("id_orden", ""),
                        detalle.get("codigoProveedor", ""),
                        detalle.get("fecha", ""),
                        detalle.get("aplicada", "")
                    ]
                    if any(detalle_data):
                        self.tree_orden.insert("", "end", values=detalle_data)

                # Leer detalles de orden desde archivo XML
                detalles_oc = archXML.archivosXML("detalle_oc").leerxml("detalle", "id_orden", ["codigoProducto", "costo", "cantidad"])
                for detalle in detalles_oc:
                    detalle_data = [
                        detalle.get("id_orden", ""),
                        detalle.get("codigoProducto", ""),
                        detalle.get("costo", ""),
                        detalle.get("cantidad", "")
                    ]
                    if any(detalle_data):
                        self.tree_detalle.insert("", "end", values=detalle_data)
                        
            elif tipo_archivo == "MongoDB":
                # Conecta con MongoDB y obtiene los datos
                datos_oc = archM.archivosMongoDB("ORDEN_COMPRA").leer_datos()
                for dato in datos_oc:
                    orden_compra = (
                        dato.get('NUM_OC', ''),
                        dato.get('COD_PROVEEDOR', ''),
                        dato.get('FECHA_OC', ''),
                        dato.get('APLICADA', '')
                    )
                    if any(orden_compra):  # Verifica que al menos un campo contenga datos
                        self.tree_orden.insert("", "end", values=orden_compra)
                        
                detalle_oc = archM.archivosMongoDB("DETALLE_OC").leer_datos()
                for dato in detalle_oc:
                    detalle_orden_compra = (
                        dato.get('NUM_OC', ''),
                        dato.get('COD_PRODUCTO', ''),
                        dato.get('COSTO',''),
                        dato.get('CANTIDAD', '')
                    )
                    if any(detalle_orden_compra):  # Verifica que al menos un campo contenga datos
                        self.tree_detalle.insert("", "end", values=detalle_orden_compra)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_entry_fields(self):
        """Limpia los campos de entrada de datos."""
        self.entry_cod_producto.delete(0, ctk.END)
        self.entry_costo.delete(0, ctk.END)
        self.entry_cantidad.delete(0, ctk.END)

    def validate_number_input(self, char):
        """Valida que el input sea un número."""
        return char.isdigit()

