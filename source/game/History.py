from source.pieces import Constants as constants


class GameHistory:
    def __init__(self, board):
        self.board = board
        self.move_history = []

    def record_move(self, piece, original_board_position, is_capture, is_check, pieces):
        is_ambiguous = False
        position = self.board.files[piece.board_position[1]] + self.board.ranks[piece.board_position[0]]
        capture = 'x' if is_capture else ''
        check = '+' if is_check else ''
        identifier = ''

        if piece.piece == constants.Type.ROOK or piece.piece == constants.Type.KNIGHT:
            for twin_piece in pieces:
                if twin_piece.owner == piece.owner and twin_piece.piece == piece.piece and twin_piece != piece:
                    new_position = piece.board_position
                    piece.board_position = original_board_position

                    for twin_move in twin_piece.get_possible_moves(pieces, self.board):
                        if twin_move[0] == new_position:
                            is_ambiguous = True
                            break

                    piece.board_position = new_position

                    if is_ambiguous:
                        if twin_piece.board_position[1] == original_board_position[1]:
                            identifier = self.board.ranks[original_board_position[0]]
                        else:
                            identifier = self.board.files[original_board_position[1]]
        elif piece.piece == constants.Type.PAWN and is_capture:
            identifier = self.board.files[original_board_position[1]]

        move = piece.name + identifier.lower() + capture + position.lower() + check

        if piece.owner == 0:
            self.move_history.append((move, ''))
        else:
            self.move_history[-1] = (self.move_history[-1][0], move)

    def add_checkmate_mark(self):
        if self.move_history[-1][1] != '':
            self.move_history[-1] = (self.move_history[-1][0], self.move_history[-1][1].replace('+', '#'))
        else:
            self.move_history[-1] = (self.move_history[-1][0].replace('+', '#'), self.move_history[-1][1])

    def check_for_repetition(self):
        repetition = False

        if len(self.move_history) >= 6:
            white_index = -1
            black_index = -1 if self.move_history[-1][1] != '' else -2
            repetition = True

            for index in range(2, 5, 2):
                if self.move_history[white_index][0] != self.move_history[white_index - index][0] or \
                        self.move_history[white_index - 1][0] != self.move_history[white_index - 1 - index][0] or \
                        self.move_history[black_index][1] != self.move_history[black_index - index][1] or \
                        self.move_history[black_index - 1][1] != self.move_history[black_index - 1 - index][1]:
                    repetition = False
                    break

        return repetition
