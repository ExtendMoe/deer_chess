import tkinter
from typing import Tuple
from constants import DEER, DOG, INVALID, PLAY_DEER, PLAY_DOG, PVP, WATCH_AI
import godeer
import rules

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 600
MIN_PADDING = 20
SPACING = min((CANVAS_WIDTH-MIN_PADDING*2)//4,
              (CANVAS_HEIGHT-MIN_PADDING*2)//8)
X_PADDING = (CANVAS_WIDTH-SPACING*4)//2
Y_PADDING = (CANVAS_HEIGHT-SPACING*8)//2

MAX_DOG_ALLOWED = 24

GAME_MODES = (PVP, PLAY_DEER, PLAY_DOG, WATCH_AI)

game_mode = PVP
selected_cod = -1, -1


def transform_to_canvas_coordinate(_x: int, _y: int) -> Tuple[int, int]:
    return _y, CANVAS_HEIGHT-_x


def get_canvas_coordinate_from_chessboard(_x: int, _y: int) -> Tuple[int, int]:
    return transform_to_canvas_coordinate(Y_PADDING+SPACING*_x, X_PADDING+SPACING*_y)


def cod_trans(_x: int, _y: int) -> Tuple[int, int]:
    return get_canvas_coordinate_from_chessboard(_x, _y)


def trans_to_board(_x: int, _y: int) -> Tuple[int, int]:
    board_x = (_y-Y_PADDING+SPACING//2)//SPACING
    board_x = 8-board_x
    board_y = (_x-X_PADDING+SPACING//2)//SPACING
    if board_x < 0:
        board_x = 0
    if board_x > 8:
        board_x = 8
    if board_y < 0:
        board_y = 0
    if board_y > 4:
        board_y = 4
    return board_x, board_y


def redraw_chessboard(canvas: tkinter.Canvas, board: rules.Chessboard):
    canvas.delete(tkinter.ALL)
    canvas.create_line(cod_trans(0, 0), cod_trans(0, 4), fill="white", width=3)
    canvas.create_line(cod_trans(1, 1), cod_trans(1, 3), fill="white", width=3)
    canvas.create_line(cod_trans(2, 0), cod_trans(2, 4), fill="white", width=3)
    canvas.create_line(cod_trans(3, 0), cod_trans(3, 4), fill="white", width=3)
    canvas.create_line(cod_trans(4, 0), cod_trans(4, 4), fill="white", width=3)
    canvas.create_line(cod_trans(5, 0), cod_trans(5, 4), fill="white", width=3)
    canvas.create_line(cod_trans(6, 0), cod_trans(6, 4), fill="white", width=3)
    canvas.create_line(cod_trans(7, 1), cod_trans(7, 3), fill="white", width=3)

    canvas.create_line(cod_trans(2, 0), cod_trans(6, 0), fill="white", width=3)
    canvas.create_line(cod_trans(2, 1), cod_trans(6, 1), fill="white", width=3)
    canvas.create_line(cod_trans(0, 2), cod_trans(8, 2), fill="white", width=3)
    canvas.create_line(cod_trans(2, 3), cod_trans(6, 3), fill="white", width=3)
    canvas.create_line(cod_trans(2, 4), cod_trans(6, 4), fill="white", width=3)

    canvas.create_line(cod_trans(0, 0), cod_trans(4, 4), fill="white", width=3)
    canvas.create_line(cod_trans(2, 0), cod_trans(6, 4), fill="white", width=3)
    canvas.create_line(cod_trans(4, 0), cod_trans(7, 3), fill="white", width=3)
    canvas.create_line(cod_trans(7, 1), cod_trans(8, 2), fill="white", width=3)

    canvas.create_line(cod_trans(4, 0), cod_trans(0, 4), fill="white", width=3)
    canvas.create_line(cod_trans(6, 0), cod_trans(2, 4), fill="white", width=3)
    canvas.create_line(cod_trans(7, 1), cod_trans(4, 4), fill="white", width=3)
    canvas.create_line(cod_trans(8, 2), cod_trans(7, 3), fill="white", width=3)

    for i in range(9):
        for j in range(5):
            cod = cod_trans(i, j)
            if board.grids[i][j].state == DEER:
                canvas.create_oval(cod[0]-SPACING//3, cod[1]-SPACING //
                                   3, cod[0]+SPACING//3, cod[1]+SPACING//3, fill="black")
                canvas.create_text(cod[0], cod[1], font=(
                    "Segoe UI Emoji", 18), text="🦌", fill="white")
            if board.grids[i][j].state == DOG:
                canvas.create_oval(cod[0]-SPACING//3, cod[1]-SPACING //
                                   3, cod[0]+SPACING//3, cod[1]+SPACING//3, fill="white")
                canvas.create_text(cod[0], cod[1], font=(
                    "Segoe UI Emoji", 18), text="🐕", fill="black")


def ai_make_move():
    _turn_and_result_content = turn_and_result_text.get()
    turn_and_result_text.set("Please wait...")
    if inner_board.current_turn == DEER and (game_mode == PLAY_DOG or game_mode == WATCH_AI):
        ai_move = ai_player.get_next_move(inner_board)
        inner_board.move_deer(
            ai_move[0], ai_move[1], ai_move[2], ai_move[3])
        inner_board.current_turn = DOG
    elif inner_board.current_turn == DOG and (game_mode == PLAY_DEER or game_mode == WATCH_AI):
        ai_move = ai_player.get_next_move(inner_board)
        if inner_board.total_dog_cnt < inner_board.max_dog_allowed:
            inner_board.put_in_dog(ai_move[0], ai_move[1])
        else:
            inner_board.move_dog(
                ai_move[0], ai_move[1], ai_move[2], ai_move[3])
        inner_board.current_turn = DEER
    turn_and_result_text.set(_turn_and_result_content)


def judge_and_set_text():
    result_jugded = inner_board.judge_result()
    # set turn_and_result_text
    if result_jugded == DEER:
        turn_and_result_text.set("Deer won!")
        inner_board.current_turn = INVALID
    elif result_jugded == DOG:
        turn_and_result_text.set("Dog won!")
        inner_board.current_turn = INVALID
    else:
        if inner_board.current_turn == DEER:
            turn_and_result_text.set("Deer's turn")
        elif inner_board.current_turn == DOG:
            turn_and_result_text.set("Dog's turn")
    # set dog_count_text
    dog_count_text.set("Dogs put on the board: %02d/%d" %
                       (inner_board.total_dog_cnt, inner_board.max_dog_allowed))
    # redraw
    redraw_chessboard(w, inner_board)


def on_click(ev: tkinter.Event):
    global selected_cod
    if game_mode == WATCH_AI:
        return
    clicked_cod = trans_to_board(ev.x, ev.y)
    if inner_board.current_turn == DEER and game_mode != PLAY_DOG:
        # select the deer to move
        if inner_board.grids[clicked_cod[0]][clicked_cod[1]].state == DEER:
            selected_cod = clicked_cod
            selected_cod_text.set("Selecting %d, %d" %
                                  (selected_cod[0], selected_cod[1]))
        # move the deer
        elif inner_board.move_deer(selected_cod[0], selected_cod[1], clicked_cod[0], clicked_cod[1]):
            selected_cod = -1, -1
            selected_cod_text.set("Not selected")
            inner_board.current_turn = DOG
    elif inner_board.current_turn == DOG and game_mode != PLAY_DEER:
        # put a new dog onto the board
        if inner_board.total_dog_cnt < inner_board.max_dog_allowed and inner_board.put_in_dog(clicked_cod[0], clicked_cod[1]):
            selected_cod = -1, -1
            selected_cod_text.set("Not selected")
            inner_board.current_turn = DEER
        elif inner_board.total_dog_cnt == inner_board.max_dog_allowed:
            # select the dog to move
            if inner_board.grids[clicked_cod[0]][clicked_cod[1]].state == DOG:
                selected_cod = clicked_cod
                selected_cod_text.set("Selecting %d, %d" %
                                      (selected_cod[0], selected_cod[1]))
            # move the dog
            elif inner_board.move_dog(selected_cod[0], selected_cod[1], clicked_cod[0], clicked_cod[1]):
                selected_cod = -1, -1
                selected_cod_text.set("Not selected")
                inner_board.current_turn = DEER

    judge_and_set_text()

    # AI makes move
    if game_mode == PLAY_DOG or game_mode == PLAY_DEER:
        ai_make_move()
        judge_and_set_text()


def on_click_new_game():
    global game_mode, selected_cod
    game_mode = GAME_MODES[game_modes_var.get()]
    turn_and_result_text.set("Deer's turn")
    dog_count_text.set("Dogs put on the board: 08/%d" % MAX_DOG_ALLOWED)
    selected_cod = -1, -1
    selected_cod_text.set("Not selected")
    inner_board.set_up_new_game()
    redraw_chessboard(w, inner_board)
    if game_mode == PLAY_DOG:
        ai_make_move()
        judge_and_set_text()
    elif game_mode == WATCH_AI:
        while inner_board.current_turn == DEER or inner_board.current_turn == DOG:
            ai_make_move()
            judge_and_set_text()


if __name__ == "__main__":
    ai_player = godeer.AutoChess()
    inner_board = rules.Chessboard(MAX_DOG_ALLOWED)
    inner_board.set_up_new_game()
    root = tkinter.Tk()
    root.title("Deer chess")
    root.geometry("900x700")
    root.resizable(width=0, height=0)
    w = tkinter.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
                       background="olive", relief=tkinter.FLAT)
    redraw_chessboard(w, inner_board)
    w.bind("<Button-1>", on_click)

    game_modes_var = tkinter.IntVar()
    game_mode_frame = tkinter.LabelFrame(
        root, font=("Consolas", 16), text="Choose game mode")
    for i in range(len(GAME_MODES)):
        tkinter.Radiobutton(game_mode_frame, font=("Consolas", 12),
                            text=GAME_MODES[i], variable=game_modes_var, value=i).pack(anchor=tkinter.W)
    turn_and_result_text = tkinter.StringVar()
    turn_and_result_text.set("Deer's turn")
    dog_count_text = tkinter.StringVar()
    dog_count_text.set("Dogs put on the board: 08/%d" % MAX_DOG_ALLOWED)
    selected_cod_text = tkinter.StringVar()
    selected_cod_text.set("Not selected")
    tkinter.Label(root, font=("Consolas", 20),
                  textvariable=turn_and_result_text).grid(column=0, row=0)
    tkinter.Label(root, font=("Consolas", 20),
                  textvariable=dog_count_text).grid(column=0, row=1)
    tkinter.Label(root, font=("Consolas", 20),
                  textvariable=selected_cod_text).grid(column=0, row=2)
    game_mode_frame.grid(column=0, row=3)
    tkinter.Button(root, font=("Consolas", 16), text="New game",
                   command=on_click_new_game).grid(column=0, row=4)
    w.grid(column=1, row=0, rowspan=5)
    tkinter.mainloop()
