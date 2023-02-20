import chess
import numpy as np
from dataclasses import dataclass
from movegeneration import next_move
from movegeneration import debug_info as debug_info_alpha_beta
from movegeneration_k_black import next_move_k_black
from movegeneration_k_black import debug_info_k_black
from movegeneration_k_white import next_move_k_white
from movegeneration_k_white import debug_info_k_white


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
k_values: list[int] = [0, 5, 10, 15]  # TODO: define the exact values
depths: list[int] = [3]  # TODO> define the exact values
colors = {True: "White", False:"Black", None:"Draw"}
Data : list[DataRow] = []


clear_white_win_positions = [
    "2r3k1/4br2/p2p2p1/q2Pp1P1/1p6/1P2BP1R/PP6/1K5R w - - 1 0", # white mates in 2: 1. Rh8+ kg7 2. R1h7#
    "8/p1r2kpp/2p2p2/r2p1KPP/8/8/8/1R2R3 w - - 1 0", # white mates in 4: 1. G6+ h:g6 2. H:g6+ kf8 3. Rb8+ rc8 4. R:c8#
    "8/p1r2kpp/2p2p2/r2p1KPP/8/8/8/1R2R3 w - - 1 0", # white mates in 4: 1. Q:e8+ k:e8 2. RAe1+ be4 3. R:e4+ kd8 4. Rf8#
]

white_wins_no_mate = [
    "r3kb1r/ppp1pppp/2n2n2/8/3q4/5BP1/PP2PP1P/RNBQK2R w - - 1 0", # white gets free queen: 1. B:c6+ b:c6 2. Q:d4!
    "P1P/RNBQK2R w - - 1 0", # white takes queen in 3: 1. Q:g6+ kh8 2. Qh6+ nh7 3.Q:c6 OR 2. ...kg8 3. Rg1+ b:g1 4. R:g1+ and mate in 3
    "8/7R/4b1p1/2r1PkN1/5P2/7P/6PK/5r2 w - - 1 0", # white takes two pieces: 1. G4+ k:f4 2. N:e6+ ke5 3. N:c5
]

equal_positions_white_turn = [
    "r1bq1rk1/1pppbppp/p1n2n2/4p3/B3P3/3P1N2/PPP2PPP/RNBQ1RK1 w - - 1 0", # Ruy Lopez defence, morphy defence closed
    "r1bqk2r/1p1nppbp/p2p1np1/8/2BNP3/2N5/PPP2PPP/R1BQR1K1 w kq - 1 0", # Open Najdorf, Lipintsky attack
]

clear_black_win_positions = [
    "2k3rr/ppp1R3/8/2Pb4/5p2/5B2/PP5P/2R3BK b - - 1 1", # black mates in 1: 1. ...b:f3#
    "6k1/ppR4p/6p1/2P1P1N1/7K/2r4P/P5r1/5R2 b - - 1 1", # black mates in 3: 1. ...rc4+ 2. Ne4 r:e4+ 3. Rf4 r:f4#
    "rn1qk3/p4pp1/2P5/4P3/5P2/P2B2Pr/5B1p/1R1Q1R1K b - - 1 1", # black mates in 3: 1. ... qd5+ 2. Be4 q:e4+ 3. Qf3 q:f3#
]

black_wins_no_mate = [
    "8/8/1K1n1k2/1N6/2p5/7P/8/8 b - - 1 1", # black captures to promotion: 1. ...n:b5 2. k:b5 c3
    "8/6p1/8/pKQ3q1/P4k2/1P6/8/8 b - - 1 1", # black captures to promotion: 1. ...q:c5+ 2. k:c5 g5
    "2Bk4/6p1/pp3n1p/3p4/3n4/6R1/PP3PPP/6K1 b - - 1 1", # black captures bishop and rook in 3: 1. ...ne2+ 2. kf1||h1 n:g3+ 3. kg1 k:c8
]



# right now, the simulator runs all the games. maybe we'll change in the future
class Simulator:
    def __init__(self):
        self.games = games
        self.k_values = k_values
        self.depths = depths

    def play_turn_white(self, depth, K, board, white_is_minmaxK):
        [nodes_white, nodes_black, time_white, time_black] = [[], [], [], []]
        while not board.is_game_over():
            move_white_uci = next_move_k_white(depth, K, board, False) if white_is_minmaxK else next_move(depth, board, False)
            print(move_white_uci)
            move_white = chess.Move.from_uci(move_white_uci.uci())
            board.push(move_white)

            # collect data
            white_info_nodes = debug_info_k_white["nodes"] if white_is_minmaxK else debug_info_alpha_beta["nodes"]
            white_info_time = debug_info_k_white["time"] if white_is_minmaxK else debug_info_alpha_beta["time"]

            nodes_white.append(white_info_nodes)
            time_white.append(white_info_time)

            if not board.is_game_over():
                move_black_uci = next_move_k_black(depth, K, board, False) if not white_is_minmaxK else next_move(depth, board, False)
                print(move_black_uci)
                move_black = chess.Move.from_uci(move_black_uci.uci())
                board.push(move_black)

                # collect data
                black_info_nodes = debug_info_k_black["nodes"] if not white_is_minmaxK else debug_info_alpha_beta["nodes"]
                black_info_time = debug_info_k_black["time"] if not white_is_minmaxK else debug_info_alpha_beta["time"]

                nodes_black.append(black_info_nodes)
                time_black.append(black_info_time)

        return board, nodes_white, nodes_black, time_white, time_black


    def play_turn_black(self, depth, K, board, black_is_minmaxK):
        [nodes_white, nodes_black, time_white, time_black] = [[], [], [], []]
        while not board.is_game_over():
            move_black_uci = next_move_k_black(depth, K, board, False) if black_is_minmaxK else next_move(depth,
                                                                                                              board,
                                                                                                              False)
            print(move_black_uci)
            move_black = chess.Move.from_uci(move_black_uci.uci())
            board.push(move_black)

            # collect data
            black_info_nodes = debug_info_k_black["nodes"] if black_is_minmaxK else debug_info_alpha_beta["nodes"]
            black_info_time = debug_info_k_black["time"] if black_is_minmaxK else debug_info_alpha_beta["time"]

            nodes_black.append(black_info_nodes)
            time_black.append(black_info_time)


            if not board.is_game_over():
                move_white_uci = next_move_k_white(depth, K, board, False) if not black_is_minmaxK else next_move(depth,
                                                                                                              board,
                                                                                                              False)
                print(move_white_uci)
                move_white = chess.Move.from_uci(move_white_uci.uci())
                board.push(move_white)

                # collect data
                white_info_nodes = debug_info_k_white["nodes"] if not black_is_minmaxK else debug_info_alpha_beta["nodes"]
                white_info_time = debug_info_k_white["time"] if not black_is_minmaxK else debug_info_alpha_beta["time"]

                nodes_white.append(white_info_nodes)
                time_white.append(white_info_time)

        return board, nodes_white, nodes_black, time_white, time_black

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

                   # detect who's player turn is, and play accordingly

                   board = chess.Board(game_fen)
                   if board.turn == chess.WHITE:
                       # white plays MINMAX-K, black plays classic
                       [board, nodes_white, nodes_black, time_white, time_black] = self.play_turn_white(depth, K, board, white_is_minmaxK=True)
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
                       [board, nodes_white, nodes_black, time_white, time_black] = self.play_turn_white(depth, K, board, white_is_minmaxK=False)
                       result = colors[board.outcome().winner]
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
                                           "Alpha_Beta",
                                           "MinMax_K"
                                           ))
                   else:
                        # white plays MINMAX-K, black plays classic
                        [board, nodes_white, nodes_black, time_white, time_black] = self.play_turn_black(depth, K, board,
                                                                                                         black_is_minmaxK=True)
                        result = colors[board.outcome().winner]
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
                                            "Alpha_Beta",
                                            "MinMax_K"
                                            ))

                        # white plays classic, black plays MINMAX-K
                        board = chess.Board(game_fen)
                        [board, nodes_white, nodes_black, time_white, time_black] = self.play_turn_black(depth, K, board,
                                                                                                         black_is_minmaxK=False)
                        result = colors[board.outcome().winner]
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

        print(Data)





