def calculate_positional_value(state, player_id):
    hook_pos = state.get_hook_positions()[player_id]
    fish_positions = state.get_fish_positions()
    fish_scores = state.get_fish_scores()
    player_caught = state.get_caught()[player_id]
    max_positional_value = 0

    #Check for fish currently on the rod, this will give us points if we bring it up
    if player_caught != -1 and player_caught is not None:
        #A guaranteed catch is the highest possible positional value
        return fish_scores.get(player_caught, 0) * 2  #Multiply by 2 to favor bringing up the caught fish

    #Iterate over all uncaught fish to find the best target
    for fish_id, pos in fish_positions.items():
        score = fish_scores.get(fish_id, 1)

        #Calculate X-distance (wrapped)
        dx_raw = abs(hook_pos[0] - pos[0])
        dx = min(dx_raw, 20 - dx_raw)

        #Calculate Y-distance
        dy = abs(hook_pos[1] - pos[1])

        distance = dx + dy

        #Calculate potential value (Score / (Distance + 1))
        value = score / (distance + 1)

        max_positional_value = max(max_positional_value, value)

    return max_positional_value



#The heuristic is based on the difference in score between the two players and the positional advantage of the player with respect to the observed fishes and their values (scores)
def minimax_heuristic(node):

    #'imp' here is the importance we want to give to the positional difference in the heuristic, higher -> the next move decision will lean more toward the current positions
    #Interesting to play with its values, since score_diff usually tells us very little information because our depth can't be very high (else the program crashes) and we can't reach end states
    imp = 1.0

    #Catched fishes score difference
    score_diff = node.state.player_scores[0] - node.state.player_scores[1]

    #Calculate positional advantage
    pos_0 = calculate_positional_value(node.state, 0)
    pos_1 = calculate_positional_value(node.state, 1)

    #Weight the positional advantage
    positional_diff = pos_0 - pos_1

    return score_diff + imp * positional_diff



# Minimax implementation. Goes through all possible children nodes given a node. Ready to implement Alpha-beta pruning and reduce computing times
def minimax(player, node, depth):

    children = node.compute_and_get_children()

    #The base case checks for the maximum desired depth we want to reach, and if there are more available children to the current node
    #Last condition is likely to happen when the game is about to end
    if depth == 0 or not children:
        heuristic = minimax_heuristic(node)
        return heuristic

    #Debug traces to understand how the application works
    #print(f"[Player] {node.state.get_player()}")
    #print(f"[Move]  {node.children[0].move}  [Player] {node.children[0].state.get_player()}  [Observation]     {node.children[0].observations}")
    #print(f"[Obs_Len] {len(node.children[0].observations)}")

    #Our green boat has an internal identifier (int) with value 0
    if player == 0:
        best_heuristic = float('-inf')
        for child in children:
            result = minimax(1, child, depth-1)
            if result > best_heuristic:
                best_heuristic = result
        return best_heuristic

    else:
        best_heuristic = float('inf')
        for child in children:
            result = minimax(0, child, depth-1)
            if result < best_heuristic:
                best_heuristic = result
        return best_heuristic