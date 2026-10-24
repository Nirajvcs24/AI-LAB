def allCombinations(current):
    combinations = []
    zeroIdx = current.index(0)
    moves = []
    row = zeroIdx // 3
    col = zeroIdx % 3
    
    if row > 0: moves.append(-3)   
    if row < 2: moves.append(3)    
    if col > 0: moves.append(-1)    
    if col < 2: moves.append(1)    
    
    for move in moves:
        newIdx = zeroIdx + move
        new_state = list(current)
        new_state[zeroIdx], new_state[newIdx] = new_state[newIdx], new_state[zeroIdx]
        combinations.append(new_state)
        
    return combinations

def solve(stack, visited_states):
    while stack:
        current, level = stack.pop()
        
        if level > 995:
            print("Max level/depth reached without finding a solution.")
            return None

        if goalState == current:
            return current, level
            
        state_tuple = tuple(current)
        if state_tuple in visited_states:
            continue  
            
        visited_states.add(state_tuple)
        
        next_states = allCombinations(current)
        for state in next_states:
            if tuple(state) not in visited_states:
                stack.append((state, level + 1))   
                
    return None

goalState = []
initial = []
print("Enter the initial state:(Enter 0 for empty space)")
for i in range(0, 9):
    num = int(input())
    initial.append(num)

print("Enter the final state:")
for i in range(0,9):
    num = int(input())
    goalState.append(num)

stack = [(initial, 0)]
visited_states = set()

print("Initial state = ", initial)
result = solve(stack, visited_states)

if result:
    solution, total_levels = result
    print("Goal reached:", solution)
    print("Total moves (level):", total_levels)
else:
    print("No solution found.")
