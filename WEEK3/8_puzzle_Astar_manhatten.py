import heapq

GOAL_STATE = (1, 2, 3, 
              4, 5, 6, 
              7, 8, 0)

GOAL_POSITIONS = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    4: (1, 0), 5: (1, 1), 6: (1, 2),
    7: (2, 0), 8: (2, 1), 0: (2, 2)
}

def get_manhattan_distance(state):
    distance = 0
    for i, tile in enumerate(state):
        if tile != 0:
            current_row, current_col = divmod(i, 3)
            goal_row, goal_col = GOAL_POSITIONS[tile]
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

def get_neighbors(state):
    neighbors = []
    zero_index = state.index(0)
    row, col = divmod(zero_index, 3)

    directions = [
        (-1, 0, "Up"),
        (1, 0, "Down"),
        (0, -1, "Left"),
        (0, 1, "Right")
    ]
    
    for dr, dc, move in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_zero_index = new_row * 3 + new_col
            
            state_list = list(state)
            state_list[zero_index], state_list[new_zero_index] = state_list[new_zero_index], state_list[zero_index]
            
            neighbors.append((tuple(state_list), move))
            
    return neighbors

def a_star_search(start_state):
    if start_state == GOAL_STATE:
        return [start_state]
    counter = 0
    h = get_manhattan_distance(start_state)
    pq = [(h, counter, 0, start_state, [start_state])]
    
    g_scores = {start_state: 0}
    
    while pq:
        f, _, g, current_state, path = heapq.heappop(pq)
        
        if current_state == GOAL_STATE:
            return path
        
        if g > g_scores.get(current_state, float('inf')):
            continue
        
        for neighbor, move in get_neighbors(current_state):
            new_g = g + 1
            
            if new_g < g_scores.get(neighbor, float('inf')):
                g_scores[neighbor] = new_g
                new_h = get_manhattan_distance(neighbor)
                new_f = new_g + new_h
                counter += 1
                
                heapq.heappush(pq, (new_f, counter, new_g, neighbor, path + [neighbor]))
                
    return None

def print_board(state):
    for i in range(0, 9, 3):
        row = [str(tile) if tile != 0 else ' ' for tile in state[i:i+3]]
        print(" ".join(row))
    print("-" * 9)

if __name__ == "__main__":
    initial_state = (1, 2, 3, 
                     4, 0, 5, 
                     7, 8, 6)
    
    print("Initial State:")
    print_board(initial_state)
    
    solution_path = a_star_search(initial_state)
    
    if solution_path:
        print(f"Solution found in {len(solution_path) - 1} moves!\n")
        print("Steps:")
        for step, state in enumerate(solution_path):
            print(f"Step {step}:")
            print_board(state)
    else:
        print("No solution exists for this initial state.")
