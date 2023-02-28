from itertools import product

sanity_position: list[str] = [("r2qk2r/pb4pp/1n2Pb2/2B2Q2/p1p5/2P5/2B2PPP/RN2R1K1 w - - 1 0", "White")] #white mates in two

clear_white_win_positions: list[str] = [
    ("2r3k1/4br2/p2p2p1/q2Pp1P1/1p6/1P2BP1R/PP6/1K5R w - - 1 0", "White"), # white mates in 2: 1. Rh8+ kg7 2. R1h7#
     ("8/p1r2kpp/2p2p2/r2p1KPP/8/8/8/1R2R3 w - - 1 0", "White"), # white mates in 4: 1. G6+ h:g6 2. H:g6+ kf8 3. Rb8+ rc8 4. R:c8#
    # ("8/p1r2kpp/2p2p2/r2p1KPP/8/8/8/1R2R3 w - - 1 0", "White"), # white mates in 4: 1. Q:e8+ k:e8 2. RAe1+ be4 3. R:e4+ kd8 4. Rf8# TODO: handle duplication
]

white_wins_no_mate: list[str] = [
    ("r3kb1r/ppp1pppp/2n2n2/8/3q4/5BP1/PP2PP1P/RNBQK2R w - - 1 0", "White"), # white gets free queen: 1. B:c6+ b:c6 2. Q:d4!
     ("8/7R/4b1p1/2r1PkN1/5P2/7P/6PK/5r2 w - - 1 0", "White"), # white takes two pieces: 1. G4+ k:f4 2. N:e6+ ke5 3. N:c5
]

equal_positions_white_turn: list[str] = [
    ("r1bq1rk1/1pppbppp/p1n2n2/4p3/B3P3/3P1N2/PPP2PPP/RNBQ1RK1 w - - 1 0", "?"), # Ruy Lopez defence, morphy defence closed
    ("r1bqk2r/1p1nppbp/p2p1np1/8/2BNP3/2N5/PPP2PPP/R1BQR1K1 w kq - 1 0", "?"), # Open Najdorf, Lipintsky attack
]

clear_black_win_positions: list[str] = [
    ("2k3rr/ppp1R3/8/2Pb4/5p2/5B2/PP5P/2R3BK b - - 1 1", "Black"), # black mates in 1: 1. ...b:f3#
     ("6k1/ppR4p/6p1/2P1P1N1/7K/2r4P/P5r1/5R2 b - - 1 1", "Black"), # black mates in 3: 1. ...rc4+ 2. Ne4 r:e4+ 3. Rf4 r:f4# || if black does not check - white mates in 3!
      ("rn1qk3/p4pp1/2P5/4P3/5P2/P2B2Pr/5B1p/1R1Q1R1K b - - 1 1", "Black"), # black mates in 3: 1. ... qd5+ 2. Be4 q:e4+ 3. Qf3 q:f3#
]

black_wins_no_mate: list[str] = [
    ("8/8/1K1n1k2/1N6/2p5/7P/8/8 b - - 1 1", "Black"), # black captures to promotion: 1. ...n:b5 2. k:b5 c3
    ("8/6p1/8/pKQ3q1/P4k2/1P6/8/8 b - - 1 1", "Black"), # black captures to promotion: 1. ...q:c5+ 2. k:c5 g5
    ("2Bk4/6p1/pp3n1p/3p4/3n4/6R1/PP3PPP/6K1 b - - 1 1", "Black"), # black captures bishop and rook in 3: 1. ...ne2+ 2. kf1||h1 n:g3+ 3. kg1 k:c8
]

test_conf = {
    "k_values": [20],
    "depths": [3, 5],
    "depths_conf": product([3, 5], repeat=2),
    "turns_limit": 10,
    "games": sanity_position
}

prod_conf = {
    "k_values": [5, 10, 15, 20],
    "depths":  [3, 5, 7, 9],
    "depths_conf": product([3, 5, 7, 9], repeat=2),
    "turns_limit": 100,
    "games":  sanity_position \
            + clear_white_win_positions \
            + clear_black_win_positions \
            + white_wins_no_mate \
            + black_wins_no_mate \
            + equal_positions_white_turn
}