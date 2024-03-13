from peaces import CheckersPiece, Queen, ChessPiece
from main import ChessBoard


class CheckersBoard(ChessBoard):
    def fill_board(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if (row + col) % 2 == 0:
                    self.board[row][col] = ' '  # White square
                else:
                    if row < 3:
                        self.place_piece(CheckersPiece('black', (col, row)))
                    elif row > 4:
                        self.place_piece(CheckersPiece('white', (col, row)))

    def is_checkmate(self):
        return self.is_stalemate()

    def is_stalemate(self):
        # Проверяем, есть ли у текущего игрока ходы
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = self.board[row][col]
                if isinstance(piece, CheckersPiece) and piece.color == self.current_player:
                    # Проверяем, есть ли у фигуры какие-либо возможные ходы
                    for move in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
                        new_col = col + move[0]
                        new_row = row + move[1]
                        if self.is_valid_position(new_col, new_row) and self.board[new_row][new_col] == ' ':
                            return False
        return True

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

                # Если ход допустим, перемещаем фигуру
                self.board[end_row][end_col] = piece
                self.board[start_row][start_col] = ' '
                # Если фигура дошла до конца доски противоположного цвета, превращаем её в дамку
                if (piece.color == 'white' and end_row == 0) or (piece.color == 'black' and end_row == 7):
                    self.board[end_row][end_col] = Queen(piece.color, (end_col, end_row))
                return True
        return False

    def is_valid_position(self, col, row):
        return 0 <= col < self.board_size and 0 <= row < self.board_size

    def is_capture_available(self):
        # Проверяем, есть ли возможные ходы, которые являются взятиями
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = self.board[row][col]
                if isinstance(piece, CheckersPiece) and piece.color == self.current_player:
                    for move in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
                        new_col = col + move[0]
                        new_row = row + move[1]
                        middle_col = (col + new_col) // 2
                        middle_row = (row + new_row) // 2
                        if self.is_valid_position(new_col, new_row) and self.board[new_row][new_col] == ' ' \
                                and isinstance(self.board[middle_row][middle_col], CheckersPiece) \
                                and self.board[middle_row][middle_col].color != self.current_player:
                            return True
        return False


if __name__ == "__main__":
    board = CheckersBoard()
    while True:
        board.print_board()
        start, end = input(f"Ход игрока {board.current_player.capitalize()} (например, e2 e4): ").split()
        if board.move_piece(start, end):
            if board.is_checkmate():
                print(f"Игрок {board.current_player.capitalize()} победил!")
                break
            board.switch_player()
        else:
            print("Недопустимый ход! Попробуйте еще раз.")
