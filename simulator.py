import chess
import numpy as np
from threading import Thread
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
    minmaxk_depth: int
    alpha_beta_depth: int
    nodes_white_avg:float
    nodes_white_sum:int
    nodes_black_avg:float
    nodes_black_sum:int
    time_white_avg:float
    time_white_sum:int
    time_black_avg:float
    time_black_sum:int
    sim_result: str
    expected_result: str
    alg_white: str
    alg_black: str
    num_turns: int
    fen_position: str


Data: list[DataRow] = []
threads: list[Thread] = []
colors = {True: "White", False:"Black", None:"Draw"}


# right now, the simulator runs all the games. maybe we'll change in the future
class Simulator:
    def __init__(self, configuration):
        self.games = configuration['games']
        self.k_values = configuration['k_values']
        self.depths = configuration['depths']
        self.depths_conf = list(configuration['depths_conf'])
        self.turns_limit = configuration['turns_limit']

    def play_game_white(self, minmaxk_depth, alpha_beta_depth, K, board, white_is_minmaxK):
        turns_played = 0
        [nodes_white, nodes_black, time_white, time_black] = [[], [], [], []]
        while not board.is_game_over() and turns_played < self.turns_limit:
            move_white_uci = next_move_k_white(minmaxk_depth, K, board, False) if white_is_minmaxK else next_move(alpha_beta_depth, board, False)
            # print(move_white_uci)
            move_white = chess.Move.from_uci(move_white_uci.uci())
            board.push(move_white)

            # collect data
            white_info_nodes = debug_info_k_white["nodes"] if white_is_minmaxK else debug_info_alpha_beta["nodes"]
            white_info_time = debug_info_k_white["time"] if white_is_minmaxK else debug_info_alpha_beta["time"]

            nodes_white.append(white_info_nodes)
            time_white.append(white_info_time)

            turns_played += 1

            if not board.is_game_over():
                move_black_uci = next_move_k_black(minmaxk_depth, K, board, False) if not white_is_minmaxK else next_move(alpha_beta_depth, board, False)
                # print(move_black_uci)
                move_black = chess.Move.from_uci(move_black_uci.uci())
                board.push(move_black)

                # collect data
                black_info_nodes = debug_info_k_black["nodes"] if not white_is_minmaxK else debug_info_alpha_beta["nodes"]
                black_info_time = debug_info_k_black["time"] if not white_is_minmaxK else debug_info_alpha_beta["time"]

                nodes_black.append(black_info_nodes)
                time_black.append(black_info_time)

                turns_played += 1

        return board, nodes_white, nodes_black, time_white, time_black, turns_played

    def play_game_black(self, minmaxk_depth, alpha_beta_depth, K, board, black_is_minmaxK):
        [nodes_white, nodes_black, time_white, time_black] = [[], [], [], []]
        turns_played = 0
        while not board.is_game_over() and turns_played < self.turns_limit:
            move_black_uci = next_move_k_black(minmaxk_depth, K, board, False) if black_is_minmaxK else next_move(alpha_beta_depth,
                                                                                                                  board,
                                                                                                                  False)
            # print(move_black_uci)
            move_black = chess.Move.from_uci(move_black_uci.uci())
            board.push(move_black)

            # collect data
            black_info_nodes = debug_info_k_black["nodes"] if black_is_minmaxK else debug_info_alpha_beta["nodes"]
            black_info_time = debug_info_k_black["time"] if black_is_minmaxK else debug_info_alpha_beta["time"]

            nodes_black.append(black_info_nodes)
            time_black.append(black_info_time)

            turns_played += 1

            if not board.is_game_over():
                move_white_uci = next_move_k_white(minmaxk_depth, K, board, False) if not black_is_minmaxK else next_move(alpha_beta_depth,
                                                                                                                          board,
                                                                                                                          False)
                # print(move_white_uci)
                move_white = chess.Move.from_uci(move_white_uci.uci())
                board.push(move_white)

                # collect data
                white_info_nodes = debug_info_k_white["nodes"] if not black_is_minmaxK else debug_info_alpha_beta["nodes"]
                white_info_time = debug_info_k_white["time"] if not black_is_minmaxK else debug_info_alpha_beta["time"]

                nodes_white.append(white_info_nodes)
                time_white.append(white_info_time)

                turns_played += 1

        return board, nodes_white, nodes_black, time_white, time_black, turns_played

    def get_game_result(self, board):
        outcome = board.outcome()
        return colors[outcome] if outcome is None else colors[outcome.winner]

    def play_game(self, game_fen, alpha_beta_depth, minmaxk_depth, K, expected_res):
        board = chess.Board(game_fen)
        if board.turn == chess.WHITE:
            # white plays MINMAX-K, black plays classic
            [board, nodes_white, nodes_black, time_white, time_black, turns_played] = self.play_game_white(
                minmaxk_depth, alpha_beta_depth, K, board, white_is_minmaxK=True)
            result = self.get_game_result(board)
            game_summary = DataRow(K,
                                   minmaxk_depth,
                                   alpha_beta_depth,
                                   np.average(nodes_white),
                                   np.sum(nodes_white),
                                   np.average(nodes_black),
                                   np.sum(nodes_black),
                                   np.average(time_white),
                                   np.sum(time_white),
                                   np.average(time_black),
                                   np.sum(time_black),
                                   result,
                                   expected_res,
                                   "MinMax_K",
                                   "Alpha_Beta",
                                   turns_played,
                                   game_fen
                                   )
            print(game_summary)
            Data.append(game_summary)

            # white plays classic, black plays MINMAX-K
            board = chess.Board(game_fen)
            [board, nodes_white, nodes_black, time_white, time_black, turns_played] = self.play_game_white(
                minmaxk_depth, alpha_beta_depth, K, board, white_is_minmaxK=False)
            result = self.get_game_result(board)
            game_summary = DataRow(K,
                                   minmaxk_depth,
                                   alpha_beta_depth,
                                   np.average(nodes_white),
                                   np.sum(nodes_white),
                                   np.average(nodes_black),
                                   np.sum(nodes_black),
                                   np.average(time_white),
                                   np.sum(time_white),
                                   np.average(time_black),
                                   np.sum(time_black),
                                   result,
                                   expected_res,
                                   "Alpha_Beta",
                                   "MinMax_K",
                                   turns_played,
                                   game_fen
                                   )
            print(game_summary)
            Data.append(game_summary)
        else:
            # white plays classic, black plays MINMAX-K
            [board, nodes_white, nodes_black, time_white, time_black, turns_played] = self.play_game_black(
                minmaxk_depth, alpha_beta_depth, K, board,
                black_is_minmaxK=True)
            result = self.get_game_result(board)
            game_summary = DataRow(K,
                                   minmaxk_depth,
                                   alpha_beta_depth,
                                   np.average(nodes_white),
                                   np.sum(nodes_white),
                                   np.average(nodes_black),
                                   np.sum(nodes_black),
                                   np.average(time_white),
                                   np.sum(time_white),
                                   np.average(time_black),
                                   np.sum(time_black),
                                   result,
                                   expected_res,
                                   "Alpha_Beta",
                                   "MinMax_K",
                                   turns_played,
                                   game_fen
                                   )
            print(game_summary)
            Data.append(game_summary)

            # white plays MINMAX-K, black plays classic
            board = chess.Board(game_fen)
            [board, nodes_white, nodes_black, time_white, time_black, turns_played] = self.play_game_black(
                minmaxk_depth, alpha_beta_depth, K, board,
                black_is_minmaxK=False)
            result = self.get_game_result(board)
            game_summary = DataRow(K,
                                   minmaxk_depth,
                                   alpha_beta_depth,
                                   np.average(nodes_white),
                                   np.sum(nodes_white),
                                   np.average(nodes_black),
                                   np.sum(nodes_black),
                                   np.average(time_white),
                                   np.sum(time_white),
                                   np.average(time_black),
                                   np.sum(time_black),
                                   result,
                                   expected_res,
                                   "MinMax_K",
                                   "Alpha_Beta",
                                   turns_played,
                                   game_fen
                                   )
            print(game_summary)
            Data.append(game_summary)

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
        for (game_fen, expected_res) in self.games:
            for K in self.k_values:
                for (alpha_beta_depth, minmaxk_depth) in self.depths_conf:
                    print(f"alpha_beta_depth = {alpha_beta_depth} | minmaxK_ depth = {minmaxk_depth} | K = {K}")
                    # detect who's player turn is, and play accordingly
                    try:
                        print(f"starting thread for:  game = {game_fen} | minmax_depth = {minmaxk_depth} | alpha_beta_deprh = {alpha_beta_depth} | K = {K}")
                        _thread = Thread(target=self.play_game, args=(game_fen, alpha_beta_depth, minmaxk_depth, K, expected_res))
                        _thread.start()
                        threads.append(_thread)
                    except Exception as e:
                        print("Error: unable start thread")

        print(len(threads))

        for _thread in threads:
            _thread.join()
        print("finished running!")
        print(Data)








