import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
import Archivos as Arc
import ArchivosXML as ArcXML
import ArchivosMongo as ArcM

class VentanaProducto(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Initialize the dictionary to store quantities
        self.productos_cantidad = {}

        # Configuring the layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        # Title
        lbl_titulo = ctk.CTkLabel(self, text="Gestión de Productos", font=ctk.CTkFont(size=16, weight="bold"))
        lbl_titulo.grid(row=0, column=0, columnspan=4, pady=10)

        # Product Data Section
        producto_frame = ctk.CTkFrame(self)
        producto_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        producto_frame.configure(border_width=2, corner_radius=10, border_color="gray")

        self.add_product_fields(producto_frame)

        # Action Buttons
        btn_register = ctk.CTkButton(self, text="Registrar", command=self.crear_producto, width=150)
        btn_register.grid(row=2, column=1, padx=5, pady=10, sticky="e")

        btn_show_last_products = ctk.CTkButton(self, text="Mostrar Últimos Productos", command=self.mostrar_ultimos_productos, width=150)
        btn_show_last_products.grid(row=2, column=2, padx=5, pady=10, sticky="w")

        # Product Deletion Section
        delete_frame = ctk.CTkFrame(self)
        delete_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        delete_frame.configure(border_width=2, corner_radius=10, border_color="gray")

        lbl_delete_id = ctk.CTkLabel(delete_frame, text="ID del Producto a Borrar:")
        lbl_delete_id.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_delete_id = ctk.CTkEntry(delete_frame, placeholder_text="Ingrese ID del Producto")
        self.entry_delete_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        btn_delete = ctk.CTkButton(delete_frame, text="Borrar Producto", command=self.borrar_producto, width=150)
        btn_delete.grid(row=0, column=2, padx=5, pady=5)

        # Table for showing recent products
        self.tabla = ttk.Treeview(self, columns=("Codigo", "Precio", "Inventario"), show="headings")
        self.tabla.heading("Codigo", text="Código de Producto")
        self.tabla.heading("Precio", text="Precio de Venta")
        self.tabla.heading("Inventario", text="Inventario")

        self.tabla.column("Codigo", width=120, anchor="center", stretch=tk.NO)
        self.tabla.column("Precio", width=120, anchor="center", stretch=tk.YES)
        self.tabla.column("Inventario", width=120, anchor="center", stretch=tk.YES)

        self.tabla.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    def add_product_fields(self, parent_frame):
        # Código de Producto
        lbl_codigo = ctk.CTkLabel(parent_frame, text="Código de Producto:")
        lbl_codigo.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_codProducto = ttk.Combobox(parent_frame, width=12)
        self.entry_codProducto.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Cargar valores en el ComboBox
        productos = Arc.archivos('producto').leerPrimerDatoDeCadaLinea(0)
        cantidades = Arc.archivos('producto').leerPrimerDatoDeCadaLinea(2)
        if productos and cantidades:
            self.entry_codProducto['values'] = productos
            self.productos_cantidad = dict(zip(productos, cantidades))
        else:
            self.entry_codProducto['values'] = []

        # Vincula el evento de selección del Combobox
        self.entry_codProducto.bind("<<ComboboxSelected>>", self.actualizar_cantidad)

        # Precio de Venta
        lbl_precio = ctk.CTkLabel(parent_frame, text="Precio de Venta:")
        lbl_precio.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_precio = ctk.CTkEntry(parent_frame)
        self.entry_precio.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.entry_precio.configure(validate="key", validatecommand=(self.register(self.validate_number_input), '%S'))

        # Cantidad
        lbl_cantidad = ctk.CTkLabel(parent_frame, text="Cantidad:")
        lbl_cantidad.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.cantidad_var = ctk.StringVar()
        self.lbl_cantidad = ctk.CTkLabel(parent_frame, textvariable=self.cantidad_var)
        self.lbl_cantidad.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        """Añade un combobox para seleccionar el tipo de archivo."""
        self.lbl_tipo_archivo = ctk.CTkLabel(parent_frame, text="Tipo de Archivo:")
        self.lbl_tipo_archivo.grid(row=4, column=0, padx=5, pady=5, sticky="e")

        self.combobox_tipo_archivo = ctk.CTkComboBox(parent_frame, values=["txt", "xml"])
        self.combobox_tipo_archivo.set("txt")  # Establece el valor inicial
        self.combobox_tipo_archivo.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    def actualizar_cantidad(self, event):
        # Get the selected product code
        codigo_seleccionado = self.entry_codProducto.get()
        # Find the corresponding quantity and update the Label
        cantidad_correspondiente = self.productos_cantidad.get(codigo_seleccionado, "")
        self.cantidad_var.set(cantidad_correspondiente)

    def crear_producto(self):
        try:    
            sub_elem = ['precio','inventario']
            producto_data = [self.entry_codProducto.get(), self.entry_precio.get(), self.cantidad_var.get()]
            tipo_archivo = self.combobox_tipo_archivo.get()
            
            datosM = {
                "ID_PRODUCTO" : self.entry_codProducto.get(),
                "PRECIO_VENTA" : self.entry_precio.get(),
                "INVENTARIOS" : self.cantidad_var.get()
            }
            if Arc.validar().verificar_ingreso_datos(producto_data):
                if tipo_archivo == "txt":
                    if Arc.archivos("producto").registrar_datos(producto_data):
                        messagebox.showinfo("Confirmación", "Registro exitoso")
                        self.entry_codProducto.set("")  # Clear ComboBox
                        self.entry_precio.delete(0, tk.END)
                        self.cantidad_var.set("")  # Clear Quantity Label
                        self.mostrar_ultimos_productos()  # Update table
                    else:
                        messagebox.showerror("Error", "Registro fallido")
                elif tipo_archivo == "xml":
                    if ArcXML.archivosXML("producto").registrar_datos('producto','producto', sub_elem, producto_data):
                            messagebox.showinfo("Confirmación", "Registro exitoso XML")
                            self.clear_entry_fields()
                    else:
                        messagebox.showerror("Error", "Registro fallido")
                elif tipo_archivo == "MongoDB":
                    # Conecta con MongoDB y registra los datos
                    mongo_db =ArcM.archivosMongoDB("PRODUCTOS")
                    if mongo_db.registrar_datos(datosM):
                        messagebox.showinfo("Confirmación", "Registro exitoso en MongoDB")
                        self.clear_entry_fields()
                    else:
                        messagebox.showerror("Error", "Registro fallido en MongoDB")
            else:
                messagebox.showerror("Error", "Todos los campos son requeridos")
        except Exception as e:
            messagebox.showerror("Error",f"Error al registrar producto: {e}")

    def mostrar_ultimos_productos(self):
        try:    
            for i in self.tabla.get_children():
                self.tabla.delete(i)
                
            # Obtén el tipo de archivo seleccionado desde el combobox
            tipo_archivo = self.combobox_tipo_archivo.get()
                
            if tipo_archivo == "txt":
                ultimos_productos = Arc.archivos("producto").leerUltimos()
                for producto in ultimos_productos:
                    producto_data = producto.split("-")
                    if len(producto_data) == 3:  # Ensure there are exactly 3 elements
                        self.tabla.insert("", tk.END, values=producto_data)
            elif tipo_archivo == "xml":
                # Leer los datos de clientes desde un archivo XML
                    ultimos_clientes = ArcXML.archivosXML("producto").leerxml("producto","id_producto", ["precio", "inventario"])
                    for cliente in ultimos_clientes:
                        cliente_data = [
                            cliente.get("id_producto", ""),  # Extraer el id_cliente desde el atributo
                            cliente.get("precio", ""),
                            cliente.get("inventario", ""),
                        ]
                        if any(cliente_data):  # Verifica que al menos un campo contenga datos
                            self.tabla.insert("", "end", values=cliente_data)
            elif tipo_archivo == "MongoDB":
                # Conecta con MongoDB y obtiene los datos
                datos = ArcM.archivosMongoDB("PRODUCTOS").leer_datos()
                for dato in datos:
                    cliente_data = (
                        dato.get('ID_PRODUCTOS', ''),
                        dato.get('PRECIO_VENTA', ''),
                        dato.get('INVENTARIOS', '')
                    )
                    if any(cliente_data):  # Verifica que al menos un campo contenga datos
                        self.tabla.insert("", "end", values=cliente_data)
            else:
                messagebox.showwarning("Advertencia", "Seleccione un tipo de archivo válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar los productos: {e}")

    def borrar_producto(self):
        id_producto = self.entry_delete_id.get()
        if id_producto:
            if Arc.archivos("producto").borrarDatos(id_producto):
                messagebox.showinfo("Confirmación", "Producto borrado exitosamente")
                self.entry_delete_id.delete(0, tk.END)
                self.mostrar_ultimos_productos()  # Update table
            else:
                messagebox.showerror("Error", "Error al borrar el producto")
        else:
            messagebox.showerror("Error", "Por favor ingrese un ID de producto")
            
    def clear_entry_fields(self):
        """Limpia los campos de entrada de datos."""
        self.combobox_tipo_archivo(0, ctk.END)
        self.lbl_cantidad(0, ctk.END)
        self.entry_precio(0, ctk.END)

    def validate_number_input(self, char):
        return char.isdigit()
