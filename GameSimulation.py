'''
Kaiju Cats Roblox game simulation script.

@author: Anh Duc Nguyen
@date: 2026-03-02
'''

import InstructionGen as ig
import time

def simulation(board, instructions):

    # Buildings: 
    #  1. High Value Building [HV] (worth 500 points, two floors = 2 commands can be placed on each floor)
    #  2. Low Value Building [LV] (worth 250 points, two floors = 2 commands can be placed on each floor)
    #  3. Power Plant [PP] (doubles points when stepped upon, one floor = 1 command can be placed on the floor)
    # Obstacles:
    #  1. Mud [M] (cat is stuck for one turn)
    #  2. Spike Trap [ST] (halves points when stepped upon)
    #  3. Boulder [B] (blocks the cat, rebounds back to opposite direction)
    # Neutral: Empty Tile [ET] (no command can be issued on this tile, cats can pass through without any effect)

    # Position of cats (initially standing on an Empty Tile outside of the board)
    # Blue cat top left corner (0, -1)
    # Red cat middle left (2, -1)
    # Green cat bottom left corner (4, -1)
    BLUE_CAT_START = (0, -1)
    RED_CAT_START = (2, -1)
    GREEN_CAT_START = (4, -1)
    
    # Position of their respective beds (outside of the board on the right side)
    # Blue cat bed (1, 5)
    # Red cat bed (2, 5)
    # Green cat bed (3, 5)
    # Order indicates also priority which cat goes first when two reach their bed on
    # the same turn, Blue has the highest priority and Green has the lowest priority
    BLUE_CAT_BED = (1, 5)
    RED_CAT_BED = (2, 5)
    GREEN_CAT_BED = (3, 5)


    blue = {
        "pos": BLUE_CAT_START,
        "power": 0,
        "dir": "E",
        "action": None
    }

    red = {
        "pos": RED_CAT_START,
        "power": 0,
        "dir": "E",
        "action": None
    }

    green = {
        "pos": GREEN_CAT_START,
        "power": 0,
        "dir": "E",
        "action": None
    }

    priority = [blue, red, green]

    directions = {
        "N": (-1, 0),
        "S": (1, 0),
        "E": (0, 1),
        "W": (0, -1)
    }

    destroyed_floors = [[0 for _ in range(5)] for _ in range(5)]  # To keep track of destroyed floors for each tile

    values = {
        "HV": lambda x: x + 500,
        "LV": lambda x: x + 250,
        "PP": lambda x: x * 2,  # Power Plant's value is determined by its effect, not a fixed point value
        "ST": lambda x: x // 2,  # Spike Trap doesn't give points, it just halves the cat's points
    }

    # for each cat, we will print their initial position, power, and direction
    # print(f"Initial Cat States:")
    # print(f"Blue Cat - Position: {blue['pos']}, Power: {blue['power']}, Direction: {blue['dir']}, Action: {blue['action']}")
    # print(f"Red Cat - Position: {red['pos']}, Power: {red['power']}, Direction: {red['dir']}, Action: {red['action']}")
    # print(f"Green Cat - Position: {green['pos']}, Power: {green['power']}, Direction: {green['dir']}, Action: {green['action']}")
    # print("-" * 100)

    # simulation of the game
    for i in range(15):

        # Record which cats were already in bed before this turn's moves
        blue_in_bed_before = (blue['pos'] == BLUE_CAT_BED)
        red_in_bed_before = (red['pos'] == RED_CAT_BED)
        green_in_bed_before = (green['pos'] == GREEN_CAT_BED)

        # Simulate each Cat's turn
        for cat in priority:
            
            # check if any cat is already eliminated, if so skip its turn
            if cat['pos'] is None:
                continue

            # check if cat already in bed, then don't do anything
            if cat['pos'] == BLUE_CAT_BED or cat['pos'] == RED_CAT_BED or cat['pos'] == GREEN_CAT_BED:
                continue
            
            # move only if no action was assigned to the cat, otherwise the cat will perform the action first before moving
            move = True

            # Handle actions of cats
            if cat['action'] == "STUCK":
                cat['action'] = None  # Cat is now unstuck and can move in the next turn
                continue  # Skip the rest of the turn for this cat since it's stuck
                move = False
            elif cat['action'] == "SP":
                # Stomp command destroys an additional floor, so we increment destroyed_floors by 1 more
                # this indirectly handles the case where the cat stomps on nothing (eg. stomp on the last floor of a building or power plant)
                if instructions[cat['pos'][0]][cat['pos'][1]] is not None and destroyed_floors[cat['pos'][0]][cat['pos'][1]] < len(instructions[cat['pos'][0]][cat['pos'][1]]):
                    cat['action'] = instructions[cat['pos'][0]][cat['pos'][1]][destroyed_floors[cat['pos'][0]][cat['pos'][1]]]
                destroyed_floors[cat['pos'][0]][cat['pos'][1]] += 1
                move = False

            if move == False:
                continue

            new_pos = tuple(x + y for x, y in zip(cat['pos'], directions[cat['dir']]))
            #print(new_pos)

            # check if valid move (not out of bounds)
            if new_pos[0] >= 0 and new_pos[0] < 5 and new_pos[1] >= 0 and new_pos[1] < 5 and cat['action'] is None:
                cat['pos'] = new_pos
                
                # ST always halves points regardless of floors (it is never destroyed)
                if board[cat['pos'][0]][cat['pos'][1]] == "ST":
                    cat['power'] = values["ST"](cat['power'])
                # Check if the tile has a building and if it still has floors left
                elif board[cat['pos'][0]][cat['pos'][1]] in values and instructions[cat['pos'][0]][cat['pos'][1]] is not None and destroyed_floors[cat['pos'][0]][cat['pos'][1]] < len(instructions[cat['pos'][0]][cat['pos'][1]]):
                    cat['power'] = values[board[cat['pos'][0]][cat['pos'][1]]](cat['power'])
                    # handle Power Up here
                    if instructions[cat['pos'][0]][cat['pos'][1]] == "PU":
                        # Remove the Power Up instruction after using it
                        instructions[cat['pos'][0]][cat['pos'][1]][destroyed_floors[cat['pos'][0]][cat['pos'][1]]] = None
                        cat['power'] += 1000
                else:
                    if board[cat['pos'][0]][cat['pos'][1]] == "M ":
                        # Cat is stuck for one turn, so we set its action to "STUCK" and it will skip its next turn
                        cat['action'] = "STUCK"
                    elif board[cat['pos'][0]][cat['pos'][1]] == "B ":
                        # Rebound back to opposite direction
                        cat['pos'] = (cat['pos'][0] - directions[cat['dir']][0], cat['pos'][1] - directions[cat['dir']][1])
                        if cat['dir'] == "N":
                            cat['dir'] = "S"
                        elif cat['dir'] == "S":
                            cat['dir'] = "N"
                        elif cat['dir'] == "E":
                            cat['dir'] = "W"
                        elif cat['dir'] == "W":
                            cat['dir'] = "E"
                    # If it's an empty tile or all floors are destroyed, just pass through without any effect
                
                if instructions[cat['pos'][0]][cat['pos'][1]] is not None and destroyed_floors[cat['pos'][0]][cat['pos'][1]] < len(instructions[cat['pos'][0]][cat['pos'][1]]):
                    next_instruction = instructions[cat['pos'][0]][cat['pos'][1]][destroyed_floors[cat['pos'][0]][cat['pos'][1]]]
                    if next_instruction is not None:
                        # only assign action if it's not Power Up since Power Up is handled separately and doesn't 
                        # need to be assigned as an action for the cat to perform in the next turn
                        if next_instruction == "PU":
                            continue
                        elif next_instruction in ["N", "S", "E", "W"]:
                            cat['dir'] = next_instruction
                        else:
                            cat['action'] = next_instruction
                    instructions[cat['pos'][0]][cat['pos'][1]][destroyed_floors[cat['pos'][0]][cat['pos'][1]]] = None
                    destroyed_floors[cat['pos'][0]][cat['pos'][1]] += 1
            
            # Case if trying to move out of bounds, but it's a bed so it's a valid move and cat can step on it
            elif new_pos == BLUE_CAT_BED or new_pos == RED_CAT_BED or new_pos == GREEN_CAT_BED:
                cat['pos'] = new_pos

            else: 
                # rebound back to opposite direction if trying to move out of bounds
                if cat['dir'] == "N":
                    cat['dir'] = "S"
                elif cat['dir'] == "S":
                    cat['dir'] = "N"
                elif cat['dir'] == "E":
                    cat['dir'] = "W"
                elif cat['dir'] == "W":
                    cat['dir'] = "E"

            # update board in case a building is destroyed in some tile, change it into Empty Tile (ET)
            if cat['pos'] is not None and 0 <= cat['pos'][0] < 5 and 0 <= cat['pos'][1] < 5 and board[cat['pos'][0]][cat['pos'][1]] not in ["ST", "ET", "M ", "B "] and instructions[cat['pos'][0]][cat['pos'][1]] is not None and destroyed_floors[cat['pos'][0]][cat['pos'][1]] >= len(instructions[cat['pos'][0]][cat['pos'][1]]):
                board[cat['pos'][0]][cat['pos'][1]] = "ET"
        # Determine which cats just arrived at their bed this turn (reward applied once only)
        blue_just_arrived = (blue['pos'] == BLUE_CAT_BED and not blue_in_bed_before)
        red_just_arrived = (red['pos'] == RED_CAT_BED and not red_in_bed_before)
        green_just_arrived = (green['pos'] == GREEN_CAT_BED and not green_in_bed_before)

        ### CASE #1: Bed arrival rewards (each cat rewarded exactly once on arrival turn) ###
        # Priority for rewards is determined by power (lowest power = highest priority).
        # If tied on power, Blue > Red > Green by position in priority list.
        # 1st to arrive (highest priority): +2000 power
        # 2nd to arrive: x3 power
        # 3rd to arrive: x5 power

        if blue_just_arrived and red_just_arrived and green_just_arrived:
            if blue['power'] < red['power']:
                if blue['power'] < green['power']:
                    blue['power'] += 2000
                    if red['power'] < green['power']:
                        red['power'] *= 3
                        green['power'] *= 5
                    elif red['power'] > green['power']:
                        red['power'] *= 5
                        green['power'] *= 3
                    else:
                        if priority.index(red) < priority.index(green):
                            red['power'] *= 3
                            green['power'] *= 5
                        else:
                            red['power'] *= 5
                            green['power'] *= 3
                elif blue['power'] > green['power']:
                    green['power'] += 2000
                    blue['power'] *= 3
                    red['power'] *= 5
                else:
                    if priority.index(blue) < priority.index(green):
                        blue['power'] += 2000
                        green['power'] *= 3
                        red['power'] *= 5
                    else:
                        green['power'] += 2000
                        blue['power'] *= 3
                        red['power'] *= 5
            elif blue['power'] > red['power']:
                if blue['power'] > green['power']:
                    blue['power'] *= 5
                    if red['power'] < green['power']:
                        red['power'] += 2000
                        green['power'] *= 3
                    elif red['power'] > green['power']:
                        red['power'] *= 3
                        green['power'] += 2000
                    else:
                        if priority.index(red) < priority.index(green):
                            red['power'] += 2000
                            green['power'] *= 3
                        else:
                            red['power'] *= 3
                            green['power'] += 2000
                elif blue['power'] < green['power']:
                    green['power'] *= 5
                    blue['power'] *= 3
                    red['power'] += 2000
                else:
                    if priority.index(blue) < priority.index(green):
                        blue['power'] *= 3
                        green['power'] *= 5
                        red['power'] += 2000
                    else:
                        green['power'] *= 3
                        blue['power'] *= 5
                        red['power'] += 2000
            else:
                priority[0]['power'] += 2000
                priority[1]['power'] *= 3
                priority[2]['power'] *= 5
            print("\n")
            print("-" * 100)
            print("GAME OVER: 15 turns have passed!")
            print(f"Final Results:")
            print(f"Blue Cat: {blue['power']}")
            print(f"Red Cat: {red['power']}")
            print(f"Green Cat: {green['power']}")
            print(f"TOTAL POWER: {blue['power'] + red['power'] + green['power']}")
            print("-" * 100)
            return blue["power"], red["power"], green["power"]

        elif blue_just_arrived and red_just_arrived:
            if green['pos'] == GREEN_CAT_BED:
                if blue['power'] < red['power']:
                    blue['power'] *= 3
                    red['power'] *= 5
                elif blue['power'] > red['power']:
                    blue['power'] *= 5
                    red['power'] *= 3
                else:
                    if priority.index(blue) < priority.index(red):
                        blue['power'] *= 3
                        red['power'] *= 5
                    else:
                        blue['power'] *= 5
                        red['power'] *= 3
                print("\n")
                print("-" * 100)
                print("GAME OVER: 15 turns have passed!")
                print(f"Final Results:")
                print(f"Blue Cat: {blue['power']}")
                print(f"Red Cat: {red['power']}")
                print(f"Green Cat: {green['power']}")
                print(f"TOTAL POWER: {blue['power'] + red['power'] + green['power']}")
                print("-" * 100)
                return blue["power"], red["power"], green["power"]
            else:
                if blue['power'] < red['power']:
                    blue['power'] += 2000
                    red['power'] *= 3
                elif blue['power'] > red['power']:
                    blue['power'] *= 3
                    red['power'] += 2000
                else:
                    if priority.index(blue) < priority.index(red):
                        blue['power'] += 2000
                        red['power'] *= 3
                    else:
                        blue['power'] *= 3
                        red['power'] += 2000

        elif blue_just_arrived and green_just_arrived:
            if red['pos'] == RED_CAT_BED:
                if blue['power'] < green['power']:
                    blue['power'] *= 3
                    green['power'] *= 5
                elif blue['power'] > green['power']:
                    blue['power'] *= 5
                    green['power'] *= 3
                else:
                    if priority.index(blue) < priority.index(green):
                        blue['power'] *= 3
                        green['power'] *= 5
                    else:
                        blue['power'] *= 5
                        green['power'] *= 3
                print("\n")
                print("-" * 100)
                print("GAME OVER: 15 turns have passed!")
                print(f"Final Results:")
                print(f"Blue Cat: {blue['power']}")
                print(f"Red Cat: {red['power']}")
                print(f"Green Cat: {green['power']}")
                print(f"TOTAL POWER: {blue['power'] + red['power'] + green['power']}")
                print("-" * 100)
                return blue["power"], red["power"], green["power"]
            else:
                if blue['power'] < green['power']:
                    blue['power'] += 2000
                    green['power'] *= 3
                elif blue['power'] > green['power']:
                    blue['power'] *= 3
                    green['power'] += 2000
                else:
                    if priority.index(blue) < priority.index(green):
                        blue['power'] += 2000
                        green['power'] *= 3
                    else:
                        blue['power'] *= 3
                        green['power'] += 2000

        elif red_just_arrived and green_just_arrived:
            if blue['pos'] == BLUE_CAT_BED:
                if red['power'] < green['power']:
                    red['power'] *= 3
                    green['power'] *= 5
                elif red['power'] > green['power']:
                    red['power'] *= 5
                    green['power'] *= 3
                else:
                    if priority.index(red) < priority.index(green):
                        red['power'] *= 3
                        green['power'] *= 5
                    else:
                        red['power'] *= 5
                        green['power'] *= 3
                print("\n")
                print("-" * 100)
                print("GAME OVER: 15 turns have passed!")
                print(f"Final Results:")
                print(f"Blue Cat: {blue['power']}")
                print(f"Red Cat: {red['power']}")
                print(f"Green Cat: {green['power']}")
                print(f"TOTAL POWER: {blue['power'] + red['power'] + green['power']}")
                print("-" * 100)
                return blue["power"], red["power"], green["power"]
            else:
                if red['power'] < green['power']:
                    red['power'] += 2000
                    green['power'] *= 3
                elif red['power'] > green['power']:
                    red['power'] *= 3
                    green['power'] += 2000
                else:
                    if priority.index(red) < priority.index(green):
                        red['power'] += 2000
                        green['power'] *= 3
                    else:
                        red['power'] *= 3
                        green['power'] += 2000

        elif blue_just_arrived:
            if red['pos'] == RED_CAT_BED and green['pos'] == GREEN_CAT_BED:
                blue['power'] *= 5
                print("\n")
                print("-" * 100)
                print("GAME OVER: 15 turns have passed!")
                print(f"Final Results:")
                print(f"Blue Cat: {blue['power']}")
                print(f"Red Cat: {red['power']}")
                print(f"Green Cat: {green['power']}")
                print(f"TOTAL POWER: {blue['power'] + red['power'] + green['power']}")
                print("-" * 100)
                return blue["power"], red["power"], green["power"]
            elif red['pos'] == RED_CAT_BED or green['pos'] == GREEN_CAT_BED:
                blue['power'] *= 3
            else:
                blue['power'] += 2000

        elif red_just_arrived:
            if blue['pos'] == BLUE_CAT_BED and green['pos'] == GREEN_CAT_BED:
                red['power'] *= 5
                print("\n")
                print("-" * 100)
                print("GAME OVER: 15 turns have passed!")
                print(f"Final Results:")
                print(f"Blue Cat: {blue['power']}")
                print(f"Red Cat: {red['power']}")
                print(f"Green Cat: {green['power']}")
                print(f"TOTAL POWER: {blue['power'] + red['power'] + green['power']}")
                print("-" * 100)
                return blue["power"], red["power"], green["power"]
            elif blue['pos'] == BLUE_CAT_BED or green['pos'] == GREEN_CAT_BED:
                red['power'] *= 3
            else:
                red['power'] += 2000

        elif green_just_arrived:
            if blue['pos'] == BLUE_CAT_BED and red['pos'] == RED_CAT_BED:
                green['power'] *= 5
                print("\n")
                print("-" * 100)
                print("GAME OVER: 15 turns have passed!")
                print(f"Final Results:")
                print(f"Blue Cat: {blue['power']}")
                print(f"Red Cat: {red['power']}")
                print(f"Green Cat: {green['power']}")
                print(f"TOTAL POWER: {blue['power'] + red['power'] + green['power']}")
                print("-" * 100)
                return blue["power"], red["power"], green["power"]
            elif blue['pos'] == BLUE_CAT_BED or red['pos'] == RED_CAT_BED:
                green['power'] *= 3
            else:
                green['power'] += 2000

        ### CASE #2: Cat fights ###
        # if two or more cats end up on the same tile after moving, the one with
        # less power -> gets eliminated and removed from the game, 
        # the one with more power -> wins the fight, stays
        if blue['pos'] == red['pos'] == green['pos']:
            # if all three cats end up on the same tile, the one with the highest power wins, the other two get eliminated
            if blue['power'] > red['power'] and blue['power'] > green['power']:
                red['pos'] = None
                red['power'] = 0
                green['pos'] = None
                green['power'] = 0
            elif red['power'] > blue['power'] and red['power'] > green['power']:
                blue['pos'] = None
                blue['power'] = 0
                green['pos'] = None
                green['power'] = 0
            elif green['power'] > blue['power'] and green['power'] > red['power']:
                blue['pos'] = None
                blue['power'] = 0
                red['pos'] = None
                red['power'] = 0
            else:
                # if there's a tie in power, based on priority list, Blue wins over Red, Red wins over Green, Blue wins over Green
                if priority.index(blue) < priority.index(red) and priority.index(blue) < priority.index(green):
                    red['pos'] = None
                    red['power'] = 0
                    green['pos'] = None
                    green['power'] = 0
                elif priority.index(red) < priority.index(blue) and priority.index(red) < priority.index(green):
                    blue['pos'] = None
                    blue['power'] = 0
                    green['pos'] = None
                    green['power'] = 0
                elif priority.index(green) < priority.index(blue) and priority.index(green) < priority.index(red):
                    blue['pos'] = None
                    blue['power'] = 0
                    red['pos'] = None
                    red['power'] = 0
        elif blue['pos'] == red['pos']:
            if blue['power'] > red['power']:
                red['pos'] = None
                red['power'] = 0
            elif red['power'] > blue['power']:
                blue['pos'] = None
                blue['power'] = 0
            else:
                # if there's a tie in power, based on priority list, Blue wins over Red
                if priority.index(blue) < priority.index(red):
                    red['pos'] = None
                    red['power'] = 0
                else:
                    blue['pos'] = None
                    blue['power'] = 0
        elif blue['pos'] == green['pos']:
            if blue['power'] > green['power']:
                green['pos'] = None
                green['power'] = 0
            elif green['power'] > blue['power']:
                blue['pos'] = None
                blue['power'] = 0
            else:
                # if there's a tie in power, based on priority list, Blue wins over Green
                if priority.index(blue) < priority.index(green):
                    green['pos'] = None
                    green['power'] = 0
                else:
                    blue['pos'] = None
                    blue['power'] = 0
        elif red['pos'] == green['pos']:
            if red['power'] > green['power']:
                green['pos'] = None
                green['power'] = 0
            elif green['power'] > red['power']:
                red['pos'] = None
                red['power'] = 0
            else:
                # if there's a tie in power, based on priority list, Red wins over Green
                if priority.index(red) < priority.index(green):
                    green['pos'] = None
                    green['power'] = 0
                else:
                    red['pos'] = None
                    red['power'] = 0

        # print(f"Turn {i + 1}:")

        # print the position, power, direction, and action of each cat after each turn
        # or if it's in the bed, print that it's in the bed instead of its position
        # if blue['pos'] == BLUE_CAT_BED:
        #     print(f"Blue Cat - Position: IN BED, Power: {blue['power']}")
        # else:  
        #     print(f"Blue Cat - Position: {blue['pos']}, Power: {blue['power']}, Direction: {blue['dir']}, Action: {blue['action']}")
        
        # if red['pos'] == RED_CAT_BED:
        #     print(f"Red Cat - Position: IN BED, Power: {red['power']}")
        # else:
        #     print(f"Red Cat - Position: {red['pos']}, Power: {red['power']}, Direction: {red['dir']}, Action: {red['action']}")
        
        # if green['pos'] == GREEN_CAT_BED:
        #     print(f"Green Cat - Position: IN BED, Power: {green['power']}")
        # else:
        #     print(f"Green Cat - Position: {green['pos']}, Power: {green['power']}, Direction: {green['dir']}, Action: {green['action']}")
        # print("-" * 100)
    

    # print("Generated Instructions:")
    # for i in range(5):
    #     for j in range(5):
    #         if instructions[i][j] is not None:
    #             print(f"{instructions[i][j]}" + (" " * (30 - len(str(instructions[i][j])))) , end=" ")
    #         else:
    #             print("None" + (" " * 26), end=" ")
    #     print()  # New line after printing all instructions

    # # print final results after 15 turns
    # print("\n")
    # print("-" * 100)
    # print("GAME OVER: 15 turns have passed!")
    # print(f"Final Results:")
    # print(f"Blue Cat: {blue['power']}")
    # print(f"Red Cat: {red['power']}")
    # print(f"Green Cat: {green['power']}")
    # print(f"TOTAL POWER: {blue['power'] + red['power'] + green['power']}")
    # print("-" * 100)
    return blue["power"], red["power"], green["power"]

def print_board(board):
    print("Generated Game Board:")
    for row in board:
        print(" | ".join(row))
        print("-" * 22)  # Separator between rows
    
def print_instructions(instructions):
    print("Generated Instructions:")
    for i in range(5):
        for j in range(5):
            if instructions[i][j] is not None:
                print(f"{instructions[i][j]}" + (" " * (30 - len(str(instructions[i][j])))) , end=" ")
            else:
                print("None" + (" " * 26), end=" ")
        print()  # New line after printing all instructions

def print_results(blue, red, green):
    print("\n")
    print("-" * 100)
    print("GAME OVER: 15 turns have passed!")
    print(f"Final Results:")
    print(f"Blue Cat: {blue}")
    print(f"Red Cat: {red}")
    print(f"Green Cat: {green}")
    print(f"TOTAL POWER: {blue + red + green}")
    print("-" * 100)


def main():
    # Example usage of the simulation with randomly generated instructions

    # Generating as many simulations as possible in 1 minute time constraint
    start_time = time.time()
    end_time = start_time + 60  # Run for 60 seconds

    i = 0
    while True:  # Arbitrary large number to keep generating simulations until time runs out
        board, instructions, budget = ig.generate_instructions(i)
        score = simulation(board, instructions)
        if time.time() >= end_time:
            break
        i += 1
    
    print(f"Generated {i} simulations in 1 minute.")
        
if __name__ == "__main__":
    main()