class ChessPiece:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.symbol = None

    def check_move(self, position, new_position, board):
        pass

    def __str__(self):
        return self.symbol


class Pawn(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = '♙' if color == 'white' else '♟'

    def check_move(self, position, new_position, board):
        col, row = new_position
        if self.color == 'white':
            direction = -1
            start_row = 6
        else:
            direction = 1
            start_row = 1

        start_col, start_row_board = position

        # Проверяем возможность движения на одну клетку вперед
        if start_col == col and start_row_board + direction == row and not isinstance(board.board[row][col],
                                                                                      ChessPiece):
            return True

        # Проверяем возможность движения на две клетки вперед из начального положения
        if (start_col == col and start_row == start_row_board and start_row + 2 * direction == row and
                not isinstance(board.board[row][col], ChessPiece)):
            return True

        # Проверяем возможность съесть фигуру
        if abs(start_col - col) == 1 and start_row_board + direction == row:
            target_piece = board.board[row][col]
            if isinstance(target_piece, ChessPiece) and target_piece.color != self.color:
                return True

        return False


class Rook(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = '♖' if color == 'white' else '♜'

    def check_move(self, position, new_position, board):
        start_col, start_row = position
        target_col, target_row = new_position

        # Проверяем, двигается ли ладья по вертикали или горизонтали
        if start_col != target_col and start_row != target_row:
            return False

        # Проверяем, нет ли фигур на пути ладьи между начальной и конечной позициями
        if start_col == target_col:  # движение по вертикали
            step = 1 if target_row > start_row else -1
            for i in range(start_row + step, target_row, step):
                if isinstance(board.board[i][start_col], ChessPiece):
                    return False
        else:  # движение по горизонтали
            step = 1 if target_col > start_col else -1
            for i in range(start_col + step, target_col, step):
                if isinstance(board.board[start_row][i], ChessPiece):
                    return False

        # Проверяем, может ли ладья захватить фигуру противника в целевой позиции
        target_piece = board.board[target_row][target_col]
        if isinstance(target_piece, ChessPiece) and target_piece.color == self.color:
            return False

        return True


class Knight(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = '♘' if color == 'white' else '♞'

    def check_move(self, position, new_position, board):
        start_col, start_row = position
        target_col, target_row = new_position

        # Проверяем, является ли ход конем (перемещение на 2 клетки по одной оси и на 1 клетку по другой оси)
        if abs(start_col - target_col) == 2 and abs(start_row - target_row) == 1:
            return True
        elif abs(start_col - target_col) == 1 and abs(start_row - target_row) == 2:
            return True
        else:
            return False


class Bishop(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = '♗' if color == 'white' else '♝'

    def check_move(self, position, new_position, board):
        start_col, start_row = position
        target_col, target_row = new_position

        # Проверяем, является ли ход по диагонали
        if abs(start_col - target_col) == abs(start_row - target_row):
            # Проверяем, нет ли фигур на пути слона между начальной и конечной позициями
            col_step = 1 if target_col > start_col else -1
            row_step = 1 if target_row > start_row else -1
            col, row = start_col + col_step, start_row + row_step
            while col != target_col and row != target_row:
                if isinstance(board.board[row][col], ChessPiece):
                    return False
                col += col_step
                row += row_step

            # Проверяем, может ли слон захватить фигуру противника в целевой позиции
            target_piece = board.board[target_row][target_col]
            if isinstance(target_piece, ChessPiece) and target_piece.color == self.color:
                return False

            return True

        return False


class Queen(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = '♕' if color == 'white' else '♛'

    def check_move(self, position, new_position, board):
        start_col, start_row = position
        target_col, target_row = new_position

        # Проверяем, является ли ход горизонтальным, вертикальным или по диагонали
        if start_col == target_col or start_row == target_row or abs(start_col - target_col) == abs(
                start_row - target_row):
            # Проверяем, нет ли фигур на пути ферзя между начальной и конечной позициями
            if start_col == target_col:  # движение по вертикали
                step = 1 if target_row > start_row else -1
                for i in range(start_row + step, target_row, step):
                    if isinstance(board.board[i][start_col], ChessPiece):
                        return False
            elif start_row == target_row:  # движение по горизонтали
                step = 1 if target_col > start_col else -1
                for i in range(start_col + step, target_col, step):
                    if isinstance(board.board[start_row][i], ChessPiece):
                        return False
            else:  # движение по диагонали
                col_step = 1 if target_col > start_col else -1
                row_step = 1 if target_row > start_row else -1
                col, row = start_col + col_step, start_row + row_step
                while col != target_col and row != target_row:
                    if isinstance(board.board[row][col], ChessPiece):
                        return False
                    col += col_step
                    row += row_step

            # Проверяем, может ли ферзь захватить фигуру противника в целевой позиции
            target_piece = board.board[target_row][target_col]
            if isinstance(target_piece, ChessPiece) and target_piece.color == self.color:
                return False

            return True

        return False


class King(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = '♔' if color == 'white' else '♚'

    def check_move(self, position, new_position, board):
        start_col, start_row = position
        target_col, target_row = new_position

        # Проверяем, является ли ход королем (смещение на одну клетку по вертикали, горизонтали или диагонали)
        if abs(start_col - target_col) <= 1 and abs(start_row - target_row) <= 1:
            # Проверяем, может ли король совершить ход на целевую позицию
            target_piece = board.board[target_row][target_col]
            if not isinstance(target_piece, ChessPiece) or target_piece.color != self.color:
                return True

        return False


class Enchanter(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = '⚔' if color == 'white' else '⚒'

    def check_move(self, position, new_position, board):
        start_col, start_row = position
        target_col, target_row = new_position

        # Проверяем, может ли чародей совершить ход на целевую позицию
        target_piece = board.board[target_row][target_col]
        if not isinstance(target_piece, ChessPiece) or target_piece.color != self.color:
            return True

        return False


class Dragon(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = '🐉' if color == 'white' else '🐲'

    def check_move(self, position, new_position, board):
        start_col, start_row = position
        target_col, target_row = new_position

        # Проверяем, является ли ход драконом
        if (abs(start_col - target_col) == 3 and abs(start_row - target_row) == 2) or \
                (abs(start_col - target_col) == 2 and abs(start_row - target_row) == 3):
            # Проверяем, может ли дракон совершить ход на целевую позицию
            target_piece = board.board[target_row][target_col]
            if not isinstance(target_piece, ChessPiece) or target_piece.color != self.color:
                return True

        return False


class Magister(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = '🔮' if color == 'white' else '📜'

    def check_move(self, position, new_position, board):
        start_col, start_row = position
        target_col, target_row = new_position

        # Проверяем, является ли ход магистром
        if abs(start_col - target_col) <= 4 and abs(start_row - target_row) <= 4:
            # Проверяем, может ли магистр совершить ход на целевую позицию
            target_piece = board.board[target_row][target_col]
            if not isinstance(target_piece, ChessPiece) or target_piece.color != self.color:
                return True

        return False


class CheckersPiece(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = '⛀' if color == 'white' else '⛂'

    def check_move(self, position, new_position, board):
        start_col, start_row = position
        target_col, target_row = new_position

        # Проверяем, является ли ход диагональным и на одну клетку
        if abs(start_col - target_col) == 1 and abs(start_row - target_row) == 1:
            return True
        else:
            return False

