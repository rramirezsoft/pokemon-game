import random


class Combat:
    def __init__(self, player, enemy_pokemon):
        """Inicializa el combate con el jugador y el Pokémon enemigo."""
        self.player = player
        self.enemy_pokemon = enemy_pokemon
        self.current_pokemon = next((pokemon for pokemon in self.player.pokemons if not pokemon.is_fainted()), None)

    def attempt_escape(self):
        """Lógica para intentar escapar del combate."""
        player_speed = self.current_pokemon.current_stats["speed"]
        enemy_speed = self.enemy_pokemon.current_stats["speed"]

        escape_chance = ((player_speed * 128) / enemy_speed) + 30
        random_number = random.randint(0, 255)

        print(f"velocidad de mi pokemon {player_speed}\nVelocidad del pokemon enemigo {enemy_speed}"
              f"\nProbabilidad de escapar {escape_chance}\nNumero aleatorio {random_number}")

        return escape_chance >= random_number

