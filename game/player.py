
class Bag:
    def __init__(self):
        self.items = {
            "potions": 0,
            "pokeballs": 0
        }

    def add_item(self, item_type, amount):
        if item_type in self.items:
            self.items[item_type] += amount
        else:
            self.items[item_type] = amount

    def use_item(self, item_type, amount):
        if item_type in self.items and self.items[item_type] >= amount:
            self.items[item_type] -= amount
            return True
        return False

    def get_item_amount(self, item_type):
        """Devuelve la cantidad de un artículo en la bolsa."""
        return self.items.get(item_type, 0)

    def __str__(self):
        return str(self.items)


class Player:
    def __init__(self, name):
        self.name = name
        self.bag = Bag()
        self.pokemons = []
        self.badges = []
        self.money = 0

    def get_starter(self, pokemon):
        """Elige el pokemon inicial y lo añade a la lista de Pokémon del jugador."""
        self.pokemons.append(pokemon)
        print(f"¡Has elegido a {pokemon.name} como tu Pokémon inicial!")

    def capture_pokemon(self, pokemon):
        """Intenta capturar un nuevo Pokémon."""
        if self.bag.get_item_amount('pokeballs') > 0:
            self.bag.use_item('pokeballs', 1)
            self.pokemons.append(pokemon)
            return True
        else:
            print("No tienes Poké Balls suficientes.")
            return False

    def use_item(self, item):
        """Usa un artículo de la bolsa del jugador."""
        if self.bag.use_item(item, 1):
            print(f"Has usado {item}.")
        else:
            print(f"No tienes {item} en la bolsa.")

    def heal_pokemon(self):
        """Cura todos los Pokémon del jugador."""
        for pokemon in self.pokemons:
            pokemon.status = None  # Restablece el estado del Pokémon a 'None'
        print("Todos tus Pokémon han sido curados.")

    def get_badge(self, badge_name):
        """Añade una insignia al jugador."""
        if badge_name not in self.badges:
            self.badges.append(badge_name)
            print(f"¡Has obtenido la insignia: {badge_name}!")
        else:
            print(f"Ya tienes la insignia: {badge_name}")

    def earn_money(self, amount):
        """Incrementa la cantidad de dinero del jugador."""
        self.money += amount
        print(f"Has ganado {amount} monedas. Dinero actual: {self.money}.")

    def spend_money(self, amount):
        """Decrementa la cantidad de dinero del jugador si es posible."""
        if self.money >= amount:
            self.money -= amount
            print(f"Has gastado {amount} monedas. Dinero restante: {self.money}.")
            return True
        else:
            print("No tienes suficiente dinero.")
            return False

    def __str__(self):
        """Devuelve una representación en cadena del jugador."""
        return (f"Jugador: {self.name}\n"
                f"Dinero: {self.money}\n"
                f"Bolsa: {self.bag}\n"
                f"Insignias: {', '.join(self.badges) if self.badges else 'Ninguna'}\n"
                f"Pokémon: {', '.join(pokemon.name for pokemon in self.pokemons) if self.pokemons else 'Ninguno'}")

