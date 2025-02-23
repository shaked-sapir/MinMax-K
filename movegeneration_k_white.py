from typing import Dict, List, Any
import chess
import sys
import time
from evaluate import evaluate_board, move_value, check_end_game

debug_info_k_white: Dict[str, Any] = {}


MATE_SCORE     = 1000000000
MATE_THRESHOLD =  999000000


def next_move_k_white(depth: int, k:int, board: chess.Board, debug=True) -> chess.Move:
    """
    What is the next best move?
    """
    debug_info_k_white.clear()
    debug_info_k_white["nodes"] = 0
    t0 = time.time()

    move = minimax_root(depth,k, board)

    debug_info_k_white["time"] = time.time() - t0
    if debug == True:
        print(f"white_k_info {debug_info_k_white}")
    return move


def get_ordered_moves(depth: int, k: int, board: chess.Board ) -> List[chess.Move]:
    """
    Get legal moves.
    Attempt to sort moves by best to worst.
    Use piece values (and positional gains/losses) to weight captures.
    """
    end_game = check_end_game(board)

    def orderer(move):
        return move_value(board, move, end_game)

    in_order = sorted(
        board.legal_moves, key=orderer, reverse=(board.turn == chess.WHITE)
    )
    if depth==1:
     return list(in_order)

    size = len(in_order)
    l= list(in_order)
    if board.turn == chess.WHITE and k < size:
     del l[size-k:]
    return l


def minimax_root(depth: int, k: int, board: chess.Board) -> chess.Move:
    """
    What is the highest value move per our evaluation function?
    """
    # White always wants to maximize (and black to minimize)
    # the board score according to evaluate_board()
    maximize = board.turn == chess.WHITE
    best_move = -float("inf")
    if not maximize:
        best_move = float("inf")

    moves = get_ordered_moves(depth,k,board)
    best_move_found = moves[0]
    i = -1
    for move in moves:
        i+=1
        board.push(move)
        # Checking if draw can be claimed at this level, because the threefold repetition check
        # can be expensive. This should help the bot avoid a draw if it's not favorable
        # https://python-chess.readthedocs.io/en/latest/core.html#chess.Board.can_claim_draw
        if board.can_claim_draw():
            value = 0.0
        else:
            value = minimax(depth - 1,k, board, -float("inf"), float("inf"), not maximize)
        board.pop()
        if maximize and value >= best_move:
            best_move = value
            best_move_found = move
        elif not maximize and value <= best_move:
            best_move = value
            best_move_found = move

    return best_move_found


def minimax(
    depth: int,
    k:int,
    board: chess.Board,
    alpha: float,
    beta: float,
    is_maximising_player: bool,
) -> float:
    """
    Core minimax logic.
    https://en.wikipedia.org/wiki/Minimax
    """
    debug_info_k_white["nodes"] += 1

    if board.is_checkmate():
        # The previous move resulted in checkmate
        return -MATE_SCORE if is_maximising_player else MATE_SCORE
    # When the game is over and it's not a checkmate it's a draw
    # In this case, don't evaluate. Just return a neutral result: zero
    elif board.is_game_over():
        return 0

    if depth == 0:
        return evaluate_board(board)

    if is_maximising_player:
        best_move = -float("inf")
        moves = get_ordered_moves(depth,k,board)
        for move in moves:
            board.push(move)
            curr_move = minimax(depth - 1,k, board, alpha, beta, not is_maximising_player)
            # Each ply after a checkmate is slower, so they get ranked slightly less
            # We want the fastest mate!
            if curr_move > MATE_THRESHOLD:
                curr_move -= 1
            elif curr_move < -MATE_THRESHOLD:
                curr_move += 1
            best_move = max(
                best_move,
                curr_move,
            )
            board.pop()
            alpha = max(alpha, best_move)
            if beta <= alpha:
                return best_move
        return best_move
    else:
        best_move = float("inf")
        moves = get_ordered_moves(depth, k,board)
        for move in moves:
            board.push(move)
            curr_move = minimax(depth - 1,k, board, alpha, beta, not is_maximising_player)
            if curr_move > MATE_THRESHOLD:
                curr_move -= 1
            elif curr_move < -MATE_THRESHOLD:
                curr_move += 1
            best_move = min(
                best_move,
                curr_move,
            )
            board.pop()
            beta = min(beta, best_move)
            if beta <= alpha:
                return best_move
        return best_move
