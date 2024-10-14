from pymongo import MongoClient

# URI de conexión a MongoDB Atlas
MONGO_URI = ("mongodb+srv://rramirezsoft:XUiJVIQgtiCzay57@pokedatabase.v35fd.mongodb.net/?retryWrites=true&w=majority"
             "&appName=PokeDataBase")


# Función para conectar a la base de datos
def get_db():
    client = MongoClient(MONGO_URI)
    db = client.PokeDataBase  # Nombre de tu base de datos en Atlas
    return db


# Ejemplo de uso para obtener una colección de jugadores
def get_players_collection():
    db = get_db()
    return db.players  # Nombre de la colección
