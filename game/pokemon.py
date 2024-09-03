import json


class Pokemon:
    def __init__(self, name, types, stats, moves, height, weight):
        self.name = name
        self.types = types
        self.stats = stats
        self.moves = moves
        self.height = height / 10.0  # Decímetros a metros
        self.weight = weight / 10.0  # Hectogramos a kilogramos

    def get_stats(self):
        return self.stats

    def get_moves(self):
        return self.moves

    def get_types(self):
        return self.types

    def get_height(self):
        return self.height

    def get_weight(self):
        return self.weight


# Función para cargar los datos desde el archivo JSON y crear objetos Pokémon
def load_pokemon_from_json(filename="pokemon_data.json"):
    with open(filename, 'r') as file:
        pokemon_data = json.load(file)

    # Crear una lista de objetos Pokémon desde los datos del JSON
    pokemon_list = []
    for pokemon in pokemon_data:
        p = Pokemon(
            name=pokemon['name'],
            types=pokemon['types'],
            stats=pokemon['stats'],
            moves=pokemon['moves'],
            height=pokemon['physical_attributes']['height'],
            weight=pokemon['physical_attributes']['weight']
        )
        pokemon_list.append(p)

    return pokemon_list


# Ejemplo de uso
if __name__ == "__main__":
    pokemons = load_pokemon_from_json()  # Cargar todos los Pokémon del archivo JSON

    # Acceder a los datos del primer Pokémon
    first_pokemon = pokemons[0]
    print(f"Nombre: {first_pokemon.name}")
    print(f"Tipos: {first_pokemon.get_types()}")
    print(f"Estadísticas: {first_pokemon.get_stats()}")
    print(f"Movimientos: {first_pokemon.get_moves()}")
    print(f"Altura:  {first_pokemon.get_height()} metros")
    print(f"Weight: {first_pokemon.get_weight()} kilogramos")
