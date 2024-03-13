from peaces import Pawn, Rook, Bishop, King, Knight, Queen, ChessPiece, Dragon, Magister, Enchanter


class Move:
    def __init__(self, start_pos, end_pos, piece, captured_piece=None):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.piece = piece
        self.captured_piece = captured_piece


class ChessBoard:
    def __init__(self):
        self.board_size = 8
        self.board = self.create_board()
        self.fill_board()
        self.current_player = 'white'
        self.moves_history = []

    def create_board(self):
        board = []
        for _ in range(self.board_size):
            row = [' '] * self.board_size
            board.append(row)
        return board

    def fill_board(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if (row + col) % 2 == 0:
                    self.board[row][col] = '█'  # Black square
                else:
                    self.board[row][col] = ' '  # White square

        # Place white pieces
        # self.place_piece(Rook('black', (0, 0)))
        # self.place_piece(Knight('black', (1, 0)))
        # self.place_piece(Bishop('black', (2, 0)))
        # self.place_piece(Queen('black', (3, 0)))
        # self.place_piece(King('black', (4, 0)))
        # self.place_piece(Bishop('black', (5, 0)))
        # self.place_piece(Knight('black', (6, 0)))
        # self.place_piece(Rook('black', (7, 0)))
        # for col in range(8):
        #     self.place_piece(Pawn('black', (col, 1)))
        #
        # # Place black pieces
        # self.place_piece(Rook('white', (0, 7)))
        # self.place_piece(Knight('white', (1, 7)))
        # self.place_piece(Bishop('white', (2, 7)))
        # self.place_piece(Queen('white', (3, 7)))
        # self.place_piece(King('white', (4, 7)))
        # self.place_piece(Bishop('white', (5, 7)))
        # self.place_piece(Knight('white', (6, 7)))
        # self.place_piece(Rook('white', (7, 7)))
        # for col in range(8):
        #     self.place_piece(Pawn('white', (col, 6)))

        # test
        self.place_piece(King('black', (7, 2)))
        self.place_piece(King('white', (0, 7)))
        self.place_piece(Queen('black', (4, 3)))

        self.place_piece(Dragon('white', (4, 7)))
        self.place_piece(Enchanter('white', (5, 7)))
        self.place_piece(Magister('white', (6, 7)))

    def print_board(self):
        print("  a b c d e f g h")
        print(" +-----------------+")
        for i in range(8):
            print(f"{8 - i}| {' | '.join(str(piece) for piece in self.board[i])} |")
        print(" +-----------------+")

    def place_piece(self, piece):
        col, row = piece.position
        self.board[row][col] = piece

    def move_piece(self, start_pos, end_pos):
        start_col, start_row = self.algebraic_to_coordinate(start_pos)
        end_col, end_row = self.algebraic_to_coordinate(end_pos)
        piece = self.board[start_row][start_col]
        if end_col in range(0, 8) and end_row in range(0, 8):
            if isinstance(piece, ChessPiece):
                if piece.color != self.current_player:  # Проверяем цвет фигуры
                    print("Вы не можете ходить этой фигурой. Ходите своими фигурами.")
                    return False

                if not piece.check_move((start_col, start_row), (end_col, end_row), self):
                    return False

                self.moves_history.append(Move(start_pos, end_pos, piece))
                # Если ход допустим, перемещаем фигуру
                self.board[end_row][end_col] = piece
                self.board[start_row][start_col] = ' '
                return True
        return False

    def algebraic_to_coordinate(self, position):
        col = ord(position[0]) - ord('a')
        row = 8 - int(position[1])
        return int(col), int(row)

    def coordinate_to_algebraic(self, position):
        col = chr(position[0] + ord('a'))
        row = str(8 - position[1])
        return col + row

    def switch_player(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def is_check(self):
        king_position = None
        king = None
        # Найдем положение короля текущего игрока
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = self.board[row][col]
                if isinstance(piece, King) and piece.color != self.current_player:
                    king_position = (col, row)
                    king = self.board[row][col]
                    break

        # Проверим, атакован ли король текущего игрока
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = self.board[row][col]
                if isinstance(piece, ChessPiece) and piece.color == self.current_player:
                    if piece.check_move((col, row), king_position, self):
                        # print(f"Шах! Король игрока {king.color.capitalize()} находится под угрозой.")
                        return True
        return False

    def get_piece_position(self, piece):
        for row_index, row in enumerate(self.board):
            for col_index, board_piece in enumerate(row):
                if board_piece == piece:
                    return col_index, row_index
        return None

    def is_checkmate(self):
        # Проверяем, находится ли король под шахом
        if not self.is_check():
            return False
        return False

    def undo_move(self, steps=1):
        for _ in range(steps):
            if self.moves_history:
                last_move = self.moves_history.pop()
                start_col, start_row = self.algebraic_to_coordinate(last_move.start_pos)
                end_col, end_row = self.algebraic_to_coordinate(last_move.end_pos)
                # Возвращаем фигуру на предыдущее место
                self.board[start_row][start_col] = last_move.piece
                # Если была захвачена фигура, восстанавливаем ее на место
                if last_move.captured_piece:
                    self.board[end_row][end_col] = last_move.captured_piece
                else:
                    self.board[end_row][end_col] = ' '  # Если фигура не была захвачена, очищаем ее предыдущее место
                # Обновляем текущего игрока
                self.switch_player()


if __name__ == "__main__":
    board = ChessBoard()
    while True:
        board.print_board()
        start, end = input(f"Ход игрока {board.current_player.capitalize()} (например, e2 e4): ").split()
        if start == 'undo':
            board.undo_move(int(end))
        elif board.move_piece(start, end):
            if board.is_checkmate():
                print(f"Игрок {board.current_player.capitalize()} победил!")
                break
            board.switch_player()
        else:
            print("Недопустимый ход! Попробуйте еще раз.")
