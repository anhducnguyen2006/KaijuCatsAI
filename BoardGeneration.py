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


def board_generation(seed):
    random.seed(seed)
    GRID_SIZE = 5
    HIGH_VALUE_BUILDING = "HV"
    LOW_VALUE_BUILDING = "LV"
    POWER_PLANT = "PP"
    MUD = "M "
    SPIKE_TRAP = "ST"
    BOULDER = "B "
    EMPTY_TILE = "ET"
    
    game_board = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    # ET always at (1, 0) and (3, 0)
    game_board[1][0] = EMPTY_TILE
    game_board[3][0] = EMPTY_TILE
    
    # Boulder can only be placed between columns 1 and 3 (only one boulder allowed)
    boulder_positions = [(i, j) for i in range(GRID_SIZE) for j in range(1, 4)]
    boulder_pos = random.choice(boulder_positions)
    game_board[boulder_pos[0]][boulder_pos[1]] = BOULDER
    
    # Place the remaining buildings and obstacles randomly
    # 5 High Value Buildings, 9 Low Value Buildings, 3 Power Plants, 1 Mud, 1 Spike Trap, 3 Empty Tiles
    remaining_tiles = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if game_board[i][j] == ""]
    random.shuffle(remaining_tiles)
    
    # High Value Building
    for _ in range(5):
        pos = remaining_tiles.pop()
        game_board[pos[0]][pos[1]] = HIGH_VALUE_BUILDING
    
    # Low Value Building
    for _ in range(9):
        pos = remaining_tiles.pop()
        game_board[pos[0]][pos[1]] = LOW_VALUE_BUILDING
    
    # Power Plant
    for _ in range(3):
        pos = remaining_tiles.pop()
        game_board[pos[0]][pos[1]] = POWER_PLANT
        
    # Mud
    pos = remaining_tiles.pop()
    game_board[pos[0]][pos[1]] = MUD
    
    # Spike Trap
    pos = remaining_tiles.pop()
    game_board[pos[0]][pos[1]] = SPIKE_TRAP
    
    # Empty Tiles
    for _ in range(3):
        pos = remaining_tiles.pop()
        game_board[pos[0]][pos[1]] = EMPTY_TILE

    # print the generated board
    # for row in game_board:
    #     print(" ".join(row))
    # print("\n")
    return game_board
    

def main():
    # Generate the game board
    board = board_generation(42)  # Using a fixed seed for reproducibility

if __name__ == "__main__":
    main()