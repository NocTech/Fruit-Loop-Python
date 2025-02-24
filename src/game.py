from .grid import Grid
from .player import Player
from . import pickups
import random

g = Grid()
mid_x = g.width // 2
mid_y = g.height // 2

player = Player(mid_x, mid_y)
score = 0
inventory = []
move_count = 0  # Räknare för antalet drag
initial_pickups_count = 8  # Antal ursprungliga saker
grace_steps = 0  # Räknare för grace period steg

g.set_player(player)
g.make_walls()
pickups.randomize(g)

# Lägg till 1-3 fiender på slumpmässiga positioner
for _ in range(random.randint(1, 3)):
    while True:
        x = g.get_random_x()
        y = g.get_random_y()
        if g.is_empty(x, y):
            g.add_enemy(x, y)
            break

# TODO: flytta denna till en annan fil
def print_status(game_grid):
    """Visa spelvärlden och antal poäng."""
    print("--------------------------------------")
    print(f"You have {score} points.")
    print(f"Inventory: {[item.name for item in inventory]}")
    print(game_grid)

def move_player(dx, dy):
    global score, move_count, grace_steps
    if player.can_move(dx, dy, g):
        maybe_item = g.get(player.pos_x + dx, player.pos_y + dy)
        player.move(dx, dy)
        move_count += 1  # Öka räknaren för antalet drag

        # Hantera grace period
        if grace_steps > 0:
            grace_steps -= 1
        else:
            score -= 1  # Minska poängen med 1 för varje steg

        if isinstance(maybe_item, pickups.Item):
            score += maybe_item.value
            inventory.append(maybe_item)
            print(f"You found a {maybe_item.name}, +{maybe_item.value} points.")
            g.clear(player.pos_x, player.pos_y)
            grace_steps = 5  # Återställ grace period steg
            if isinstance(maybe_item, pickups.Shovel):
                player.has_shovel = True
            elif isinstance(maybe_item, pickups.Key):
                player.keys += 1
                print("You picked up a key.")
            elif isinstance(maybe_item, pickups.Chest):
                if player.keys > 0:
                    player.keys -= 1
                    score += maybe_item.value
                    print(f"You opened a chest and found a treasure worth {maybe_item.value} points.")
                    g.clear(player.pos_x, player.pos_y)
                else:
                    print("You need a key to open this chest.")
            elif isinstance(maybe_item, pickups.Exit):
                if len(inventory) >= initial_pickups_count:
                    print("Congratulations! You have collected all items and reached the exit. You win!")
                    exit()
                else:
                    print("You need to collect all items before you can use the exit.")
        
        # Skapa en ny frukt/grönsak efter varje 25:e drag
        if move_count % 25 == 0:
            new_item = random.choice(pickups.pickups[:8])  # Välj en frukt/grönsak
            while True:
                x = g.get_random_x()
                y = g.get_random_y()
                if g.is_empty(x, y):
                    g.set(x, y, new_item)
                    print(f"A new {new_item.name} has appeared on the map!")
                    break

        # Flytta fiender mot spelaren
        for enemy in g.enemies:
            if random.random() < 0.5:  # 50% chans att fienden rör sig
                new_pos = g.move_enemy_towards_player(enemy)
                if new_pos == (player.pos_x, player.pos_y):
                    score -= 20
                    print("An enemy caught you! -20 points.")

def print_inventory():
    """Skriv ut innehållet i spelarens inventory."""
    print("Inventory:")
    for item in inventory:
        print(f"- {item.name}")

def handle_command(command):
    global score
    if command.startswith("j"):
        jump = True
        command = command[1:]
    else:
        jump = False

    if command == "d":  # move right
        move_player(2 if jump else 1, 0)
    elif command == "a":  # move left
        move_player(-2 if jump else -1, 0)
    elif command == "w":  # move up
        move_player(0, -2 if jump else -1)
    elif command == "s":  # move down
        move_player(0, 2 if jump else 1)
    elif command == "i":  # view inventory
        print_inventory()
    elif command == "b":  # place bomb
        if g.place_bomb(player.pos_x, player.pos_y):
            print("Bomb placed!")
        else:
            print("Cannot place bomb here.")
    elif command == "t":  # disarm trap
        if g.disarm_trap(player.pos_x, player.pos_y):
            print("Trap disarmed!")
        else:
            print("No trap to disarm here.")

def update_game():
    global score
    player_damaged = g.update_bombs()
    if player_damaged:
        score -= 30
        print("You were caught in a bomb explosion! -30 points.")

command = "a"
# Loopa tills användaren trycker Q eller X.
while not command.casefold() in ["q", "x"]:
    print_status(g)

    command = input("Use WASD to move, J+WASD to jump, I to view inventory, B to place bomb, T to disarm trap, Q/X to quit. ")
    command = command.casefold()

    handle_command(command)
    update_game()

# Hit kommer vi när while-loopen slutar
print("Thank you for playing!")
