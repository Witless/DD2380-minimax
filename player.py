#!/usr/bin/env python3
import random

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR
from search_algorithms import minimax


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate first message (Do not remove this line!)
        first_msg = self.receiver()

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def search_best_next_move(self, initial_tree_node):
        """
        Use minimax (and extensions) to find best possible next move for player 0 (green boat)
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str

        :keyword initial_tree_node should be renamed to current_state_first_tree_node for clarity
        """

        best_move_int = 0
        best_value = float('-inf')
        min_value = float('inf')

        # Get all the possible next moves by our player (0, Green boat) by calling the next function, then apply minimax on each of the moves and select move with max value
        child_nodes = initial_tree_node.compute_and_get_children()

        for child_node in child_nodes:

            #The current 'child_node' represents the state after we make a move
            #Now we call minimax to evaluate this branch with value '1' as it's the other player's (Red boat) turns

            value = minimax(1, child_node, 2)


            print(f"[Move {child_node.move}] eval: {value}")

            if value > best_value:
                best_value = value
                best_move_int = child_node.move
            if value < min_value:
                min_value = value

        #The odd is very low, but it could happen that the max and min value are equal. In that case go random move
        if min_value == best_value:
            best_move_int = random.randrange(5)

        return ACTION_TO_STR[best_move_int]


