from numpy import random

import BoardGeneration as bg

def generate_instructions(seed):
    
    # generate seed for reproducibility
    random.seed(seed)

    # Generate the game board
    board = bg.board_generation(seed)  # Using a fixed seed for reproducibility

    # Initialize instructions for each tile based on the board layout
    instructions = [[] for _ in range(5)]

    # Framework for generating instructions based on the board layout    
    for i in range(5): 
        for j in range(5):
            if board[i][j] in ["HV", "LV"]:
                instructions[i].append([None, None])  # two commands available 
            elif board[i][j] == "PP":
                instructions[i].append([None])  # one command available
            elif board[i][j] == "M":
                instructions[i].append(None)  # zero commands available, cat is stuck for one turn
            elif board[i][j] == "ST":
                instructions[i].append(None)  # zero commands available, cat's points are halved when stepped upon
            elif board[i][j] == "B":
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
                    if random.random() < 0.25:  # 50% chance to place two commands
                        instructions[i][j][0] = str(random.choice(list(commands.keys())))
                        budget -= commands[instructions[i][j][0]]
                        if budget <= 0:
                            break
                    if random.random() < 0.25:  # 50% chance to place two commands
                        instructions[i][j][1] = str(random.choice(list(commands.keys())))
                        budget -= commands[instructions[i][j][1]]
                else:
                    if random.random() < 0.25:  # 50% chance to place two commands
                        # if it's not either high value or low value building, then don't place SP command since 
                        # it doesn't make sense to stomp on non-building tiles
                        random_command = str(random.choice(list(commands.keys())))
                        while random_command == "SP":
                            random_command = str(random.choice(list(commands.keys())))
                        instructions[i][j][0] = random_command
                        budget -= commands[instructions[i][j][0]]
    
    # print the instructions for testing purposes
    print("Generated Instructions:")
    for i in range(5):
        for j in range(5):
            if instructions[i][j] is not None:
                print(f"{instructions[i][j]}" + (" " * (30 - len(str(instructions[i][j])))) , end=" ")
            else:
                print("None" + (" " * 26), end=" ")
        print()  # New line after printing all instructions

    return (board, instructions, budget)