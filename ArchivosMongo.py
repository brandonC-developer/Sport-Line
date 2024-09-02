from pymongo import MongoClient

class archivosMongoDB:
    def __init__(self, collection_name):
        self.client = MongoClient('')  # Update with your MongoDB connection string
        self.db = self.client["SportLine"]
        self.collection = self.db[collection_name]

    def leer_datos(self, filtro=None):
        try:
            if filtro:
                datos = list(self.collection.find(filtro))
            else:
                datos = list(self.collection.find())
            return datos
        except Exception as e:
            print(f"Error al leer los datos: {e}")
            return []

    def leer_datos_seleccionados(self, campo):
        try:
            # Crear una proyección para solo incluir el campo deseado
            proyeccion = {campo: 1, "_id": 0}  # Excluir el campo '_id' si no es necesario
            datos_seleccionados = self.collection.find({}, proyeccion)
            
            # Extraer solo los valores del campo deseado y devolverlos como una lista
            return [dato[campo] for dato in datos_seleccionados if campo in dato]
        except Exception as e:
            print(f"Error al leer los datos: {e}")
            return []

    def registrar_datos(self, datos):
        try:
            result = self.collection.insert_one(datos)
            if result.inserted_id:
                print("Registro exitoso")
                return True
            else:
                return False
        except Exception as e:
            print(f"Error al registrar los datos: {e}")
            return False
        
    def borrar_datos(self, filtro):
        try:
            result = self.collection.delete_one(filtro)
            if result.deleted_count > 0:
                print("Borrado exitoso")
                return True
            else:
                print("No se encontró ningún documento para borrar")
                return False
        except Exception as e:
            print(f"Error al borrar los datos: {e}")
            return False

    def verificar_dato(self, filtro):
        try:
            return self.collection.count_documents(filtro) > 0
        except Exception as e:
            print(f"Error al verificar los datos: {e}")
            return False
