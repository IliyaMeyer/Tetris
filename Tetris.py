import threading
import random

BOARD_HEIGHT = 20
BOARD_WIDTH = 10


class Engine:

    def print_board(self):
        for row in reversed(self.board):
            for block in row:
                if block == 0:
                    print(" ", end="")
                else:
                    print(block, end="")
            print("")

    #   check if a given piece overlaps existing board elements
    #   TODO shouldn't return false if above max height
    def check_free(self, piece):
        for cord in piece:
            if cord[0] < 0 or cord[0] >= BOARD_WIDTH or cord[1] < 0 or cord[1] >= BOARD_HEIGHT \
                    or self.board[cord[1]][cord[0]] != 0:
                return False
        return True

    #   rotate player_piece; direction: -1 -> left; 1 -> right
    def rotate_piece(self, direction):
        if not self.can_input:
            return
        self.can_input = False
        self.lock.acquire()

        piece_number = self.player_piece[0]
        new_piece = [None, None, None, None]
        orientation = self.player_piece[2]  # orientation for 2-state-> 0 horizontal, 1 vertical

        if piece_number == 1:  # I
            new_piece[2] = self.player_piece[1][2]
            center = new_piece[2]
            if orientation == 0:
                new_piece[0] = [center[0], center[1] + 2]
                new_piece[1] = [center[0], center[1] + 1]
                new_piece[3] = [center[0], center[1] - 1]
                if not self.check_free(new_piece):
                    self.lock.release()
                    self.can_input = True
                    return
                self.player_piece[1] = new_piece
                self.player_piece[2] = 1
            else:
                new_piece[0] = [center[0] - 2, center[1]]
                new_piece[1] = [center[0] - 1, center[1]]
                new_piece[3] = [center[0] + 1, center[1]]
                if not self.check_free(new_piece):
                    self.lock.release()
                    self.can_input = True
                    return
                self.player_piece[1] = new_piece
                self.player_piece[2] = 0
        elif piece_number == 6:  # Z
            new_piece[1] = self.player_piece[1][1]
            new_piece[2] = self.player_piece[1][2]
            center = new_piece[1]
            if orientation == 0:
                new_piece[0] = [center[0] + 1, center[1] + 1]
                new_piece[3] = [center[0] + 1, center[1]]
                if not self.check_free(new_piece):
                    self.lock.release()
                    self.can_input = True
                    return
                self.player_piece[1] = new_piece
                self.player_piece[2] = 1
            else:
                new_piece[0] = [center[0] - 1, center[1]]
                new_piece[3] = [center[0] + 1, center[1] - 1]
                if not self.check_free(new_piece):
                    self.lock.release()
                    self.can_input = True
                    return
                self.player_piece[1] = new_piece
                self.player_piece[2] = 0
        elif piece_number == 7:  # S
            new_piece[2] = self.player_piece[1][2]
            center = new_piece[2]
            if orientation == 0:
                new_piece[0] = [center[0] + 1, center[1] - 1]
                new_piece[1] = [center[0] + 1, center[1]]
                new_piece[3] = [center[0], center[1] + 1]
                if not self.check_free(new_piece):
                    self.lock.release()
                    self.can_input = True
                    return
                self.player_piece[1] = new_piece
                self.player_piece[2] = 1
            else:
                new_piece[0] = [center[0] - 1, center[1] - 1]
                new_piece[1] = [center[0], center[1] - 1]
                new_piece[3] = [center[0] + 1, center[1]]
                if not self.check_free(new_piece):
                    self.lock.release()
                    self.can_input = True
                    return
                self.player_piece[1] = new_piece
                self.player_piece[2] = 0
        elif piece_number != 2:
            new_piece[0] = self.player_piece[1][0]
            new_orientation = orientation + direction
            if new_orientation == -1:
                new_orientation = 3
            elif new_orientation == 4:
                new_orientation = 0
            center = self.player_piece[1][0]
            if piece_number == 3:  # L
                if new_orientation == 0:
                    new_piece[1] = [center[0] - 1, center[1]]
                    new_piece[2] = [center[0] + 1, center[1]]
                    new_piece[3] = [center[0] - 1, center[1] - 1]
                if new_orientation == 1:
                    new_piece[1] = [center[0], center[1] + 1]
                    new_piece[2] = [center[0], center[1] - 1]
                    new_piece[3] = [center[0] - 1, center[1] + 1]
                if new_orientation == 2:
                    new_piece[1] = [center[0] + 1, center[1]]
                    new_piece[2] = [center[0] - 1, center[1]]
                    new_piece[3] = [center[0] + 1, center[1] + 1]
                if new_orientation == 3:
                    new_piece[1] = [center[0], center[1] - 1]
                    new_piece[2] = [center[0], center[1] + 1]
                    new_piece[3] = [center[0] + 1, center[1] - 1]
            elif piece_number == 4:  # J
                if new_orientation == 0:
                    new_piece[1] = [center[0] - 1, center[1]]
                    new_piece[2] = [center[0] + 1, center[1]]
                    new_piece[3] = [center[0] + 1, center[1] - 1]
                if new_orientation == 1:
                    new_piece[1] = [center[0], center[1] + 1]
                    new_piece[2] = [center[0], center[1] - 1]
                    new_piece[3] = [center[0] - 1, center[1] - 1]
                if new_orientation == 2:
                    new_piece[1] = [center[0] + 1, center[1]]
                    new_piece[2] = [center[0] - 1, center[1]]
                    new_piece[3] = [center[0] - 1, center[1] + 1]
                if new_orientation == 3:
                    new_piece[1] = [center[0], center[1] - 1]
                    new_piece[2] = [center[0], center[1] + 1]
                    new_piece[3] = [center[0] + 1, center[1] + 1]
            elif piece_number == 5:  # T
                if new_orientation == 0:
                    new_piece[1] = [center[0] - 1, center[1]]
                    new_piece[2] = [center[0] + 1, center[1]]
                    new_piece[3] = [center[0], center[1] - 1]
                if new_orientation == 1:
                    new_piece[1] = [center[0], center[1] + 1]
                    new_piece[2] = [center[0], center[1] - 1]
                    new_piece[3] = [center[0] - 1, center[1]]
                if new_orientation == 2:
                    new_piece[1] = [center[0] + 1, center[1]]
                    new_piece[2] = [center[0] - 1, center[1]]
                    new_piece[3] = [center[0], center[1] + 1]
                if new_orientation == 3:
                    new_piece[1] = [center[0], center[1] - 1]
                    new_piece[2] = [center[0], center[1] + 1]
                    new_piece[3] = [center[0] + 1, center[1]]
            if not self.check_free(new_piece):
                self.lock.release()
                self.can_input = True
                return
            self.player_piece[1] = new_piece
            self.player_piece[2] = new_orientation

        self.lock.release()
        self.can_input = True

    #   move player_piece; direction: -1 -> left; 1 -> right
    def move_piece(self, direction):
        if not self.can_input:
            return
        self.can_input = False
        self.lock.acquire()

        new_piece = []
        for i in range(4):
            piece = self.player_piece[1]
            new_piece.append([piece[i][0] + direction, piece[i][1]])
        if not self.check_free(new_piece):
            self.lock.release()
            self.can_input = True
            return
        self.player_piece[1] = new_piece

        self.lock.release()
        self.can_input = True

    #   drop player_piece one block down: return False if it can't go down
    def fall(self):
        self.lock.acquire()

        new_piece = []
        for i in range(4):
            new_piece.append([self.player_piece[1][i][0], self.player_piece[1][i][1] - 1])

        if not self.check_free(new_piece):
            self.lock.release()
            return False

        self.player_piece[1] = new_piece
        self.lock.release()
        return True

    #   set "next piece" to a random piece
    def generate_next(self):
        self.next = random.randint(1, 7)

    def __init__(self):
        self.board = []     # 1->I; 2->O; 3->L; 4->J; 5->T; 6->Z; 7->S; bottom left-> (0,0)
        for i in range(BOARD_HEIGHT):
            self.board.append([0] * BOARD_WIDTH)
        self.player_piece = None  # [piece_number, [cord1, cord2, cord3, cord4], orientation] cord1-> center
        self.next = None
        self.generate_next()
        self.lines = 0
        self.score = 0
        self.speed_number = 0
        self.can_input = False  # whether or not a move/rotation can be queued
        self.lock = threading.Lock()

    #   the player has lost
    def game_over(self):
        pass

    #   place a new piece on the board: return False if game over
    def start_move(self):
        #   generate new piece
        self.player_piece = [self.next, None, 0]
        if self.next == 1:      # I
            self.player_piece[1] = [[3, BOARD_HEIGHT-1], [4, BOARD_HEIGHT-1], [5, BOARD_HEIGHT-1], [6, BOARD_HEIGHT-1]]
        elif self.next == 2:    # O
            self.player_piece[1] = [[4, BOARD_HEIGHT-1], [5, BOARD_HEIGHT-1], [4, BOARD_HEIGHT-2], [5, BOARD_HEIGHT-2]]
        elif self.next == 3:    # L
            self.player_piece[1] = [[4, BOARD_HEIGHT-1], [3, BOARD_HEIGHT-1], [5, BOARD_HEIGHT-1], [3, BOARD_HEIGHT-2]]
        elif self.next == 4:    # J
            self.player_piece[1] = [[4, BOARD_HEIGHT-1], [3, BOARD_HEIGHT-1], [5, BOARD_HEIGHT-1], [5, BOARD_HEIGHT-2]]
        elif self.next == 5:    # T
            self.player_piece[1] = [[4, BOARD_HEIGHT-1], [3, BOARD_HEIGHT-1], [5, BOARD_HEIGHT-1], [4, BOARD_HEIGHT-2]]
        elif self.next == 6:    # Z
            self.player_piece[1] = [[4, BOARD_HEIGHT-1], [5, BOARD_HEIGHT-1], [5, BOARD_HEIGHT-2], [6, BOARD_HEIGHT-2]]
        elif self.next == 7:    # S
            self.player_piece[1] = [[4, BOARD_HEIGHT-2], [5, BOARD_HEIGHT-2], [5, BOARD_HEIGHT-1], [6, BOARD_HEIGHT-1]]
        self.generate_next()

        #   check for lose condition
        if not self.check_free(self.player_piece[1]):
            self.game_over()
            return False

        #   let the piece fall
        while self.fall():
            pass

        #   imprint the piece onto the board
        for cord in self.player_piece[1]:
            self.board[cord[1]][cord[0]] = self.player_piece[0]

        # remove complete lines
        checked_lines = []
        complete_lines = []
        for cord in self.player_piece[1]:
            if cord[1] in checked_lines:
                continue
            checked_lines.append(cord[1])
            add = True
            for pos in self.board[cord[1]]:
                if pos == 0:
                    add = False
                    break
            if add:
                complete_lines.append(cord[1])


def main():
    engine = Engine()
    engine.start_move()
    engine.start_move()
    engine.start_move()
    engine.start_move()
    engine.print_board()


if __name__ == "__main__":
    main()
