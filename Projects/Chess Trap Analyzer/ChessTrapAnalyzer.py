import berserk
from stockfish import Stockfish
import chess
import math
import json
import time
import datetime

LICHESS_REQUEST_DELAY = 0.25

MATE_CP = 3000
CP_PER_MOVE_TO_MATE = 100

RELEVANT_RATINGS = ["0", "1000", "1200", "1400", "1600", "1800"]
RELEVANT_SPEEDS = ["ultraBullet", "bullet", "blitz", "rapid", "classical"]

WHITE_MATE_IN_3 = "r1bq1k1r/ppppRppp/8/8/2BP4/B4N2/P4PPP/b2Q2K1 w - - 1 13"
BLACK_MATE_IN_1 = "rnbqkbnr/pppp1ppp/8/4p3/5PP1/8/PPPPP2P/RNBQKBNR b KQkq - 0 2"
BLACK_WINNING = "rnbqk2r/pppp1ppp/5n2/2b5/2P5/4PK2/PP4PP/RNBQ1BNR b kq - 4 6"
WHITE_TO_MOVE = "r1bqk2r/pppp1ppp/2n2n2/2b5/2BpP3/2P2N2/PP3PPP/RNBQK2R w KQkq - 0 6"

MEMO_FN = "/Users/juliushoang/Repos/Python/Projects/Chess Trap Analyzer/italian_trap_memo.json"
ANALYSIS_FN = "/Users/juliushoang/Repos/Python/Projects/Chess Trap Analyzer/italian_trap_analysis.json"

MY_MOVE_DEPTH_CUTOFF = 1
MY_MOVE_CP_MARGIN = 150 
MY_MOVE_MIN_CP = -250
# If my possible moves are analyzed to at least the depth cutoff, and there are moves that 
# evaluate to a score that is lower than the highest-scoring evaluation by a difference
# of more than the centipawn margin, throw those moves out

OPP_MOVE_MIN_GAMES = 300
OPP_TO_MOVE_PERCENTAGE_CUTOFF = .80

GLOBAL_START_T = time.perf_counter()


def get_move_percentage(games, move):
    total_games_at_pos = games["white"] + games["draws"] + games["black"]
    num_games_after_move = move["white"] + move["draws"] + move["black"]
    return num_games_after_move / total_games_at_pos


def get_fen_after_san(fen, san):
    board = chess.Board(fen)
    board.push_san(san)
    return board.fen()

def get_fen_after_uci(fen, uci):
    board = chess.Board(fen)
    board.push_san(uci)
    return board.fen()

def white_to_move(fen):
    board = chess.Board(fen)
    return board.turn

def fen_to_move_number(fen):
    board = chess.Board(fen)
    return f"{board.fullmove_number}{"." if board.turn else "..."}"

def log_progress(progress):
    elapsed_time = time.perf_counter() - GLOBAL_START_T
    if progress < 0.0001:
        print("Progress: 0 Time left: ??")
    else:
        expected_t = seconds=(1- progress) * elapsed_time / progress
        formatted_t = time.strftime('%H:%M:%S', time.gmtime(expected_t))
        print(f"Progress: {progress*100:5.2f}% Time left: {formatted_t}")




def get_engine_eval(fen):
    # Try to get lichess cloud eval
    try:
        engine_eval = client.analysis.get_cloud_evaluation(fen)["pvs"][0]
        time.sleep(LICHESS_REQUEST_DELAY) 
        cp = engine_eval.get("cp")
        if cp is not None:
            return cp
        mate = engine_eval.get("mate")
        if mate is not None:
            return math.copysign(MATE_CP, mate) - mate * CP_PER_MOVE_TO_MATE
        else:
            raise ValueError(f"No centipawn or mate value found in {engine_eval}")
            
    except:
        # No cloud eval found; use SF
        stockfish.set_fen_position(fen)
        engine_eval = stockfish.get_evaluation()
        if engine_eval["type"] == "cp":
            return engine_eval["value"]
        elif engine_eval["type"] == "mate":
            mate = engine_eval["value"]
            return math.copysign(MATE_CP, mate) - mate * CP_PER_MOVE_TO_MATE


def recursive_weighted_eval(fen, me_to_move=True, depth=10, memo=None, progress=0, progress_step=1):
    """
    Get the weighted eval of a position, calculated by taking of the sum of 
    the evaluations of the opponent's responses times the percentage played in 
    lichess games.


    :param fen: FEN of pos to analyse
    :type fen: str
    :param me_to_move: If I have the move, or if the opponent has the move, defaults to True
    :type me_to_move: bool, optional
    :param depth: depth to analyze, defaults to 10
    :type depth: int, optional
    :param memo: cache of evaluations, defaults to None
    :type memo: dict, optional
    e.g.
    memo = {"r1bqk2r/pppp1ppp/2n2n2/2b1p3/2BPP3/2P2N2/PP3PPP/RNBQK2R b KQkq - 0 5": {
                "cp" = 360,
                "depth" = 3},

            }
    """

    starting_progress = progress
    # Memo case
    if memo.get(fen) is not None and memo[fen]["depth"] >= depth:
        print(f"Hit match in memo: {fen}: {memo[fen]}")
        log_progress(progress)
        return memo[fen]["cp"]
    
    # Base case. If max depth reached, do normal engine eval
    if depth <= 0:
        engine_eval = get_engine_eval(fen)
        memo[fen] = {"cp": engine_eval,
                    "depth": depth}
        return engine_eval

    # Recursive case
    games = client.opening_explorer.get_lichess_games(position=fen, ratings=RELEVANT_RATINGS, speeds=RELEVANT_SPEEDS)
    time.sleep(LICHESS_REQUEST_DELAY)
    moves = games["moves"]
    # If I have the move, the evaluation is the max of all candidate moves
    if me_to_move:
        weighted_evals = []
        top_moves = []
        # Go through all moves recursively
        for i in range(MAX_ME_MOVES):
            if i == len(moves):
                break
            move = moves[i]
            print(f"Evaluating move {fen_to_move_number(fen)} {move["san"]}")
            log_progress(progress)
            new_fen = get_fen_after_uci(fen, move["uci"])
            weighted_eval_after_move = recursive_weighted_eval(new_fen, 
                                                               me_to_move=not me_to_move, 
                                                               depth=depth-1, 
                                                               memo=memo,
                                                               progress=progress,
                                                               progress_step=progress_step/MAX_ME_MOVES)
            weighted_evals.append(weighted_eval_after_move)
            top_moves.append((move["san"], weighted_eval_after_move))
            progress = starting_progress + (i+1)/MAX_ME_MOVES * progress_step

        if white_to_move(fen):
            weighted_eval_current_pos = max(weighted_evals)
        else:
            weighted_eval_current_pos = min(weighted_evals)

        memo[fen] = {"cp": weighted_eval_current_pos,
                     "depth": depth,
                     "top_moves": top_moves}
        return weighted_eval_current_pos

    # If opponent has the move, the evaluation is the weighted average of the candidate moves
    else:
        weighted_evals = []
        cumulative_percentage = 0
        top_moves = []
        # Get nsubset of moves under cumulative percentage
        moves_to_consider = []
        for move in moves:
            move_percentage = get_move_percentage(games, move)
            top_moves.append((move["san"], int(move_percentage*100)))
            moves_to_consider.append(move)
            cumulative_percentage += move_percentage
            # Only iterate until we reach the percentage cutoff
            if cumulative_percentage > OPP_TO_MOVE_PERCENTAGE_CUTOFF:
                break

        num_moves_to_consider = len(moves_to_consider)
        for i in range(num_moves_to_consider):
            move = moves_to_consider[i]
            print(f"Evaluating move {fen_to_move_number(fen)} {move["san"]}")
            log_progress(progress)
            new_fen = get_fen_after_uci(fen, move["uci"])
            weighted_eval_after_move = recursive_weighted_eval(new_fen, 
                                                               me_to_move=not me_to_move, 
                                                               depth=depth-1, 
                                                               memo=memo,
                                                               progress=progress,
                                                               progress_step=progress_step/num_moves_to_consider) * move_percentage
            weighted_evals.append(weighted_eval_after_move)
            progress = starting_progress + (i+1)/num_moves_to_consider * progress_step
            
        weighted_eval_current_pos = int(sum(weighted_evals))
        memo[fen] = {"cp": weighted_eval_current_pos,
                     "depth": depth,
                     "top_moves": top_moves}

        return weighted_eval_current_pos


def run_analysis(fen, me_to_move=True, max_depth=6):
    try:
        with open(MEMO_FN, 'r') as file:
            memo = json.load(file)
    except:
        memo = dict()
    depth = 0
    while depth <= max_depth:
        try:
            global GLOBAL_START_T 
            GLOBAL_START_T = time.perf_counter()
            print(f"\n\nStarting analysis at depth {depth}")
            weighted_eval = recursive_weighted_eval(fen, me_to_move=me_to_move, depth=depth, memo=memo, progress=0, progress_step=1)
            print(f"\nEvaluation: {weighted_eval}")
            print(f"\nFinished analysis at depth {depth} in {time.perf_counter()-GLOBAL_START_T:.2f} seconds")
        except Exception as e:
            with open(MEMO_FN, "w") as f:
                json.dump(memo, f, indent=4)
            raise e
        with open(MEMO_FN, "w") as f:
            json.dump(memo, f, indent=4)
        depth += 1
    

def recursive_analysis_str(fen, me_to_move=True, depth=4, tabs=0):
    with open(MEMO_FN, 'r') as file:
        memo = json.load(file)

    # memo
    if memo.get(fen) is not None and memo[fen].get("top_moves") is not None:
        moves = memo[fen]["top_moves"]
        print(f"Hit memo case {fen_to_move_number(fen)} {moves}")

        out=""
        if me_to_move:
            sorted_moves = sorted(moves, key = lambda x: x[1])
            if memo[fen]["depth"] >= MY_MOVE_DEPTH_CUTOFF:
                max_cp = sorted_moves[-1][1]
                sorted_moves = [move for move in sorted_moves if max_cp - move[1] < MY_MOVE_CP_MARGIN and move[1] > MY_MOVE_MIN_CP]
            moves = sorted_moves
            # remove 
            if white_to_move(fen):
                top_moves = sorted_moves[:-ME_TO_MOVE_ANALYSIS-1:-1]
            else:   
                top_moves = sorted_moves[:ME_TO_MOVE_ANALYSIS]

            for san, cp in top_moves:
                new_fen = get_fen_after_san(fen, san)
                line = "\t" * tabs + f"{fen_to_move_number(fen)} {san} (cp_trap={cp}) (cp_eng={get_engine_eval(new_fen)})\n"
                out += line
                out += recursive_analysis_str(new_fen, me_to_move=not me_to_move, depth=depth-1, tabs=tabs+1)
            return out
        else:
            for san, percentage in moves:
                new_fen = get_fen_after_san(fen, san)
                line = "\t" * tabs + f"{fen_to_move_number(fen)} {san} ({percentage}%)\n"
                out += line
                out += recursive_analysis_str(new_fen, me_to_move=not me_to_move, depth=depth-1, tabs=tabs+1)
            return out

            
    # base
    if depth <= 0:
        return ""
    
    # recursive
    games = client.opening_explorer.get_lichess_games(position=fen, ratings=RELEVANT_RATINGS, speeds=RELEVANT_SPEEDS)
    time.sleep(LICHESS_REQUEST_DELAY)
    moves = games["moves"]

    if me_to_move:
        weighted_evals = []
        # Go through all moves recursively
        for i in range(MAX_ME_MOVES):
            move = moves[i]
            print(f"Evaluating move {fen_to_move_number(fen)} {move["san"]}")
            new_fen = get_fen_after_uci(fen, move["uci"])
            try:
                weighted_eval_after_move = recursive_weighted_eval(new_fen, 
                                                                me_to_move=not me_to_move, 
                                                                depth=1, 
                                                                memo=memo)
            except Exception as e:
                with open(MEMO_FN, "w") as f:
                    json.dump(memo, f, indent=4)
                raise e
            weighted_evals.append(
                {
                    "move": move,
                    "cp": weighted_eval_after_move
                }
            )
        
        sorted_moves = sorted(weighted_evals, key=lambda item: item["cp"])
        if white_to_move(fen):
            top_moves = sorted_moves[:-ME_TO_MOVE_ANALYSIS-1:-1]
        else:
            top_moves = sorted_moves[:ME_TO_MOVE_ANALYSIS]
        
        out = ""
        for move in top_moves:
            new_fen = get_fen_after_uci(fen, move["move"]["uci"])
            line = "\t" * tabs + f"{fen_to_move_number(fen)} {move["move"]["san"]} (cp_trap=({move["cp"]}) (cp_eng=({get_engine_eval(new_fen)})\n"
            out += line
            out += recursive_analysis_str(new_fen, me_to_move=not me_to_move, depth=depth-1, tabs=tabs+1)

        with open(MEMO_FN, "w") as f:
            json.dump(memo, f, indent=4)
        return out

    else:
        weighted_evals = []
        cumulative_percentage = 0
        for move in moves:
            print(f"Evaluating move {fen_to_move_number(fen)} {move["san"]}")
            move_percentage = get_move_percentage(games, move)
            new_fen = get_fen_after_uci(fen, move["uci"])
            try:
                weighted_eval_after_move = recursive_weighted_eval(new_fen, 
                                                               me_to_move=not me_to_move, 
                                                               depth=1, 
                                                               memo=memo) * move_percentage
            except Exception as e:
                with open(MEMO_FN, "w") as f:
                    json.dump(memo, f, indent=4)
                raise e
            weighted_evals.append(                
                {
                    "move": move,
                    "cp": weighted_eval_after_move
                })

            cumulative_percentage += move_percentage
            # Only iterate until we reach the percentage cutoff
            if cumulative_percentage > OPP_TO_MOVE_PERCENTAGE_CUTOFF:
                break
            
        out = ""
        for move in weighted_evals:
            new_fen = get_fen_after_uci(fen, move["move"]["uci"])
            move_percentage = int(get_move_percentage(games,move["move"]) * 100)
            line = "\t" * tabs + f"{fen_to_move_number(fen)} {move["move"]["san"]} ({move_percentage}%)\n"
            out += line
            out += recursive_analysis_str(new_fen, me_to_move=not me_to_move, depth=depth-1, tabs=tabs+1)

        with open(MEMO_FN, "w") as f:
            json.dump(memo, f, indent=4)
        return out


        
    
if __name__ == "__main__":
    MAX_ME_MOVES = 6 # max number of moves to analyze
    ME_TO_MOVE_ANALYSIS = 3 # top moves to keep in analysis

    starting_fen = "r1bqk2r/pppp1ppp/2n5/2b1P3/2Bp2n1/2P2N2/PP3PPP/RNBQK2R w KQkq - 1 7"
    session = berserk.TokenSession("lip_PuMYqKFWXOOjl3eSwU4J")
    client = berserk.Client(session=session)

    stockfish = Stockfish(path="/Users/juliushoang/Repos/stockfish/stockfish-macos-x86-64-bmi2")
    I_AM_WHITE = True
    me_to_move = white_to_move(starting_fen) == I_AM_WHITE


    run_analysis(starting_fen, me_to_move=me_to_move, max_depth=4)

    with open(ANALYSIS_FN, "w") as f:
        f.write(recursive_analysis_str(starting_fen, me_to_move=me_to_move, depth=3))
