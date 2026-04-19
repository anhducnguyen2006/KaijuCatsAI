from numpy import random

import MapGeneration as mg

def generate_instructions():
    
    # Generate the game map
    map = mg.map_generation(42)  # Using a fixed seed for reproducibility

    # Initialize instructions for each tile based on the map layout
    instructions = [[] for _ in range(5)]

    # Framework for generating instructions based on the map layout    
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
    

    # Cost of each commands (Budget 200 dollars):
    # 1. Move North (N) - 10 dollars
    # 2. Move South (S) - 10 dollars
    # 3. Move East (E) - 10 dollars
    # 4. Move West (W) - 10 dollars
    # 5. Stomp (SP) - 20 dollars (cat stays and destroys an additional (second) floor)
    # 6. Power Up (PU) - 30 dollars (upon breaking a floor cat gains additional 1000 points)
    commands = {
        "N": 10,
        "S": 10,
        "E": 10,
        "W": 10,
        "SP": 20,
        "PU": 30
    }

    budget = 200
    # Random instructions generation for testing purposes (to be replaced with actual search algorithm)
    for i in range(5): 
        for j in range(5):
            if budget <= 0:
                break
            if instructions[i][j] is not None:
                if len(instructions[i][j]) == 2:
                    if random.random() < 0.5:  # 50% chance to place two commands
                        instructions[i][j][0] = random.choice(list(commands.keys()))
                        budget -= commands[instructions[i][j][0]]
                        if budget <= 0:
                            break
                    if random.random() < 0.5:  # 50% chance to place two commands
                        instructions[i][j][1] = random.choice(list(commands.keys()))
                        budget -= commands[instructions[i][j][1]]
                else:
                    if random.random() < 0.5:  # 50% chance to place two commands
                        instructions[i][j][0] = random.choice(list(commands.keys()))
                        budget -= commands[instructions[i][j][0]]
    
    # print the instructions for testing purposes
    print("Generated Instructions:")
    for i in range(5):
        for j in range(5):
            if instructions[i][j] is not None:
                print(f"{instructions[i][j]}" + (" " * (20 - len(str(instructions[i][j])))) , end=" ")
        print()  # New line after printing all instructions

    return (map, instructions, budget)