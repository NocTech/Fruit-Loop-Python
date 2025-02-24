import random

class Grid:
    """Representerar spelplanen. Du kan ändra standardstorleken och tecknen för olika rutor. """
    width = 36
    height = 12
    empty = "."  # Tecken för en tom ruta
    wall = "■"   # Tecken för en ogenomtränglig vägg
    trap = "X"   # Tecken för en fälla
    enemy = "E"  # Tecken för en fiende
    bomb = "B"  # Tecken för en bomb

    def __init__(self):
        """Skapa ett objekt av klassen Grid"""
        # Spelplanen lagras i en lista av listor. Vi använder "list comprehension" för att sätta tecknet för "empty" på varje plats på spelplanen.
        self.data = [[self.empty for y in range(self.width)] for z in range(
            self.height)]
        self.enemies = []
        self.bombs = {}  # Dictionary för att lagra bomber och deras nedräkning

    def get(self, x, y):
        """Hämta det som finns på en viss position"""
        return self.data[y][x]

    def set(self, x, y, value):
        """Ändra vad som finns på en viss position"""
        self.data[y][x] = value

    def set_player(self, player):
        self.player = player

    def clear(self, x, y):
        """Ta bort item från position"""
        self.set(x, y, self.empty)

    def __str__(self):
        """Gör så att vi kan skriva ut spelplanen med print(grid)"""
        xs = ""
        for y in range(len(self.data)):
            row = self.data[y]
            for x in range(len(row)):
                if x == self.player.pos_x and y == self.player.pos_y:
                    xs += "@"
                elif (x, y) in self.enemies:
                    xs += self.enemy
                elif (x, y) in self.bombs:
                    xs += self.bomb
                else:
                    xs += str(row[x])
            xs += "\n"
        return xs

    def make_walls(self):
        """Skapa väggar runt hela spelplanen och några inre väggar"""
        # Yttre väggar
        for i in range(self.height):
            self.set(0, i, self.wall)
            self.set(self.width - 1, i, self.wall)

        for j in range(1, self.width - 1):
            self.set(j, 0, self.wall)
            self.set(j, self.height - 1, self.wall)

        # Inre väggar
        for i in range(2, self.height - 2, 4):
            for j in range(2, self.width - 2):
                self.set(j, i, self.wall)

        for j in range(2, self.width - 2, 6):
            for i in range(2, self.height - 2):
                self.set(j, i, self.wall)

        # Skapa öppningar i de inre väggarna för att undvika instängda rum
        for i in range(2, self.height - 2, 4):
            self.set(random.randint(2, self.width - 3), i, self.empty)

        for j in range(2, self.width - 2, 6):
            self.set(j, random.randint(2, self.height - 3), self.empty)

    # Används i filen pickups.py
    def get_random_x(self):
        """Slumpa en x-position på spelplanen"""
        return random.randint(0, self.width-1)

    def get_random_y(self):
        """Slumpa en y-position på spelplanen"""
        return random.randint(0, self.height-1)

    def is_empty(self, x, y):
        """Returnerar True om det inte finns något på aktuell ruta"""
        return self.get(x, y) == self.empty

    def add_enemy(self, x, y):
        """Lägg till en fiende på en given position"""
        self.enemies.append((x, y))

    def move_enemy_towards_player(self, enemy):
        """Flytta en fiende ett steg närmare spelaren"""
        ex, ey = enemy
        px, py = self.player.pos_x, self.player.pos_y
        if ex < px:
            new_ex = ex + 1
        elif ex > px:
            new_ex = ex - 1
        else:
            new_ex = ex

        if ey < py:
            new_ey = ey + 1
        elif ey > py:
            new_ey = ey - 1
        else:
            new_ey = ey

        if self.is_empty(new_ex, new_ey):
            self.enemies.remove(enemy)
            self.enemies.append((new_ex, new_ey))
            return (new_ex, new_ey)
        return enemy

    def place_bomb(self, x, y):
        """Placera en bomb på en given position"""
        if self.is_empty(x, y):
            self.bombs[(x, y)] = 3
            self.set(x, y, self.bomb)
            return True
        return False

    def explode_bomb(self, x, y):
        """Explodera en bomb och förstör omgivningen"""
        for i in range(max(0, y - 1), min(self.height, y + 2)):
            for j in range(max(0, x - 1), min(self.width, x + 2)):
                self.clear(j, i)
        if (self.player.pos_x >= max(0, x - 1) and self.player.pos_x <= min(self.width, x + 2) and
            self.player.pos_y >= max(0, y - 1) and self.player.pos_y <= min(self.height, y + 2)):
            return True  # Spelaren skadades
        return False

    def update_bombs(self):
        """Uppdatera alla bomber och detonera dem som ska explodera"""
        bombs_to_remove = []
        for (x, y), timer in self.bombs.items():
            self.bombs[(x, y)] -= 1
            if self.bombs[(x, y)] == 0:
                bombs_to_remove.append((x, y))

        player_damaged = False
        for (x, y) in bombs_to_remove:
            if self.explode_bomb(x, y):
                player_damaged = True
            del self.bombs[(x, y)]
        return player_damaged

    def disarm_trap(self, x, y):
        """Desarmera en fälla på en given position"""
        if self.get(x, y) == self.trap:
            self.clear(x, y)
            return True
        return False

