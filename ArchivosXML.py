import xml.etree.ElementTree as ET

class archivosXML:
    def __init__(self, nomArchivo):
        self._nomArchivo = f"XML/{nomArchivo}.xml"
        
    def leerxml(self, tipo,atributoElemento, subElementos):
        try:
            # Cargar y parsear el archivo XML
            tree = ET.parse(self._nomArchivo)
            root = tree.getroot()

            # Encontrar todos los elementos del tipo especificado
            elementos = root.findall(f'.//{tipo}')

            # Crear una lista para almacenar los datos
            datos = []

            # Iterar sobre los elementos
            for element in elementos:
                # Extraer el id_cliente desde el atributo y los demás subelementos
                dato = {
                    f"{atributoElemento}": element.get(f"{atributoElemento}", ""),  # Extraer el id_cliente desde el atributo
                    **{sub: element.find(sub).text if element.find(sub) is not None else '' for sub in subElementos}
                }
                datos.append(dato)

            return datos
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return []

    def leerDatosSeleccionados(self, nombre_tag, nombre_atributo=None):
        try:
            # Parsear el archivo XML
            tree = ET.parse(f'{self._nomArchivo}')
            root = tree.getroot()
            
            # Inicializar una lista para almacenar los datos seleccionados
            datos_seleccionados = []

            # Iterar sobre cada elemento en la raíz
            for elem in root.findall(f'.//{nombre_tag}'):
                if nombre_atributo:  # Si se especifica un atributo, lo recupera
                    dato = elem.get(nombre_atributo)
                    if dato:
                        datos_seleccionados.append(dato)
                else:  # De lo contrario, recupera el contenido de texto
                    dato = elem.text.strip() if elem.text else ""
                    if dato:
                        datos_seleccionados.append(dato)

            return datos_seleccionados
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return []

    def precioProducto(self, id):
        try:
            tree = ET.parse(self._nomArchivo)
            root = tree.getroot()
            for elem in root:
                partes = elem.text
                if partes[0] == id:
                    return elem[0][0].text
            return None
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return None

    def registrar_datos(self, titulo,sub_titulo,sub_elem, datos):
        try:
            tree = ET.parse(self._nomArchivo)
            root = tree.getroot()

            nuevo_cliente = ET.Element(f'{titulo}')
            nuevo_cliente.set(f'{sub_titulo}', str(datos[0]))

            # Crear subelementos dinámicamente
            for i, elem in enumerate(sub_elem):
                x = ET.SubElement(nuevo_cliente, elem)
                x.text = datos[i + 1]  # datos[i+1] porque datos[0] es id_cliente

            root.append(nuevo_cliente)
            tree.write(self._nomArchivo)

            print("Registro exitoso")
            return True
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return False
        
    
    def borrarDatos(self, elem_name, atrib_name, id_value):
        try:
            # Cargar el archivo XML
            tree = ET.parse(self._nomArchivo)
            root = tree.getroot()

            # Buscar y eliminar el elemento <elem_name> que coincida con el atributo y su valor
            for elem in root.findall(f'{elem_name}'):
                if elem.get(atrib_name) == id_value:
                    # Si el atributo coincide con el valor, eliminamos el elemento
                    root.remove(elem)
                    tree.write(self._nomArchivo)
                    return True

            return False  # Si no se encontró ningún elemento para eliminar
        except Exception as e:
            print(f"Error al borrar los datos: {e}")
            return False

    def verificarCliente(self, id):
        try:
            tree = ET.parse(self._nomArchivo)
            root = tree.getroot()
            for elem in root:
                partes = elem.text
                if partes[0] == id:
                    return True
            return False
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return False
