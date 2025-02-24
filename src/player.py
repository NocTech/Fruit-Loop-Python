class Player:
    marker = "@"

    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.has_shovel = False
        self.keys = 0  # Lägg till detta för att initiera attributet keys

    # Flyttar spelaren. "dx" och "dy" är skillnaden
    def move(self, dx, dy):
        """Flyttar spelaren.\n
        dx = horisontell förflyttning, från vänster till höger\n
        dy = vertikal förflyttning, uppifrån och ned"""
        self.pos_x += dx
        self.pos_y += dy

    def can_move(self, dx, dy, grid):
        new_x = self.pos_x + dx
        new_y = self.pos_y + dy
        if grid.get(new_x, new_y) == grid.wall:
            if self.has_shovel:
                grid.clear(new_x, new_y)
                self.has_shovel = False
                print("You used the shovel to remove the wall.")
                return True
            return False
        return True


