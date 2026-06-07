# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "chess>=1.11",
#   "mcp>=1.0",
# ]
# ///

import io
import json
import os
import re
from typing import Optional

import chess
import chess.pgn
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("chess-tools")

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
}
PIECE_NAMES = {
    chess.PAWN: "Pawn",
    chess.KNIGHT: "Knight",
    chess.BISHOP: "Bishop",
    chess.ROOK: "Rook",
    chess.QUEEN: "Queen",
    chess.KING: "King",
}

CLK_RE = re.compile(r"\[%clk\s+(\d+):(\d+):(\d+(?:\.\d+)?)\]")


def _material(board: chess.Board, color: chess.Color) -> int:
    return sum(PIECE_VALUES[pt] * len(board.pieces(pt, color)) for pt in PIECE_VALUES)


def _parse_clk(comment: str) -> Optional[float]:
    m = CLK_RE.search(comment or "")
    if not m:
        return None
    h, mn, s = m.groups()
    return int(h) * 3600 + int(mn) * 60 + float(s)


def _parse_tc_seconds(tc: Optional[str]) -> Optional[int]:
    if not tc:
        return None
    base = tc.split("+")[0]
    return int(base) if base.isdigit() else None


def _walk_moves(game: chess.pgn.Game):
    """Walk mainline moves safely, stopping at the first illegal move.
    Returns (moves_list, san_list)."""
    board = game.board()
    moves, sans = [], []
    for mv in game.mainline_moves():
        try:
            sans.append(board.san(mv))
            board.push(mv)
            moves.append(mv)
        except Exception:
            break
    return moves, sans


@mcp.tool()
def parse_game(pgn: str) -> dict:
    """Parse a PGN string and return game metadata from the headers."""
    game = chess.pgn.read_game(io.StringIO(pgn))
    if game is None:
        return {"error": "Could not parse PGN"}
    h = game.headers
    moves, _ = _walk_moves(game)
    tc = h.get("TimeControl")
    variant = h.get("Variant")
    return {
        "white_player": h.get("White"),
        "black_player": h.get("Black"),
        "white_elo": h.get("WhiteElo"),
        "black_elo": h.get("BlackElo"),
        "result": h.get("Result"),
        "total_half_moves": len(moves),
        "total_full_moves": (len(moves) + 1) // 2,
        "time_control": tc,
        "time_control_seconds": _parse_tc_seconds(tc),
        "opening": h.get("Opening") or h.get("ECO"),
        "site": h.get("Site"),
        "date": h.get("Date"),
        "termination": h.get("Termination"),
        "variant_warning": variant if variant not in (None, "Standard") else None,
    }


@mcp.tool()
def get_position(pgn: str, half_move: int) -> dict:
    """Return the board state after a specific half-move (1-indexed).

    half_move arithmetic:
      White's move N  -> half_move = (N - 1) * 2 + 1
      Black's move N  -> half_move = (N - 1) * 2 + 2
    Example: White move 15 = half_move 29, Black move 15 = half_move 30.
    """
    game = chess.pgn.read_game(io.StringIO(pgn))
    if game is None:
        return {"error": "Could not parse PGN"}
    moves, sans = _walk_moves(game)
    if half_move < 1 or half_move > len(moves):
        return {"error": f"half_move {half_move} out of range 1–{len(moves)}"}
    board = game.board()
    for mv in moves[:half_move]:
        board.push(mv)
    pieces = {chess.WHITE: [], chess.BLACK: []}
    for sq, piece in sorted(board.piece_map().items()):
        pieces[piece.color].append(
            f"{PIECE_NAMES[piece.piece_type]} on {chess.square_name(sq)}"
        )
    return {
        "half_move": half_move,
        "full_move_number": (half_move + 1) // 2,
        "color_just_moved": "white" if half_move % 2 == 1 else "black",
        "move_played": sans[half_move - 1],
        "fen": board.fen(),
        "side_to_move": "white" if board.turn == chess.WHITE else "black",
        "white_material": _material(board, chess.WHITE),
        "black_material": _material(board, chess.BLACK),
        "material_balance": _material(board, chess.WHITE) - _material(board, chess.BLACK),
        "white_pieces": pieces[chess.WHITE],
        "black_pieces": pieces[chess.BLACK],
    }


@mcp.tool()
def get_move_history(pgn: str, start: int = 1, end: Optional[int] = None) -> list:
    """Return a range of moves as full-move rows. start/end are full move numbers."""
    game = chess.pgn.read_game(io.StringIO(pgn))
    if game is None:
        return [{"error": "Could not parse PGN"}]
    _, sans = _walk_moves(game)
    total = (len(sans) + 1) // 2
    if end is None or end > total:
        end = total
    result = []
    for n in range(start, end + 1):
        wi, bi = (n - 1) * 2, (n - 1) * 2 + 1
        result.append({
            "move_number": n,
            "white_move": sans[wi] if wi < len(sans) else None,
            "black_move": sans[bi] if bi < len(sans) else None,
        })
    return result


@mcp.tool()
def get_material_curve(pgn: str) -> list:
    """Return material balance at every half-move for turning point detection.

    Positive balance = White ahead. Includes the SAN of the move played so
    the agent can read the move name without a separate get_position call.
    """
    game = chess.pgn.read_game(io.StringIO(pgn))
    if game is None:
        return [{"error": "Could not parse PGN"}]
    board = game.board()
    curve = []
    for i, mv in enumerate(game.mainline_moves()):
        try:
            san = board.san(mv)
            board.push(mv)
        except Exception:
            break
        curve.append({
            "half_move": i + 1,
            "full_move_number": (i // 2) + 1,
            "color": "white" if i % 2 == 0 else "black",
            "san": san,
            "balance": _material(board, chess.WHITE) - _material(board, chess.BLACK),
        })
    return curve


@mcp.tool()
def get_clock_data(pgn: str) -> list:
    """Parse [%clk] annotations from PGN comments and compute time spent per move.

    Returns per-half-move clock info. clock_remaining_seconds is the time left
    after the move; time_spent_seconds is computed by diffing consecutive values
    for the same color. Returns empty list if no clock annotations found.
    """
    game = chess.pgn.read_game(io.StringIO(pgn))
    if game is None:
        return [{"error": "Could not parse PGN"}]
    tc_seconds = _parse_tc_seconds(game.headers.get("TimeControl"))
    node = game
    entries = []
    half_move = 0
    last_clk = {chess.WHITE: tc_seconds, chess.BLACK: tc_seconds}
    while node.variations:
        node = node.variations[0]
        half_move += 1
        color = chess.WHITE if half_move % 2 == 1 else chess.BLACK
        clk = _parse_clk(node.comment)
        time_spent = None
        if clk is not None and last_clk[color] is not None:
            time_spent = round(last_clk[color] - clk, 1)
        if clk is not None:
            last_clk[color] = clk
        entries.append({
            "half_move": half_move,
            "full_move_number": (half_move + 1) // 2,
            "color": "white" if color == chess.WHITE else "black",
            "clock_remaining_seconds": clk,
            "time_spent_seconds": time_spent,
        })
    return entries


@mcp.tool()
def get_time_analysis(pgn: str) -> dict:
    """Pre-compute all time-usage statistics from [%clk] annotations.

    Returns a ready-to-read summary — no arithmetic needed from the caller.
    Includes per-player stats, long thinks, time pressure moments, and a
    ranked list of notable time moments with plain-language notes.

    Thresholds:
      long think  : time_spent > max(45s, time_control * 0.025)
      time pressure: clock_remaining < max(60s, time_control * 0.07)
    """
    game = chess.pgn.read_game(io.StringIO(pgn))
    if game is None:
        return {"error": "Could not parse PGN"}
    tc_seconds = _parse_tc_seconds(game.headers.get("TimeControl"))
    long_think_threshold = max(45.0, (tc_seconds or 600) * 0.025)
    pressure_threshold = max(60.0, (tc_seconds or 600) * 0.07)

    # Collect raw clock entries with SANs
    board = game.board()
    node = game
    half_move = 0
    last_clk = {chess.WHITE: tc_seconds, chess.BLACK: tc_seconds}
    raw = []
    while node.variations:
        node = node.variations[0]
        half_move += 1
        color = chess.WHITE if half_move % 2 == 1 else chess.BLACK
        clk = _parse_clk(node.comment)
        time_spent = None
        if clk is not None and last_clk[color] is not None:
            time_spent = round(last_clk[color] - clk, 1)
        if clk is not None:
            last_clk[color] = clk
        # Get SAN for this half-move
        san = None
        try:
            mv = node.move
            san = board.san(mv)
            board.push(mv)
        except Exception:
            pass
        raw.append({
            "half_move": half_move,
            "full_move_number": (half_move + 1) // 2,
            "color": chess.WHITE if half_move % 2 == 1 else chess.BLACK,
            "color_str": "white" if half_move % 2 == 1 else "black",
            "san": san,
            "clock_remaining": clk,
            "time_spent": time_spent,
        })

    if not raw or all(e["clock_remaining"] is None for e in raw):
        return {"error": "No clock annotations found in PGN"}

    # Per-player aggregation
    stats = {}
    for color_str in ("white", "black"):
        moves = [e for e in raw if e["color_str"] == color_str and e["time_spent"] is not None]
        if not moves:
            stats[color_str] = None
            continue
        times = [e["time_spent"] for e in moves]
        max_entry = max(moves, key=lambda e: e["time_spent"])
        stats[color_str] = {
            "total_time_used_seconds": round(sum(times), 1),
            "avg_time_per_move_seconds": round(sum(times) / len(times), 1),
            "move_count": len(moves),
            "longest_think": {
                "full_move_number": max_entry["full_move_number"],
                "san": max_entry["san"],
                "seconds": max_entry["time_spent"],
            },
            "long_thinks": [
                {"full_move_number": e["full_move_number"], "san": e["san"], "seconds": e["time_spent"]}
                for e in moves if e["time_spent"] >= long_think_threshold
            ],
            "time_pressure_moments": [
                {"full_move_number": e["full_move_number"], "san": e["san"],
                 "clock_remaining_seconds": e["clock_remaining"], "time_spent_seconds": e["time_spent"]}
                for e in moves if e["clock_remaining"] is not None and e["clock_remaining"] < pressure_threshold
            ],
        }

    # Notable moments: long thinks + time pressure, with plain-language notes, sorted by move
    notable = []
    for e in raw:
        if e["time_spent"] is None and e["clock_remaining"] is None:
            continue
        notes = []
        if e["time_spent"] is not None and e["time_spent"] >= long_think_threshold:
            notes.append(f"spent {e['time_spent']}s (long think)")
        if e["clock_remaining"] is not None and e["clock_remaining"] < pressure_threshold:
            notes.append(f"only {round(e['clock_remaining'])}s remaining (time pressure)")
        if notes:
            notable.append({
                "full_move_number": e["full_move_number"],
                "color": e["color_str"],
                "san": e["san"],
                "time_spent_seconds": e["time_spent"],
                "clock_remaining_seconds": e["clock_remaining"],
                "note": "; ".join(notes),
            })

    return {
        "time_control_seconds": tc_seconds,
        "long_think_threshold_seconds": round(long_think_threshold, 1),
        "time_pressure_threshold_seconds": round(pressure_threshold, 1),
        "white": stats.get("white"),
        "black": stats.get("black"),
        "notable_moments": notable,
    }


@mcp.tool()
def get_game_phases(pgn: str) -> dict:
    """Detect opening/middlegame/endgame boundaries heuristically.

    Opening end: both sides have no minor pieces (N/B) on their home rank,
    enforced minimum move 5.
    Endgame start: queens gone OR total material below 20 points.
    """
    game = chess.pgn.read_game(io.StringIO(pgn))
    if game is None:
        return {"error": "Could not parse PGN"}
    board = game.board()
    opening_end = None
    endgame_start = None
    total_half = 0
    for i, mv in enumerate(game.mainline_moves()):
        try:
            board.push(mv)
        except Exception:
            break
        total_half += 1
        full_move = (i // 2) + 1
        if opening_end is None and full_move >= 5:
            w_home = sum(
                1 for sq in chess.SquareSet(chess.BB_RANK_1)
                if board.piece_at(sq)
                and board.piece_at(sq).color == chess.WHITE
                and board.piece_at(sq).piece_type in (chess.KNIGHT, chess.BISHOP)
            )
            b_home = sum(
                1 for sq in chess.SquareSet(chess.BB_RANK_8)
                if board.piece_at(sq)
                and board.piece_at(sq).color == chess.BLACK
                and board.piece_at(sq).piece_type in (chess.KNIGHT, chess.BISHOP)
            )
            if w_home == 0 and b_home == 0:
                opening_end = full_move
        if endgame_start is None:
            queens = len(board.pieces(chess.QUEEN, chess.WHITE)) + len(
                board.pieces(chess.QUEEN, chess.BLACK)
            )
            total_mat = sum(_material(board, c) for c in [chess.WHITE, chess.BLACK])
            if queens == 0 or total_mat < 20:
                endgame_start = full_move
    total_full = (total_half + 1) // 2
    return {
        "opening_end_move": opening_end,
        "middlegame_start_move": (opening_end + 1) if opening_end else None,
        "endgame_start_move": endgame_start,
        "total_full_moves": total_full,
    }


@mcp.tool()
def get_player_history() -> dict:
    """Read persisted game patterns from .chess/history.json.

    Returns {"games": [...]} or {"games": []} if no history exists yet.
    """
    path = os.path.join(os.getcwd(), ".chess", "history.json")
    if not os.path.exists(path):
        return {"games": []}
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e), "games": []}


@mcp.tool()
def save_game_summary(
    patterns: list,
    result: str,
    date: str,
    user_color: str,
    user_elo: str,
) -> dict:
    """Append a game summary to .chess/history.json for multi-game tracking.

    patterns: list of strings describing recurring themes, e.g.
              ["blunder under time pressure", "missed back-rank weakness"]
    """
    path = os.path.join(os.getcwd(), ".chess", "history.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    history = {"games": []}
    if os.path.exists(path):
        try:
            with open(path) as f:
                history = json.load(f)
        except Exception:
            pass
    history["games"].append({
        "date": date,
        "result": result,
        "user_color": user_color,
        "user_elo": user_elo,
        "patterns": patterns,
    })
    with open(path, "w") as f:
        json.dump(history, f, indent=2)
    return {"saved": True, "total_games": len(history["games"])}


if __name__ == "__main__":
    mcp.run()
