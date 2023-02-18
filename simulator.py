import chess
import numpy as np
from dataclasses import dataclass
from movegeneration import next_move
from movegeneration import debug_info as debug_info_alpha_beta
from movegeneration_k_black import next_move_k_black
from movegeneration_k_black import debug_info as debug_info_k_black
from movegeneration_k_white import next_move_k_white
from movegeneration_k_white import debug_info as debug_info_k_white

@dataclass
class DataRow:
    K: int
    depth: int
    nodes_white_avg:float
    nodes_white_sum:int
    nodes_black_avg:float
    nodes_black_sum:int
    time_white_avg:float
    time_white_sum:int
    time_black_avg:float
    time_black_sum:int
    win: str
    alg_white: str
    alg_black: str


games: list[str] = ["r2qk2r/pb4pp/1n2Pb2/2B2Q2/p1p5/2P5/2B2PPP/RN2R1K1 w - - 1 0"]  # TODO: insert games in FEN format
k_values: list[int] = [1, 5, 10, 20]  # TODO: define the exact values
depths: list[int] = [2, 4, 6, 8]  # TODO> define the exact values
colors = {True: "White", False:"Black", None:"Draw"}
Data : list[DataRow] = []


# right now, the simulator runs all the games. maybe we'll change in the future
class Simulator:
    def __init__(self):
        self.games = games
        self.k_values = k_values
        self.depths = depths

    def run(self):

        """
        pseudo-code:

        0.for game in self.games:

        1 foreach k in k_values:

        1.1.foreach depth in depths: (means, we run all possible configurations of depth + k)

        1.1.1. while game is not over:
        1.1.1.1. white plays MINMAX-K(K, depth), black plays classic(depth)
        1.1.1.2. board = curr_board <--- next_move (either white / black)
        1.1.2. save result - 'A'
        1.1.3. reset game to original position

        1.1.4. while game is not over:
        1.1.4.1. white plays classic(depth),  black plays MINMAX-K(K, depth)
        1.1.4.2. board = curr_board <--- next_move (either white / black)
        1.1.5. save result - 'B'

        1.1.6 report 'A' + 'B'

        """

        for game_fen in self.games:
            for K in self.k_values:
                for depth in self.depths:

                   # white plays MINMAX-K, black plays classic
                   board = chess.Board(game_fen)
                   nodes_white=[]
                   nodes_black=[]
                   time_white=[]
                   time_black=[]
                   while (not board.is_game_over()):
                       # next move of MINMAX-K(K, depth)
                       move_white_uci = next_move_k_white(depth,K,board)
                       move_white = chess.Move.from_uci(move_white_uci.uci())
                       board.push(move_white)

                       #collect data
                       nodes_white.append(debug_info_k_white["nodes"])
                       time_white.append(debug_info_k_white["time"])

                       if(not board.is_game_over()):
                           # next_move of alpha-beta(depth)
                           move_black_uci = next_move(depth, board)
                           move_black = chess.Move.from_uci(move_black_uci.uci())
                           board.push(move_black)

                           # collect data
                           nodes_black.append(debug_info_alpha_beta["nodes"])
                           time_black.append(debug_info_alpha_beta["time"])

                   result=colors[board.outcome().winner]
                   Data.append(DataRow(K,
                                       depth,
                                       np.average(nodes_white),
                                       np.sum(nodes_white),
                                       np.average(nodes_black),
                                       np.sum(nodes_black),
                                       np.average(time_white),
                                       np.sum(time_white),
                                       np.average(time_black),
                                       np.sum(time_black),
                                       result,
                                       "MinMax_K",
                                       "Alpha_Beta"
                                       ))


                   # white plays classic, black plays MINMAX-K
                   board = chess.Board(game_fen)

        print(Data)

