import chess


def evaluate_board(board, last_move=None):
    score = 0.0

    # bauer pushen
    if last_move:
        moved_piece = board.piece_at(last_move.to_square)
        if moved_piece and moved_piece.piece_type == chess.PAWN:
            from_rank = chess.square_rank(last_move.from_square)
            to_rank = chess.square_rank(last_move.to_square)
            is_double_move = (
                (moved_piece.color == chess.WHITE and from_rank == 1 and to_rank == 3) or
                (moved_piece.color == chess.BLACK and from_rank == 6 and to_rank == 4)
            )
            if is_double_move:
                score += 0.4
            else:
                score += 0.3


        if board.is_check():
            score += 0.15

    # springer am rand -5
    for square in board.pieces(chess.KNIGHT, board.turn):
        rank = chess.square_rank(square)
        file = chess.square_file(square)
        if rank in (0, 7) or file in (0, 7):
            score -= 2

    def has_rook_and_queen(color):
        has_rook = False
        has_queen = False
        for square in board.pieces(chess.PIECE_TYPES, color):
            piece = board.piece_at(square)
            if piece.piece_type == chess.ROOK:
                has_rook = True
            elif piece.piece_type == chess.QUEEN:
                has_queen = True
        return has_rook and has_queen

    # pawn vorm king
    for king_color in [chess.WHITE, chess.BLACK]:
        king_square = board.king(king_color)
        king_rank = chess.square_rank(king_square)
        king_file = chess.square_file(king_square)

        if king_color == chess.WHITE:
            front_rank = king_rank + 1
        else:
            front_rank = king_rank - 1

        required_pawn_positions = [
            chess.square(front_rank, king_file),
            chess.square(front_rank, king_file - 1),
            chess.square(front_rank, king_file + 1)
        ]

        all_pawns_present = True
        for position in required_pawn_positions:
            piece = board.piece_at(position)

            pawn_file = chess.square_file(position)
            if pawn_file in [chess.FILE_E, chess.FILE_D]:
                continue

            if not piece or piece.piece_type != chess.PAWN or piece.color != king_color:
                all_pawns_present = False
                break

        if all_pawns_present:
            if has_rook_and_queen(king_color):
                score += 0.6
            else:
                score -= 0.3


    return score


def minimax(board, depth, is_maximizing, last_move=None):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board, last_move)

    best_eval = -float('inf') if is_maximizing else float('inf')
    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, not is_maximizing, move)
        board.pop()

        if is_maximizing:
            best_eval = max(best_eval, eval)
        else:
            best_eval = min(best_eval, eval)

    return best_eval

def get_move(board: chess.Board, depth: int = 2, candidate_moves: list = None) -> chess.Move:
    best_score = -float("inf")
    best_move = None

    moves = candidate_moves if candidate_moves is not None else list(board.legal_moves)

    for move in moves:
        board.push(move)
        score = minimax(board, depth - 1, False, move)
        board.pop()

        if score > best_score or best_move is None:
            best_score = score
            best_move = move

    return best_move
