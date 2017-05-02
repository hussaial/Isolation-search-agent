"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import sys
import math

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # TODO: finish this function!
    if game.is_loser(player):  
        return float("-inf")

    if game.is_winner(player):  
        return float("inf")
    
    
    '''
    identify the corners of the board and avoid these
    topright_corner = (game.height-1,game.width-1)
    bottomright-corner = (0,game.width-1)
    bottomleft_corner = (0,0)
    topleft_corner = (game.height-1,0)
    '''
    # heuristic function a variation of #my-moves-#opp_moves
    #go down four levels further
    #print('height :',game.height)
    #print('width: ',game.width)
    own_score = 0.0
    opp_score = 0.0
    own_moves = game.get_legal_moves(player)

    opp_moves = game.get_legal_moves(game.get_opponent(player))

    percent_board_unoccupied = (len(game.get_blank_spaces())/(game.height*game.width))*100
    
    #own_move_coverage = (len(game.get_legal_moves(player))/len(game.get_blank_spaces()))*100
    #opp_move_coverage = (len(game.get_opponent(player))/len(game.get_blank_spaces()))*100
    #common_moves = list(set(own_moves).intersection(opp_moves))
    #union_moves = list(set(own_moves).union(opp_moves))
    #opp_diff_moves = len(opp_moves)-len(common_moves)
    #own_diff_moves = len(own_moves)-len(common_moves)
    #corners= [(game.height-1,game.width-1),(0,game.width-1),(0,0),(game.height-1,0)]
    walls = [
            [(0,i) for i in range(game.width)],[(i,0) for i in range(game.height)],[(game.height-1,i) for i in range(game.width)],[(i,game.width-1) for i in range(game.height)]
            ]
#==============================================================================
#     for move in game.get_legal_moves(player):
#         if move in corners:
#             own_score -= 10
#         else:
#             own_score += 1
#     return own_score
#==============================================================================
    centers = [(i,j) for i in range(math.floor(game.width/2)-1,math.floor(game.width/2)+1) for j in range(math.floor(game.height/2)-1,math.floor(game.height/2)+1)]
    
    #print(center)
#==============================================================================
#     for move in own_moves:
#             if move in centers and percent_board_unoccupied<25:
#                 own_score += 30
#             elif move in centers and percent_board_unoccupied>=25 and percent_board_unoccupied<50: 
#                 own_score +=20
#             elif move in centers and percent_board_unoccupied>=50 and percent_board_unoccupied<75:
#                 own_score +=10
#             elif move in centers and percent_board_unoccupied>=75:
#                 own_score +=5
#     return own_score
#==============================================================================
    
#==============================================================================
#     for move in opp_moves:
#             if move in centers and percent_board_unoccupied<25:
#                 opp_score += 30
#             elif move in centers and percent_board_unoccupied>=25 and percent_board_unoccupied<50: 
#                 opp_score +=20
#             elif move in centers and percent_board_unoccupied>=50 and percent_board_unoccupied<75:
#                 opp_score +=10
#             elif move in centers and percent_board_unoccupied>=75:
#                 opp_score +=5
#     return opp_score
#==============================================================================
    
    for move in own_moves:
        for wall in walls:
            if move in wall and percent_board_unoccupied<25:
                own_score -=5   #30
            elif move in wall and (percent_board_unoccupied>=25 and percent_board_unoccupied<50):
                own_score -=10   #20
            elif move in wall and (percent_board_unoccupied>=50 and percent_board_unoccupied<75):
                own_score -=20   #10
            elif move in wall and percent_board_unoccupied>=75:
                own_score -=30   #5
            elif move in centers:
                own_score +=20
            else:
                own_score += 1
    return own_score

    for move in opp_moves:
        for wall in walls:
            if move in wall and percent_board_unoccupied<25:
                opp_score -=30
            elif move in wall and (percent_board_unoccupied>=25 and percent_board_unoccupied<50):
                opp_score -=20
            elif move in wall and (percent_board_unoccupied>=50 and percent_board_unoccupied<75):
                opp_score -=10
            elif move in wall and percent_board_unoccupied>=75:
                opp_score -=5    #91.43
            elif move in centers:
                opp_score +=20
            else:
                opp_score += 1
    return opp_score
  
    return float((own_score)-(2*opp_score))   #float((own_score)-(2*len(opp_moves)))




class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            # Perform Iterative Deepening with depth d

            if not legal_moves:
                return (-1, -1)

            best_move = legal_moves[0] #have to start somewhere
            #most_depth = 0
            if self.iterative: 

                for d in range(0,sys.maxsize):   #IDS goes from 0 to inf
                                     
                    if self.method == 'minimax':
                        _,best_move = self.minimax(game, d)
                    else:
                        _,best_move = self.alphabeta(game, d)
                    
                #most_depth=d
            
            #print('board:', game.to_string())
            return best_move
        
        
        except Timeout:
            # Handle any actions required at timeout, if necessary
            # In case of timeout return the last timeout
            return best_move

        # Return the best move from the last completed search iteration
        #raise NotImplementedError


    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!

        if depth == 0:
            return self.score(game,self), game.get_player_location(self)
        
        else:
            
            if maximizing_player:
                
                best_score = float('-inf')
                for m in game.get_legal_moves():
                    score, move = self.minimax(game.forecast_move(m), depth - 1, False)
                    if score > best_score:
                        best_score = score
                        best_move = m
                        
                #print('score and move:',best_score,best_move)
                return best_score, best_move

            else:   #minimizing player
                
                best_score = float('inf')
                for m in game.get_legal_moves(game.get_opponent(self)):
                    score, move = self.minimax(game.forecast_move(m), depth - 1,  True)
                    if score < best_score:
                        best_score = score
                        best_move = m
                        
                #print('score and move:',best_score,best_move)
                return best_score, best_move
              
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        #legal_moves=game.get_legal_moves()
        best_move=(3,3)      #occupy the middle square 

        if depth == 0:
            return self.score(game,self), game.get_player_location(self)
        
        else:
            
            if maximizing_player:
                
                best_score = float('-inf')
                for m in game.get_legal_moves():
                    score, move = self.alphabeta(game.forecast_move(m), depth - 1, alpha, beta, False)
                    if score > best_score:
                        best_score = score
                        best_move = m
                    alpha = max(alpha,best_score)
                    if beta <= alpha:
                        break #prune
                #print('score and move:',best_score,best_move)
                return best_score, best_move

            else:   #minimizing player
                
                best_score = float('inf')
                for m in game.get_legal_moves(game.get_opponent(self)):
                    score, move = self.alphabeta(game.forecast_move(m), depth - 1, alpha, beta, True)
                    if score < best_score:
                        best_score = score
                        best_move = m
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break   #prune
                #print('score and move:',best_score,best_move)
                return best_score, best_move


