import random

constraints = [
    (0, 1), (1, 2), (2, 3), (2, 5), (2, 6),
    (3, 5), (3, 4), (4, 5), (5, 6)
]

def calculate_satisfied_constraints(state):
    satisfied = 0
    for region1, region2 in constraints:
        if state[region1] != state[region2]:
            satisfied += 1
    return satisfied

def generate_neighbors(state):
    neighbors = []
    for region_index in range(len(state)):
        current_color = state[region_index]
        
        for new_color in [1, 2, 3]:
            if new_color != current_color:
                new_state = state[:]
                new_state[region_index] = new_color
                neighbors.append(new_state)
    return neighbors

def steepest_hill_climbing(initial_state):
    current_state = initial_state
    current_score = calculate_satisfied_constraints(current_state)
    
    while True:
        neighbors = generate_neighbors(current_state)
        best_neighbor = None
        best_score = current_score

        for neighbor in neighbors:
            neighbor_score = calculate_satisfied_constraints(neighbor)
            if neighbor_score > best_score:
                best_score = neighbor_score
                best_neighbor = neighbor

        if best_neighbor is None or best_score <= current_score:
            return current_state, current_score
        
        current_state = best_neighbor
        current_score = best_score

if __name__ == "__main__":
    initial_state = [random.randint(1, 3) for _ in range(7)]
    print("Initial State:", initial_state)
    print("Initial Satisfied Constraints:", calculate_satisfied_constraints(initial_state))

    final_state, final_score = steepest_hill_climbing(initial_state)
    print("Final State:", final_state)
    print("Final Satisfied Constraints:", final_score)
