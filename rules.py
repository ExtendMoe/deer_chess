from typing import Dict, List, Tuple
from constants import *


def is_coordinate_legal(_x: int, _y: int) -> bool:
    return 0 <= _x and _x < 9 and 0 <= _y and _y < 5


class BoardGrid:
    def __init__(self, _x: int, _y: int) -> None:
        self._x = _x
        self._y = _y
        self.links: Dict[str, BoardGrid] = {}
        self.state = EMPTY


class Chessboard:
    def __init__(self, max_dog_allowed: int) -> None:
        self.current_turn = DEER
        self.max_dog_allowed = max_dog_allowed
        self.grids: List[List[BoardGrid]] = []
        for i in range(9):
            _row = []
            for j in range(5):
                _row.append(BoardGrid(i, j))
            self.grids.append(_row)
        self.grids[0][1].state = INVALID
        self.grids[0][3].state = INVALID
        self.grids[1][0].state = INVALID
        self.grids[1][4].state = INVALID
        self.grids[7][0].state = INVALID
        self.grids[7][4].state = INVALID
        self.grids[8][0].state = INVALID
        self.grids[8][1].state = INVALID
        self.grids[8][3].state = INVALID
        self.grids[8][4].state = INVALID

        self.grids[0][0].state = EMPTY
        self.grids[0][0].links[NE] = self.grids[1][1]
        self.grids[0][0].links[E] = self.grids[0][2]

        self.grids[0][2].state = EMPTY
        self.grids[0][2].links[N] = self.grids[1][2]
        self.grids[0][2].links[E] = self.grids[0][4]
        self.grids[0][2].links[W] = self.grids[0][0]

        self.grids[0][4].state = EMPTY
        self.grids[0][4].links[NW] = self.grids[1][3]
        self.grids[0][4].links[W] = self.grids[0][2]

        self.grids[1][1].state = EMPTY
        self.grids[1][1].links[NE] = self.grids[2][2]
        self.grids[1][1].links[E] = self.grids[1][2]
        self.grids[1][1].links[SW] = self.grids[0][0]

        self.grids[1][2].state = EMPTY
        self.grids[1][2].links[N] = self.grids[2][2]
        self.grids[1][2].links[E] = self.grids[1][3]
        self.grids[1][2].links[S] = self.grids[0][2]
        self.grids[1][2].links[W] = self.grids[1][1]

        self.grids[1][3].state = EMPTY
        self.grids[1][3].links[NW] = self.grids[2][2]
        self.grids[1][3].links[SE] = self.grids[0][4]
        self.grids[1][3].links[W] = self.grids[1][2]

        self.grids[2][0].state = EMPTY
        self.grids[2][0].links[N] = self.grids[3][0]
        self.grids[2][0].links[NE] = self.grids[3][1]
        self.grids[2][0].links[E] = self.grids[2][1]

        self.grids[2][1].state = EMPTY
        self.grids[2][1].links[N] = self.grids[3][1]
        self.grids[2][1].links[E] = self.grids[2][2]
        self.grids[2][1].links[W] = self.grids[2][0]

        self.grids[2][2].state = EMPTY
        self.grids[2][2].links[NW] = self.grids[3][1]
        self.grids[2][2].links[N] = self.grids[3][2]
        self.grids[2][2].links[NE] = self.grids[3][3]
        self.grids[2][2].links[E] = self.grids[2][3]
        self.grids[2][2].links[SE] = self.grids[1][3]
        self.grids[2][2].links[S] = self.grids[1][2]
        self.grids[2][2].links[SW] = self.grids[1][1]
        self.grids[2][2].links[W] = self.grids[2][1]

        self.grids[2][3].state = EMPTY
        self.grids[2][3].links[N] = self.grids[3][3]
        self.grids[2][3].links[E] = self.grids[2][4]
        self.grids[2][3].links[W] = self.grids[2][2]

        self.grids[2][4].state = EMPTY
        self.grids[2][4].links[NW] = self.grids[3][3]
        self.grids[2][4].links[N] = self.grids[3][4]
        self.grids[2][4].links[W] = self.grids[2][3]

        self.grids[3][0].state = EMPTY
        self.grids[3][0].links[N] = self.grids[4][0]
        self.grids[3][0].links[E] = self.grids[3][1]
        self.grids[3][0].links[S] = self.grids[2][0]

        self.grids[3][1].state = EMPTY
        self.grids[3][1].links[NW] = self.grids[4][0]
        self.grids[3][1].links[N] = self.grids[4][1]
        self.grids[3][1].links[NE] = self.grids[4][2]
        self.grids[3][1].links[E] = self.grids[3][2]
        self.grids[3][1].links[SE] = self.grids[2][2]
        self.grids[3][1].links[S] = self.grids[2][1]
        self.grids[3][1].links[SW] = self.grids[2][0]
        self.grids[3][1].links[W] = self.grids[3][0]

        self.grids[3][2].state = EMPTY
        self.grids[3][2].links[N] = self.grids[4][2]
        self.grids[3][2].links[E] = self.grids[3][3]
        self.grids[3][2].links[S] = self.grids[2][2]
        self.grids[3][2].links[W] = self.grids[3][1]

        self.grids[3][3].state = EMPTY
        self.grids[3][3].links[NW] = self.grids[4][2]
        self.grids[3][3].links[N] = self.grids[4][3]
        self.grids[3][3].links[NE] = self.grids[4][4]
        self.grids[3][3].links[E] = self.grids[3][4]
        self.grids[3][3].links[SE] = self.grids[2][4]
        self.grids[3][3].links[S] = self.grids[2][3]
        self.grids[3][3].links[SW] = self.grids[2][2]
        self.grids[3][3].links[W] = self.grids[3][2]

        self.grids[3][4].state = EMPTY
        self.grids[3][4].links[N] = self.grids[4][4]
        self.grids[3][4].links[S] = self.grids[2][4]
        self.grids[3][4].links[W] = self.grids[3][3]

        self.grids[4][0].state = EMPTY
        self.grids[4][0].links[N] = self.grids[5][0]
        self.grids[4][0].links[NE] = self.grids[5][1]
        self.grids[4][0].links[E] = self.grids[4][1]
        self.grids[4][0].links[SE] = self.grids[3][1]
        self.grids[4][0].links[S] = self.grids[3][0]

        self.grids[4][1].state = EMPTY
        self.grids[4][1].links[N] = self.grids[5][1]
        self.grids[4][1].links[E] = self.grids[4][2]
        self.grids[4][1].links[S] = self.grids[3][1]
        self.grids[4][1].links[W] = self.grids[4][0]

        self.grids[4][2].state = EMPTY
        self.grids[4][2].links[NW] = self.grids[5][1]
        self.grids[4][2].links[N] = self.grids[5][2]
        self.grids[4][2].links[NE] = self.grids[5][3]
        self.grids[4][2].links[E] = self.grids[4][3]
        self.grids[4][2].links[SE] = self.grids[3][3]
        self.grids[4][2].links[S] = self.grids[3][2]
        self.grids[4][2].links[SW] = self.grids[3][1]
        self.grids[4][2].links[W] = self.grids[4][1]

        self.grids[4][3].state = EMPTY
        self.grids[4][3].links[N] = self.grids[5][3]
        self.grids[4][3].links[E] = self.grids[4][4]
        self.grids[4][3].links[S] = self.grids[3][3]
        self.grids[4][3].links[W] = self.grids[4][2]

        self.grids[4][4].state = EMPTY
        self.grids[4][4].links[NW] = self.grids[5][3]
        self.grids[4][4].links[N] = self.grids[5][4]
        self.grids[4][4].links[S] = self.grids[3][4]
        self.grids[4][4].links[SW] = self.grids[3][3]
        self.grids[4][4].links[W] = self.grids[4][3]

        self.grids[5][0].state = EMPTY
        self.grids[5][0].links[N] = self.grids[6][0]
        self.grids[5][0].links[E] = self.grids[5][1]
        self.grids[5][0].links[S] = self.grids[4][0]

        self.grids[5][1].state = EMPTY
        self.grids[5][1].links[NW] = self.grids[6][0]
        self.grids[5][1].links[N] = self.grids[6][1]
        self.grids[5][1].links[NE] = self.grids[6][2]
        self.grids[5][1].links[E] = self.grids[5][2]
        self.grids[5][1].links[SE] = self.grids[4][2]
        self.grids[5][1].links[S] = self.grids[4][1]
        self.grids[5][1].links[SW] = self.grids[4][0]
        self.grids[5][1].links[W] = self.grids[5][0]

        self.grids[5][2].state = EMPTY
        self.grids[5][2].links[N] = self.grids[6][2]
        self.grids[5][2].links[E] = self.grids[5][3]
        self.grids[5][2].links[S] = self.grids[4][2]
        self.grids[5][2].links[W] = self.grids[5][1]

        self.grids[5][3].state = EMPTY
        self.grids[5][3].links[NW] = self.grids[6][2]
        self.grids[5][3].links[N] = self.grids[6][3]
        self.grids[5][3].links[NE] = self.grids[6][4]
        self.grids[5][3].links[E] = self.grids[5][4]
        self.grids[5][3].links[SE] = self.grids[4][4]
        self.grids[5][3].links[S] = self.grids[4][3]
        self.grids[5][3].links[SW] = self.grids[4][2]
        self.grids[5][3].links[W] = self.grids[5][2]

        self.grids[5][4].state = EMPTY
        self.grids[5][4].links[N] = self.grids[6][4]
        self.grids[5][4].links[S] = self.grids[4][4]
        self.grids[5][4].links[W] = self.grids[5][3]

        self.grids[6][0].state = EMPTY
        self.grids[6][0].links[E] = self.grids[6][1]
        self.grids[6][0].links[SE] = self.grids[5][1]
        self.grids[6][0].links[S] = self.grids[5][0]

        self.grids[6][1].state = EMPTY
        self.grids[6][1].links[E] = self.grids[6][2]
        self.grids[6][1].links[S] = self.grids[5][1]
        self.grids[6][1].links[W] = self.grids[6][0]

        self.grids[6][2].state = EMPTY
        self.grids[6][2].links[NW] = self.grids[7][1]
        self.grids[6][2].links[N] = self.grids[7][2]
        self.grids[6][2].links[NE] = self.grids[7][3]
        self.grids[6][2].links[E] = self.grids[6][3]
        self.grids[6][2].links[SE] = self.grids[5][3]
        self.grids[6][2].links[S] = self.grids[5][2]
        self.grids[6][2].links[SW] = self.grids[5][1]
        self.grids[6][2].links[W] = self.grids[6][1]

        self.grids[6][3].state = EMPTY
        self.grids[6][3].links[E] = self.grids[6][4]
        self.grids[6][3].links[S] = self.grids[5][3]
        self.grids[6][3].links[W] = self.grids[6][2]

        self.grids[6][4].state = EMPTY
        self.grids[6][4].links[S] = self.grids[5][4]
        self.grids[6][4].links[SW] = self.grids[5][3]
        self.grids[6][4].links[W] = self.grids[6][3]

        self.grids[7][1].state = EMPTY
        self.grids[7][1].links[NE] = self.grids[8][2]
        self.grids[7][1].links[E] = self.grids[7][2]
        self.grids[7][1].links[SE] = self.grids[6][2]

        self.grids[7][2].state = EMPTY
        self.grids[7][2].links[N] = self.grids[8][2]
        self.grids[7][2].links[E] = self.grids[7][3]
        self.grids[7][2].links[S] = self.grids[6][2]
        self.grids[7][2].links[W] = self.grids[7][1]

        self.grids[7][3].state = EMPTY
        self.grids[7][3].links[NW] = self.grids[8][2]
        self.grids[7][3].links[SW] = self.grids[6][2]
        self.grids[7][3].links[W] = self.grids[7][2]

        self.grids[8][2].state = EMPTY
        self.grids[8][2].links[SE] = self.grids[7][3]
        self.grids[8][2].links[S] = self.grids[7][2]
        self.grids[8][2].links[SW] = self.grids[7][1]

        self.total_dog_cnt = 0
        self.active_dog_cnt = 0

    def set_up_new_game(self) -> None:
        self.current_turn = DEER
        for i in range(9):
            for j in range(5):
                if self.grids[i][j].state != INVALID:
                    self.grids[i][j].state = EMPTY
        self.grids[3][1].state = DOG
        self.grids[3][2].state = DOG
        self.grids[3][3].state = DOG
        self.grids[4][1].state = DOG
        self.grids[4][3].state = DOG
        self.grids[5][1].state = DOG
        self.grids[5][2].state = DOG
        self.grids[5][3].state = DOG
        self.grids[2][2].state = DEER
        self.grids[6][2].state = DEER
        self.total_dog_cnt = 8
        self.active_dog_cnt = 8

    def put_in_dog(self, _x: int, _y: int) -> bool:
        if is_coordinate_legal(_x, _y) and self.grids[_x][_y].state == EMPTY:
            self.grids[_x][_y].state = DOG
            self.total_dog_cnt += 1
            self.active_dog_cnt += 1
            return True
        return False

    def move_dog(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        if is_coordinate_legal(from_x, from_y) and is_coordinate_legal(to_x, to_y):
            if self.grids[from_x][from_y].state == DOG and self.grids[to_x][to_y].state == EMPTY:
                for linked_grid in self.grids[from_x][from_y].links.values():
                    if linked_grid._x == to_x and linked_grid._y == to_y:
                        self.grids[from_x][from_y].state = EMPTY
                        self.grids[to_x][to_y].state = DOG
                        return True
        return False

    def move_deer(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        if is_coordinate_legal(from_x, from_y) and is_coordinate_legal(to_x, to_y):
            if self.grids[from_x][from_y].state == DEER and self.grids[to_x][to_y].state == EMPTY:
                # plain move
                for linked_grid in self.grids[from_x][from_y].links.values():
                    if linked_grid._x == to_x and linked_grid._y == to_y:
                        self.grids[from_x][from_y].state = EMPTY
                        self.grids[to_x][to_y].state = DEER
                        return True
                # capture a dog
                for link_key in self.grids[from_x][from_y].links.keys():
                    captured_grid = self.grids[from_x][from_y].links[link_key]
                    if captured_grid.state == DOG and link_key in captured_grid.links.keys() and captured_grid.links[link_key]._x == to_x and captured_grid.links[link_key]._y == to_y:
                        self.grids[from_x][from_y].state = EMPTY
                        self.grids[to_x][to_y].state = DEER
                        captured_grid.state = EMPTY
                        self.active_dog_cnt -= 1
                        return True
        return False

    def test_move_dog(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        if is_coordinate_legal(from_x, from_y) and is_coordinate_legal(to_x, to_y):
            if self.grids[from_x][from_y].state == DOG and self.grids[to_x][to_y].state == EMPTY:
                for linked_grid in self.grids[from_x][from_y].links.values():
                    if linked_grid._x == to_x and linked_grid._y == to_y:
                        return True
        return False

    def test_move_deer(self, from_x: int, from_y: int, to_x: int, to_y: int) -> Tuple[bool, bool]:
        # returns (is-able-to-move, is-capturing)
        if is_coordinate_legal(from_x, from_y) and is_coordinate_legal(to_x, to_y):
            if self.grids[from_x][from_y].state == DEER and self.grids[to_x][to_y].state == EMPTY:
                # plain move
                for linked_grid in self.grids[from_x][from_y].links.values():
                    if linked_grid._x == to_x and linked_grid._y == to_y:
                        return (True, False)
                # capture a dog
                for link_key in self.grids[from_x][from_y].links.keys():
                    captured_grid = self.grids[from_x][from_y].links[link_key]
                    if captured_grid.state == DOG and link_key in captured_grid.links.keys() and captured_grid.links[link_key]._x == to_x and captured_grid.links[link_key]._y == to_y:
                        return (True, True)
        return (False, False)

    def get_possible_dog_actions(self) -> List[Tuple[int, int, int, int, str]]:
        result: List[Tuple[int, int, int, int, str]] = []
        if self.total_dog_cnt < self.max_dog_allowed:
            for i in range(9):
                for j in range(5):
                    if self.grids[i][j].state == EMPTY:
                        result.append((i, j, -1, -1, PUT_IN))
        else:
            dogs: List[Tuple[int, int]] = []
            for i in range(9):
                for j in range(5):
                    if self.grids[i][j].state == DOG:
                        dogs.append((i, j))
            for dog in dogs:
                for i in range(9):
                    for j in range(5):
                        if self.test_move_dog(dog[0], dog[1], i, j):
                            result.append((dog[0], dog[1], i, j, MOVE))
        return result

    def get_possible_deer_moves(self) -> List[Tuple[int, int, int, int, str]]:
        result: List[Tuple[int, int, int, int, str]] = []
        deers: List[Tuple[int, int]] = []
        for i in range(9):
            for j in range(5):
                if self.grids[i][j].state == DEER:
                    deers.append((i, j))
        for deer in deers:
            for i in range(9):
                for j in range(5):
                    test_result = self.test_move_deer(deer[0], deer[1], i, j)
                    if test_result[0]:
                        if test_result[1]:
                            result.append((deer[0], deer[1], i, j, CAPTURE))
                        else:
                            result.append(
                                (deer[0], deer[1], i, j, NOT_CAPTURE))
        return result

    def judge_result(self):
        if self.active_dog_cnt < 4:
            return DEER
        # secure the hill
        if self.total_dog_cnt == self.max_dog_allowed:
            dog_in_the_hill_num = 0
            another_deer_in_the_hill = False
            if self.grids[2][2].state == DEER:
                for i in range(2):
                    for j in range(5):
                        if self.grids[i][j].state == DEER:
                            another_deer_in_the_hill = True
                        if self.grids[i][j].state == DOG:
                            dog_in_the_hill_num += 1
                if another_deer_in_the_hill and dog_in_the_hill_num < 3:
                    return DEER
            dog_in_the_hill_num = 0
            another_deer_in_the_hill = False
            if self.grids[6][2].state == DEER:
                for i in range(7, 9):
                    for j in range(5):
                        if self.grids[i][j].state == DEER:
                            another_deer_in_the_hill = True
                        if self.grids[i][j].state == DOG:
                            dog_in_the_hill_num += 1
                if another_deer_in_the_hill and dog_in_the_hill_num < 3:
                    return DEER
        if self.current_turn == DOG and len(self.get_possible_dog_actions()) == 0:
            return DEER
        if self.current_turn == DEER and len(self.get_possible_deer_moves()) == 0:
            return DOG
        return NOT_SET


if __name__ == "__main__":
    cb = Chessboard(24)
    cb.set_up_new_game()
    print(cb.get_possible_deer_moves())
    print(cb.get_possible_dog_actions())
    print(cb.judge_result())
