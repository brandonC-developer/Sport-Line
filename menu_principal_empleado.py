import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import Archivos as Arc
import random
import datetime

ctk.set_appearance_mode("Dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

class InvoiceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Registrar Factura")
        self.geometry("600x600")

        # Initialize GUI
        self.create_widgets()
        self.mainloop()

    def create_widgets(self):
        # File Format Selection
        ctk.CTkLabel(self, text="Formato de Archivo:").grid(row=0, column=0, padx=5, pady=5)
        self.filetype_combobox = ctk.CTkComboBox(self, values=["TXT", "XML"])
        self.filetype_combobox.set("TXT")
        self.filetype_combobox.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkButton(self, text="Cambiar Formato", command=self.change_format).grid(row=0, column=2, padx=5, pady=5)

        # Invoice Header Section
        ctk.CTkLabel(self, text="Numero de Factura:").grid(row=1, column=0, padx=5, pady=5)
        self.lbl_numFactura = ctk.CTkLabel(self, text=f"{random.randint(1000, 999999999)}")
        self.lbl_numFactura.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(self, text="ID Cliente:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_idCliente = ctk.CTkEntry(self, width=150)
        self.entry_idCliente.grid(row=2, column=1, padx=5, pady=5)
        self.entry_idCliente.bind("<KeyRelease>", self.validate_number_input)

        ctk.CTkButton(self, text="Verificar", command=self.verify_client).grid(row=2, column=2, padx=5, pady=5)

        ctk.CTkLabel(self, text="Fecha de Factura:").grid(row=3, column=0, padx=5, pady=5)
        self.lbl_fecha = ctk.CTkLabel(self, text=f"{datetime.datetime.today().strftime('%d/%m/%Y %H:%M')}")
        self.lbl_fecha.grid(row=3, column=1, padx=5, pady=5)

        # Product Details Section
        self.product_rows = 4
        self.product_entries = []
        self.add_product_fields()

        ctk.CTkButton(self, text="Agregar Producto", command=self.add_product).grid(row=4, column=4, padx=5, pady=5)

        # Continue Button
        ctk.CTkButton(self, text="Continuar", command=self.preview_invoice, width=120).grid(row=7, column=2, pady=20)

    def add_product_fields(self):
        ctk.CTkLabel(self, text="Codigo de Producto:").grid(row=self.product_rows, column=0, padx=5, pady=5, sticky='w')
        codProducto = ctk.CTkComboBox(self, width=150)
        codProducto.grid(row=self.product_rows, column=1, padx=5, pady=5, sticky='w')
        codProducto.bind("<KeyRelease>", self.validate_number_input)

        productos = Arc.archivos('producto').leerPrimerDatoDeCadaLinea(0)
        codProducto.configure(values=productos)
        codProducto.set(productos[0] if productos else '')

        ctk.CTkLabel(self, text="Cantidad:").grid(row=self.product_rows, column=2, pady=5, sticky='w')
        cantidad = ctk.CTkComboBox(self, values=[str(i) for i in range(1, 11)], width=150)
        cantidad.grid(row=self.product_rows, column=3,pady=5,sticky='w')
        cantidad.set("1")

        self.product_entries.append((codProducto, cantidad))

    def add_product(self):
        self.product_rows += 1
        self.add_product_fields()

    def verify_client(self):
        formato = self.filetype_combobox.get().lower()
        cliente_existe = Arc.archivos("cliente").verificarCliente(self.entry_idCliente.get())
        if cliente_existe:
            messagebox.showinfo("Confirmacion", f"El cliente {self.entry_idCliente.get()} existe")
            for codProducto, cantidad in self.product_entries:
                codProducto.configure(state="normal")
                cantidad.configure(state="normal")
        else:
            messagebox.showwarning("Error", "El cliente no existe")

    def preview_invoice(self):
        # Create a new Toplevel window for invoice preview
        preview_window = ctk.CTkToplevel(self)
        preview_window.title("Vista Previa de Factura")
        preview_window.geometry("600x400")

        # Invoice Information
        ctk.CTkLabel(preview_window, text="Número de Factura:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=25, pady=5, sticky='w')
        ctk.CTkLabel(preview_window, text=self.lbl_numFactura.cget("text")).grid(row=0, column=1, padx=25, pady=5, sticky='w')

        ctk.CTkLabel(preview_window, text="ID Cliente:", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=25, pady=5, sticky='w')
        ctk.CTkLabel(preview_window, text=self.entry_idCliente.get()).grid(row=1, column=1, padx=25, pady=5, sticky='w')

        ctk.CTkLabel(preview_window, text="Fecha de Factura:", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=25, pady=5, sticky='w')
        ctk.CTkLabel(preview_window, text=self.lbl_fecha.cget("text")).grid(row=2, column=1, padx=25, pady=5, sticky='w')

        # Product Details
        ctk.CTkLabel(preview_window, text="Productos:", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=25, pady=5, sticky='w')
        ctk.CTkLabel(preview_window, text="Cantidad", font=("Arial", 10, "bold")).grid(row=3, column=1, padx=10, pady=5, sticky='w')
        ctk.CTkLabel(preview_window, text="Precio", font=("Arial", 10, "bold")).grid(row=3, column=2, padx=10, pady=5, sticky='w')
        ctk.CTkLabel(preview_window, text="Subtotal", font=("Arial", 10, "bold")).grid(row=3, column=3, padx=10, pady=5, sticky='w')

        # Show Products and Calculate Total
        total = 0
        for index, (codProducto, cantidad) in enumerate(self.product_entries):
            producto = codProducto.get()
            cantidad_val = int(cantidad.get())
            precio = float(Arc.archivos('producto').precionProducto(producto, 1))
            subtotal = precio * cantidad_val
            total += subtotal

            ctk.CTkLabel(preview_window, text=f"{index + 1}. {producto}", font=("Arial", 10)).grid(row=4 + index, column=0, padx=25, pady=5, sticky='w')
            ctk.CTkLabel(preview_window, text=f"{cantidad_val}", font=("Arial", 10)).grid(row=4 + index, column=1, padx=5, pady=5, sticky='w')
            ctk.CTkLabel(preview_window, text=f"{precio:.2f}", font=("Arial", 10)).grid(row=4 + index, column=2, padx=10, pady=5, sticky='w')
            ctk.CTkLabel(preview_window, text=f"{subtotal:.2f}", font=("Arial", 10)).grid(row=4 + index, column=3, padx=10, pady=5, sticky='w')

        # Total Amount
        ctk.CTkLabel(preview_window, text="Total:", font=("Arial", 10, "bold")).grid(row=4 + len(self.product_entries), column=0, padx=25, pady=5, sticky='w')
        ctk.CTkLabel(preview_window, text=f"${total:.2f}", font=("Arial", 10, "bold")).grid(row=4 + len(self.product_entries), column=1, padx=10, pady=5, sticky='w')

        # Complete Sale Button
        ctk.CTkButton(preview_window, text="Venta Realizada", command=self.save_invoice).grid(row=5 + len(self.product_entries), column=0, columnspan=4, pady=20)

    def save_invoice(self):
        formato = self.filetype_combobox.get().lower()
        encab_factura = [
            self.lbl_numFactura.cget("text"),
            self.entry_idCliente.get(),
            self.lbl_fecha.cget("text"),
            self.total
        ]

        detalle_factura = []
        for codProducto, cantidad in self.product_entries:
            detalle_factura.append([
                self.lbl_numFactura.cget("text"),
                codProducto.get(),
                cantidad.get()
            ])

        if Arc.archivos(f"encab_factura.{formato}").registrar_datos(encab_factura) and Arc.archivos(f"detalle_factura.{formato}").registrar_datos(detalle_factura):
            messagebox.showinfo("Confirmacion", "Registro exitoso")
            self.clear_entries()
        else:
            messagebox.showwarning("Error", "Registro fallido")

    def clear_entries(self):
        self.entry_idCliente.delete(0, ctk.END)
        for codProducto, cantidad in self.product_entries:
            codProducto.set('')
            cantidad.set('1')

    def validate_number_input(self, event):
        if not event.char.isdigit():
            event.widget.delete(len(event.widget.get())-1, ctk.END)

    def change_format(self):
        formato = self.filetype_combobox.get()
        messagebox.showinfo("Formato Cambiado", f"Formato cambiado a {formato}")
