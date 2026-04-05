'''
Kaiju Cats Roblox game simulation script.

@author: Anh Duc Nguyen
@date: 2026-03-02
'''


# Place buildings and obstacles on the 5x5 map
# Buildings: 
#  1. High Value Building [HV] (worth 500 points, two floors = 2 commands can be placed on each floor)
#  2. Low Value Building [LV] (worth 250 points, two floors = 2 commands can be placed on each floor)
#  3. Power Plant [PP] (doubles points when stepped upon, one floor = 1 command can be placed on the floor)
# Obstacles:
#  1. Mud [M] (cat is stuck for one turn)
#  2. Spike Trap [ST] (halves points when stepped upon)
#  3. Boulder [B] (blocks the cat, rebounds back to opposite direction)
# Neutral: Empty Tile [ET] (no command can be issued on this tile, cats can pass through without any effect)
import random


def map_generation():
    GRID_SIZE = 5
    HIGH_VALUE_BUILDING = "HV"
    LOW_VALUE_BUILDING = "LV"
    POWER_PLANT = "PP"
    MUD = "M"
    SPIKE_TRAP = "ST"
    BOULDER = "B"
    EMPTY_TILE = "ET"
    
    game_map = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    # ET always at (1, 0) and (3, 0)
    game_map[1][0] = EMPTY_TILE
    game_map[3][0] = EMPTY_TILE
    
    # Boulder can only be placed between columns 1 and 3 (only one boulder allowed)
    boulder_positions = [(i, j) for i in range(GRID_SIZE) for j in range(1, 4)]
    boulder_pos = random.choice(boulder_positions)
    game_map[boulder_pos[0]][boulder_pos[1]] = BOULDER
    
    # Place the remaining buildings and obstacles randomly
    # 5 High Value Buildings, 9 Low Value Buildings, 3 Power Plants, 1 Mud, 1 Spike Trap, 3 Empty Tiles
    remaining_tiles = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if game_map[i][j] == 0]
    random.shuffle(remaining_tiles)
    
    # High Value Building
    for _ in range(5):
        pos = remaining_tiles.pop()
        game_map[pos[0]][pos[1]] = HIGH_VALUE_BUILDING
    
    # Low Value Building
    for _ in range(9):
        pos = remaining_tiles.pop()
        game_map[pos[0]][pos[1]] = LOW_VALUE_BUILDING
    
    # Power Plant
    for _ in range(3):
        pos = remaining_tiles.pop()
        game_map[pos[0]][pos[1]] = POWER_PLANT
        
    # Mud
    pos = remaining_tiles.pop()
    game_map[pos[0]][pos[1]] = MUD
    
    # Spike Trap
    pos = remaining_tiles.pop()
    game_map[pos[0]][pos[1]] = SPIKE_TRAP
    
    # Empty Tiles
    for _ in range(3):
        pos = remaining_tiles.pop()
        game_map[pos[0]][pos[1]] = EMPTY_TILE
        
    # Print the generated map
    print("Generated Game Map:")
    for row in game_map:
        print(" ".join(row))
    return game_map
    

def main():
    print("Starting the game simulation...")
    
    # Generate the game map
    map = map_generation()
    
    # Commands (Budget 200 dollars):
    # 1. Move North (N) - 10 dollars
    # 2. Move South (S) - 10 dollars
    # 3. Move East (E) - 10 dollars
    # 4. Move West (W) - 10 dollars
    # 5. Stomp (SP) - 20 dollars (cat stays and destroys an additional (second) floor)
    # 6. Power Up (PU) - 30 dollars (upon breaking a floor cat gains additional 1000 points)
    
    instructions = [[] for _ in range(5)]
    
    for i in range(5): 
        for j in range(5):
            if map[i][j] in ["HV", "LV"]:
                instructions[i].append([None, None])  # two commands available 
            elif map[i][j] == "PP":
                instructions[i].append([None])  # one command available
            elif map[i][j] == "M":
                instructions[i].append(None)  # zero commands available, cat is stuck for one turn
            elif map[i][j] == "ST":
                instructions[i].append(None)  # zero commands available, cat's points are halved when stepped upon
            elif map[i][j] == "B":
                instructions[i].append(None)  # zero commands available, cat is blocked and rebounds back to opposite direction
            else:
                instructions[i].append(None)  # zero commands available, cats can pass through without any effect
    
    commands = {
        "N": 10,
        "S": 10,
        "E": 10,
        "W": 10,
        "SP": 20,
        "PU": 30
    }
    
    # Position of cats (initially standing on an Empty Tile outside of the map)
    # Blue cat top left corner (0, -1)
    # Red cat middle left (2, -1)
    # Green cat bottom left corner (4, -1)
    BLUE_CAT_START = (0, -1)
    RED_CAT_START = (2, -1)
    GREEN_CAT_START = (4, -1)
    
    # Position of their respective beds (outside of the map on the right side)
    # Blue cat bed (1, 5)
    # Red cat bed (2, 5)
    # Green cat bed (3, 5)
    
    BLUE_CAT_BED = (1, 5)
    RED_CAT_BED = (2, 5)
    GREEN_CAT_BED = (3, 5)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    main()