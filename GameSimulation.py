import MapGeneration as mg
import InstructionGen as ig

def simulation(map, instructions):

    # Buildings: 
    #  1. High Value Building [HV] (worth 500 points, two floors = 2 commands can be placed on each floor)
    #  2. Low Value Building [LV] (worth 250 points, two floors = 2 commands can be placed on each floor)
    #  3. Power Plant [PP] (doubles points when stepped upon, one floor = 1 command can be placed on the floor)
    # Obstacles:
    #  1. Mud [M] (cat is stuck for one turn)
    #  2. Spike Trap [ST] (halves points when stepped upon)
    #  3. Boulder [B] (blocks the cat, rebounds back to opposite direction)
    # Neutral: Empty Tile [ET] (no command can be issued on this tile, cats can pass through without any effect)

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
    print(f"Initial Cat States:")
    print(f"Blue Cat - Position: {blue['pos']}, Power: {blue['power']}, Direction: {blue['dir']}, Action: {blue['action']}")
    print(f"Red Cat - Position: {red['pos']}, Power: {red['power']}, Direction: {red['dir']}, Action: {red['action']}")
    print(f"Green Cat - Position: {green['pos']}, Power: {green['power']}, Direction: {green['dir']}, Action: {green['action']}")
    print("-" * 30)

    # simulation of the game
    for i in range(15):

        # Simulate each Cat's turn
        for cat in priority:
            
            # check if any cat is already eliminated, if so skip its turn
            if cat['pos'] is None:
                continue

            # check if cat already in bed, then don't do anything
            if cat['pos'] == BLUE_CAT_BED or cat['pos'] == RED_CAT_BED or cat['pos'] == GREEN_CAT_BED:
                continue
            
            new_pos = tuple(x + y for x, y in zip(cat['pos'], directions[cat['dir']]))
            print(new_pos)

            # check if valid move (not out of bounds)
            if new_pos >= (0, 0) and new_pos < (5, 5):
                cat['pos'] = new_pos
                
                # Check if the tile has a building and if it still has floors left
                if map[cat['pos'][0]][cat['pos'][1]] in values and destroyed_floors[cat['pos'][0]][cat['pos'][1]] < len(instructions[cat['pos'][0]][cat['pos'][1]]):
                    destroyed_floors[cat['pos'][0]][cat['pos'][1]] += 1
                    cat['power'] = values[map[cat['pos'][0]][cat['pos'][1]]](cat['power'])
                else:
                    if map[cat['pos'][0]][cat['pos'][1]] == "M ":
                        # Cat is stuck for one turn, so we set its action to "STUCK" and it will skip its next turn
                        cat['action'] = "STUCK"
                    elif map[cat['pos'][0]][cat['pos'][1]] == "B ":
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
                    if instructions[cat['pos'][0]][cat['pos'][1]][destroyed_floors[cat['pos'][0]][cat['pos'][1]]] is not None:
                        cat['action'] = instructions[cat['pos'][0]][cat['pos'][1]][destroyed_floors[cat['pos'][0]][cat['pos'][1]]]
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
        

        ### CASE #1: All cats reach their bed on the same turn ###
        # if two or more cats reach their bed on the same turn, the cat with the highest 
        # priority:
        
        # 1st priority: power (cat with lowest power gets the highest priority).

        # if tie in power, 2nd priority (Blue > Red > Green) will be considered to have reached its bed first and will 
        # be awarded points accordingly.

        # the highest priority: +2000 power
        # the second priority: x3 power
        # the third priority: x5 power

        # if 3 simultaneously reach their bed, Blue gets +2000 power, Red gets x3 power, Green gets x5 power
        if blue['pos'] == BLUE_CAT_BED and red['pos'] == RED_CAT_BED and green['pos'] == GREEN_CAT_BED:
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
                        # based on priority list
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
                    # based on priority list
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
                        # based on priority list
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
                    # based on priority list
                    if priority.index(blue) < priority.index(green):
                        blue['power'] *= 3
                        green['power'] *= 5
                        red['power'] += 2000
                    else:
                        green['power'] *= 3
                        blue['power'] *= 5
                        red['power'] += 2000
            else:
                # based on priority list
                priority[0]['power'] += 2000
                priority[1]['power'] *= 3
                priority[2]['power'] *= 5

            print("\n")
            print("-" * 30)
            print("GAME OVER: All cats reached their bed at the same turn!")
            return blue["power"], red["power"], green["power"]
        
        # if 2 simultaneously reach their bed, 
        # if 3rd one is already in bed:
        #   the one with higher priority gets x3 power, the other gets x5 power
        # otherwise the one with higher priority gets +2000 power, the other gets x3 power
        elif blue['pos'] == BLUE_CAT_BED and red['pos'] == RED_CAT_BED:
            if green['pos'] == GREEN_CAT_BED:
                
                if blue['power'] < red['power']:
                    blue['power'] *= 3
                    red['power'] *= 5
                elif blue['power'] > red['power']:
                    blue['power'] *= 3
                    red['power'] *= 5
                else:
                    # based on priority list
                    if priority.index(blue) < priority.index(red):
                        blue['power'] *= 3
                        red['power'] *= 5
                    else:
                        blue['power'] *= 5
                        red['power'] *= 3
                
                print("\n")
                print("-" * 30)
                print("GAME OVER: All cats reached their bed at the same turn!")
                return blue["power"], red["power"], green["power"]
            else:
                if blue['power'] < red['power']:
                    blue['power'] += 2000
                    red['power'] *= 3
                elif blue['power'] > red['power']:
                    blue['power'] *= 3
                    red['power'] += 2000
                else:
                    # based on priority list
                    if priority.index(blue) < priority.index(red):
                        blue['power'] += 2000
                        red['power'] *= 3
                    else:
                        blue['power'] *= 3
                        red['power'] += 2000
        # same here
        elif blue['pos'] == BLUE_CAT_BED and green['pos'] == GREEN_CAT_BED:
            if red['pos'] == RED_CAT_BED:
                    
                if blue['power'] < green['power']:
                    blue['power'] *= 3
                    green['power'] *= 5
                elif blue['power'] > green['power']:
                    blue['power'] *= 5
                    green['power'] *= 3
                else:
                    # based on priority list
                    if priority.index(blue) < priority.index(green):
                        blue['power'] += 2000
                        green['power'] *= 3
                    else:
                        blue['power'] *= 3
                        green['power'] += 2000
                print("\n")
                print("-" * 30)
                print("GAME OVER: All cats reached their bed at the same turn!")
                return blue["power"], red["power"], green["power"]
            else:
                if blue['power'] < green['power']:
                    blue['power'] += 2000
                    green['power'] *= 3
                elif blue['power'] > green['power']:
                    blue['power'] *= 3
                    green['power'] += 2000
                else:
                    # based on priority list
                    if priority.index(blue) < priority.index(green):
                        blue['power'] += 2000
                        green['power'] *= 3
                    else:
                        blue['power'] *= 3
                        green['power'] += 2000
        # same here
        elif red['pos'] == RED_CAT_BED and green['pos'] == GREEN_CAT_BED:
            if blue['pos'] == BLUE_CAT_BED:
                if red['power'] < green['power']:
                    red['power'] *= 3
                    green['power'] *= 5
                elif red['power'] > green['power']:
                    red['power'] *= 5
                    green['power'] *= 3
                else:
                    # based on priority list
                    if priority.index(red) < priority.index(green):
                        red['power'] *= 3
                        green['power'] *= 5
                    else:
                        red['power'] *= 5
                        green['power'] *= 3
                print("\n")
                print("-" * 30)
                print("GAME OVER: All cats reached their bed at the same turn!")
                return blue["power"], red["power"], green["power"]
            else:
                if red['power'] < green['power']:
                    red['power'] += 2000
                    green['power'] *= 3
                elif red['power'] > green['power']:
                    red['power'] *= 3
                    green['power'] += 2000
                else:
                    # based on priority list
                    if priority.index(red) < priority.index(green):
                        red['power'] += 2000
                        green['power'] *= 3
                    else:
                        red['power'] *= 3
                        green['power'] += 2000
        # here, if only one cat reaches its bed, it gets +2000 power, 
        # if the other cats are already in their bed, then it gets x3 power, 
        # if both other cats are already in their bed, then it gets x5 power
        elif blue['pos'] == BLUE_CAT_BED:
            if red['pos'] == RED_CAT_BED:
                if green['pos'] == GREEN_CAT_BED:
                    blue['power'] *= 5
                    print("\n")
                    print("-" * 30)
                    print("GAME OVER: All cats reached their bed at the same turn!")
                    return blue["power"], red["power"], green["power"]
                else:
                    blue['power'] *= 3
            else:
                blue['power'] += 2000
        elif red['pos'] == RED_CAT_BED:
            if blue['pos'] == BLUE_CAT_BED:
                if green['pos'] == GREEN_CAT_BED:
                    red['power'] *= 5
                    print("\n")
                    print("-" * 30)
                    print("GAME OVER: All cats reached their bed at the same turn!")
                    return blue["power"], red["power"], green["power"]
                else:
                    red['power'] *= 3
            else:
                red['power'] += 2000
        elif green['pos'] == GREEN_CAT_BED:
            if blue['pos'] == BLUE_CAT_BED:
                if red['pos'] == RED_CAT_BED:
                    green['power'] *= 5
                    print("\n")
                    print("-" * 30)
                    print("GAME OVER: All cats reached their bed at the same turn!")
                    return blue["power"], red["power"], green["power"]
                else:
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

        print(f"Turn {i + 1}:")
        print(f"Blue Cat - Position: {blue['pos']}, Power: {blue['power']}, Direction: {blue['dir']}, Action: {blue['action']}")
        print(f"Red Cat - Position: {red['pos']}, Power: {red['power']}, Direction: {red['dir']}, Action: {red['action']}")
        print(f"Green Cat - Position: {green['pos']}, Power: {green['power']}, Direction: {green['dir']}, Action: {green['action']}")
        print("-" * 30)

    
    
    
    
    
    
def main():
    map, instructions, budget = ig.generate_instructions()
    simulation(map, instructions)
    
        
if __name__ == "__main__":
    main()