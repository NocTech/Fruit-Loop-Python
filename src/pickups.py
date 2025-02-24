class Item:
    """Representerar saker man kan plocka upp."""
    def __init__(self, name, value=20, symbol="?"):
        self.name = name
        self.value = value
        self.symbol = symbol

    def __str__(self):
        return self.symbol

class Shovel(Item):
    """Representerar en spade."""
    def __init__(self):
        super().__init__(name="shovel", value=0, symbol="S")

class Key(Item):
    """Representerar en nyckel."""
    def __init__(self):
        super().__init__(name="key", value=0, symbol="K")

class Chest(Item):
    """Representerar en kista."""
    def __init__(self):
        super().__init__(name="chest", value=100, symbol="C")

class Exit(Item):
    """Representerar en exit."""
    def __init__(self):
        super().__init__(name="exit", value=0, symbol="E")

pickups = [Item("carrot"), Item("apple"), Item("strawberry"), Item("cherry"), Item("watermelon"), Item("radish"), Item("cucumber"), Item("meatball"), Shovel(), Key(), Chest(), Exit()]

def randomize(grid):
    # Slumpa ut vanliga saker
    for item in pickups[:8]:
        while True:
            # slumpa en position tills vi hittar en som är ledig
            x = grid.get_random_x()
            y = grid.get_random_y()
            if grid.is_empty(x, y):
                grid.set(x, y, item)
                break  # avbryt while-loopen, fortsätt med nästa varv i for-loopen

    # Slumpa ut en spade
    while True:
        x = grid.get_random_x()
        y = grid.get_random_y()
        if grid.is_empty(x, y):
            grid.set(x, y, Shovel())
            break

    # Slumpa ut en nyckel
    while True:
        x = grid.get_random_x()
        y = grid.get_random_y()
        if grid.is_empty(x, y):
            grid.set(x, y, Key())
            break

    # Slumpa ut en kista
    while True:
        x = grid.get_random_x()
        y = grid.get_random_y()
        if grid.is_empty(x, y):
            grid.set(x, y, Chest())
            break

    # Slumpa ut en exit
    while True:
        x = grid.get_random_x()
        y = grid.get_random_y()
        if grid.is_empty(x, y):
            grid.set(x, y, Exit())
            break

