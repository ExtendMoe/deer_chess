import math
import random
from typing import Tuple
from constants import CAPTURE, DEER, DOG
import rules


class AutoChess:
    def __init__(self) -> None:
        pass

    def copy_board_state(source_board: rules.Chessboard, destination_board: rules.Chessboard):
        destination_board.current_turn = source_board.current_turn
        destination_board.max_dog_allowed = source_board.max_dog_allowed
        destination_board.active_dog_cnt = source_board.active_dog_cnt
        for i in range(9):
            for j in range(5):
                destination_board.grids[i][j].state = source_board.grids[i][j].state
        destination_board.total_dog_cnt = source_board.total_dog_cnt
        destination_board.active_dog_cnt = source_board.active_dog_cnt

    def generate_random_deer_move(board: rules.Chessboard) -> Tuple[int, int, int, int]:
        possible_moves = board.get_possible_deer_moves()
        if len(possible_moves) > 0:
            return possible_moves[random.randrange(len(possible_moves))][:4]
        else:
            return (-1, -1, -1, -1)

    def generate_random_dog_move(board: rules.Chessboard) -> Tuple[int, int, int, int]:
        possible_moves = board.get_possible_dog_actions()
        if len(possible_moves) > 0:
            return possible_moves[random.randrange(len(possible_moves))][:4]
        else:
            return (-1, -1, -1, -1)

    def make_deer_move(board: rules.Chessboard, move_tuple: Tuple[int, int, int, int]):
        board.move_deer(move_tuple[0], move_tuple[1],
                        move_tuple[2], move_tuple[3])
        board.current_turn = DOG

    def make_dog_move(board: rules.Chessboard, move_tuple: Tuple[int, int, int, int]):
        if board.total_dog_cnt < board.max_dog_allowed:
            board.put_in_dog(move_tuple[0], move_tuple[1])
        else:
            board.move_dog(move_tuple[0], move_tuple[1],
                           move_tuple[2], move_tuple[3])
        board.current_turn = DEER

    def merge_dog_survive_and_deer_possible_move(dog_survive: int, deer_possible_move: int) -> int:
        return math.floor(math.log(deer_possible_move+0.1)*2)-dog_survive*3

    def search_deer_move(_board: rules.Chessboard,
                         current_search_depth: int,
                         max_search_depth: int) -> Tuple[int, int, int, int, int, int]:
        """
        Returns
        -------
        Tuple[dog_survive, deer_possible_move, x0, y0, x1, y1]
            - for deer, try to minimize dog_survive and maximize deer_possible_move
            - if deer can win within one move, return (0, 1000)
            - [x0, y0, x1, y1] means the best move a deer can make
        """
        board = rules.Chessboard(0)
        AutoChess.copy_board_state(_board, board)
        all_moves_with_attr = board.get_possible_deer_moves()
        all_moves = [i[:4] for i in all_moves_with_attr]
        if current_search_depth == max_search_depth:
            processed_move_cnt = 0
            for i in all_moves_with_attr:
                if i[4] == CAPTURE:
                    processed_move_cnt += 2
                else:
                    processed_move_cnt += 1
            return (board.active_dog_cnt, processed_move_cnt, all_moves[0][0], all_moves[0][1], all_moves[0][2], all_moves[0][3])
        # find min of max
        dog_survive_cnt_list = [0]*len(all_moves)
        # find max of min
        deer_possible_move_cnt_list = [0]*len(all_moves)
        for idx, move in enumerate(all_moves):
            AutoChess.make_deer_move(board, move)
            if board.judge_result() == DEER:
                return (0, 1000, move[0], move[1], move[2], move[3])
            else:
                _result = AutoChess.search_dog_move(
                    board, current_search_depth+1, max_search_depth)
                dog_survive_cnt_list[idx] = _result[0]
                deer_possible_move_cnt_list[idx] = _result[1]
            AutoChess.copy_board_state(_board, board)
        _now_max = -10000
        _now_max_idx_list = [0]
        for i in range(len(all_moves)):
            _value = AutoChess.merge_dog_survive_and_deer_possible_move(
                dog_survive_cnt_list[i], deer_possible_move_cnt_list[i])
            if _value > _now_max:
                _now_max = _value
                _now_max_idx_list.clear()
                _now_max_idx_list.append(i)
            elif _value == _now_max:
                _now_max_idx_list.append(i)
        _now_max_idx = random.choice(_now_max_idx_list)
        return (dog_survive_cnt_list[_now_max_idx],
                deer_possible_move_cnt_list[_now_max_idx],
                all_moves[_now_max_idx][0],
                all_moves[_now_max_idx][1],
                all_moves[_now_max_idx][2],
                all_moves[_now_max_idx][3])

    def search_dog_move(_board: rules.Chessboard,
                        current_search_depth: int,
                        max_search_depth: int) -> Tuple[int, int, int, int, int, int]:
        """
        Returns
        -------
        Tuple[dog_survive, deer_possible_move, random_result, x0, y0, x1, y1]
            - for dog, try to maximize dog_survive and minimize deer_possible_move
            - if dog can win within one move, return (1000, 0)
            - [x0, y0, x1, y1] means the best move a dog can make
        """
        board = rules.Chessboard(0)
        AutoChess.copy_board_state(_board, board)
        all_moves_with_attr = board.get_possible_dog_actions()
        all_moves = [i[:4] for i in all_moves_with_attr]
        if current_search_depth == max_search_depth:
            deer_all_moves_with_attr = board.get_possible_deer_moves()
            processed_move_cnt = 0
            for i in deer_all_moves_with_attr:
                if i[4] == CAPTURE:
                    processed_move_cnt += 2
                else:
                    processed_move_cnt += 1
            return (board.active_dog_cnt, processed_move_cnt, all_moves[0][0], all_moves[0][1], all_moves[0][2], all_moves[0][3])
        # find max of min
        dog_survive_cnt_list = [0]*len(all_moves)
        # find min of max
        deer_possible_move_cnt_list = [0]*len(all_moves)
        for idx, move in enumerate(all_moves):
            AutoChess.make_dog_move(board, move)
            if board.judge_result() == DOG:
                return (1000, 0, move[0], move[1], move[2], move[3])
            else:
                _result = AutoChess.search_deer_move(
                    board, current_search_depth+1, max_search_depth)
                dog_survive_cnt_list[idx] = _result[0]
                deer_possible_move_cnt_list[idx] = _result[1]
            AutoChess.copy_board_state(_board, board)
        _now_max = -10000
        _now_max_idx_list = [0]
        for i in range(len(all_moves)):
            _value = -AutoChess.merge_dog_survive_and_deer_possible_move(
                dog_survive_cnt_list[i], deer_possible_move_cnt_list[i])
            if _value > _now_max:
                _now_max = _value
                _now_max_idx_list.clear()
                _now_max_idx_list.append(i)
            elif _value == _now_max:
                _now_max_idx_list.append(i)
        _now_max_idx = random.choice(_now_max_idx_list)
        return (dog_survive_cnt_list[_now_max_idx],
                deer_possible_move_cnt_list[_now_max_idx],
                all_moves[_now_max_idx][0],
                all_moves[_now_max_idx][1],
                all_moves[_now_max_idx][2],
                all_moves[_now_max_idx][3])

    def get_next_move(self, current_board: rules.Chessboard) -> Tuple[int, int, int, int]:
        """
        Get suggestion about the next move.

        Parameters
        ----------
        `current_board` : rules.Chessboard
            The current state of chessboard.

        Returns
        -------
        Tuple[x0, y0, x1, y1]
            - for deer, it means moving the deer from (x0, y0) to (x1, y1).
            - for dog during piece-putting stage, it means putting a dog on (x0, y0). x1 and y1 are set to -1.
            - for dog during piece-moving stage, it means moving the dog from (x0, y0) to (x1, y1).
            - if no legal move can be made, then return (-1, -1, -1, -1).
        """
        if current_board.current_turn == DEER:
            # return AutoChess.generate_random_deer_move(current_board)
            _result = AutoChess.search_deer_move(current_board, 0, 3)
            return (_result[2], _result[3], _result[4], _result[5])
        elif current_board.current_turn == DOG:
            # return AutoChess.generate_random_dog_move(current_board)
            _result = AutoChess.search_dog_move(current_board, 0, 3)
            return (_result[2], _result[3], _result[4], _result[5])
        else:
            return (-1, -1, -1, -1)


if __name__ == "__main__":
    pass
