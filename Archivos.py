import xml.etree.ElementTree as ET

class archivos:
    def __init__(self,nomArchivo):
        self._nomArchivo = nomArchivo
        
    def leerUltimos(self):
        try:
            with open(f"Archivos/{self._nomArchivo}.txt", "r") as arc1:
                lineas = arc1.readlines()
                return [li.strip() for li in lineas]  
        except Exception as e:
            print(f"Error al leer el archivo {e}")
            return []
        
    def leerPrimerDatoDeCadaLinea(self, dato):
        try:
            with open(f"Archivos/{self._nomArchivo}.txt", "r") as arc1:
                primeros_datos = []
                lineas = arc1.readlines()
                for li in lineas:
                    if li.strip():
                        primeros_datos.append(li.strip().split("-")[dato])
                return primeros_datos
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return []
    def precionProducto(self, id,dato):  
        with open(f"Archivos/{self._nomArchivo}.txt", "r") as arc1:
            lineas = arc1.readlines()
            for li in lineas:
                if li.startswith(id):
                    return li.strip().split("-")[int(dato)]
            return None
    def registrar_datos(self, datos):
        try:
            linea = '-'.join(map(str, datos)) + '\n'
            with open(f"Archivos/{self._nomArchivo}.txt", 'a') as archivo:
                archivo.write(linea)
            archivo.close()
            print("Registro exitoso")
            return True
        except Exception as e:
            print(F"Error al leer el archivo {e}")
            
    def borrarDatos(self, id):
        try:
            with open(f"Archivos/{self._nomArchivo}.txt", "r") as arc1:
                lineas = arc1.readlines()
            with open(f"Archivos/{self._nomArchivo}.txt", "w") as arc1:
                for linea in lineas:
                    if not linea.startswith(id):
                        arc1.write(linea)
            return True
        except Exception as e:
            print(f"Error al borrar los datos: {e}")
            return False
                    
    def verificarCliente(self, id):
        with open(f"Archivos/{self._nomArchivo}.txt", "r") as arc1:
            lineas = arc1.readlines()
            for i in range(len(lineas)):
                partes = lineas[i].strip().split("-")
                if partes[0] == id:
                    return True
            return False
        
class validar:
    def __init__(self):
        pass
    
    def verificar_ingreso_datos(self, datos):
        return all(datos)
        