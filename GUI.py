import tkinter as tk

import AI
import Tetris
import threading
import time

SIDE_LENGTH = 20


def symbol_to_color(symbol):
    if symbol == 0:
        return "grey"
    elif symbol == 1:
        return "red"
    elif symbol == 2:
        return "green"
    elif symbol == 3:
        return "blue"
    elif symbol == 4:
        return "yellow"
    elif symbol == 5:
        return "black"
    elif symbol == 6:
        return "orange"
    elif symbol == 7:
        return "white"


def run():
    # setup tkinter
    window = tk.Tk()
    window.title("Tetris Bot")
    canvas = tk.Canvas(window, width=500, height=500)
    canvas.pack()

    # setup board
    board = []
    for i in range(Tetris.BOARD_HEIGHT):
        row = []
        for j in range(Tetris.BOARD_WIDTH):
            block = canvas.create_rectangle(
                j*SIDE_LENGTH, i*SIDE_LENGTH, (j+1)*SIDE_LENGTH, (i+1)*SIDE_LENGTH, fill="grey")
            row.append(block)
        board.append(row)
    board.reverse()

    # setup engine
    engine = Tetris.Engine()

    #rectangle = canvas.create_rectangle(50, 50, 150, 150, fill="pink")

    def update_board():
        for i in range(Tetris.BOARD_HEIGHT):
            for j in range(Tetris.BOARD_WIDTH):
                fill_color = None
                symbol = engine.board[i][j]
                fill_color = symbol_to_color(symbol)
                canvas.itemconfig(board[i][j], fill=fill_color)
        if engine.inTurn:
            fill_color = symbol_to_color(engine.player_piece[0])
            for cord in engine.player_piece[1]:
                canvas.itemconfig(board[cord[1]][cord[0]], fill=fill_color)

    def move(event):
        if event.keysym == "Left":      # move left
            engine.move_piece(-1)
        elif event.keysym == "Right":   # move right
            engine.move_piece(1)
        elif event.keysym == "z":       # rotate left
            engine.rotate_piece(-1)
        elif event.keysym == "Up":      # rotate right
            engine.rotate_piece(1)
        update_board()

    running = True

    def run_engine():
        while engine.start_move():
            pass
        running = False
    engine_thread = threading.Thread(target=run_engine)
    engine_thread.start()

    def run_ai():
        ai = AI.AI()
        ai.randomize_network()
        while running:
            move_idea = ai.get_move(engine.board, engine.next, engine.player_piece)
            if move_idea == 1:
                engine.move_piece(1)
            elif move_idea == 2:
                engine.move_piece(-1)
            elif move_idea == 3:
                engine.rotate_piece(1)
            elif move_idea == 4:
                engine.rotate_piece(-1)
            time.sleep(Tetris.WAIT_TIME / 2)
    ai_thread = threading.Thread(target=run_ai)
    ai_thread.start()

    def run_board():
        update_board()
        while running:
            time.sleep(Tetris.WAIT_TIME / 5)
            update_board()
    board_thread = threading.Thread(target=run_board)
    board_thread.start()

    window.bind("<KeyPress>", move)
    window.focus_set()
    window.mainloop()


if __name__ == "__main__":
    run()
