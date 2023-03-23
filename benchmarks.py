"""Benchmark Problems

- Parity
- Symbolic regression
- Artificial ant

Created by Yifan He (heyif@outlook.com)
Last update on Feb 20, 2023
"""
import copy
from functools import partial


class SymbolicRegression:

    def __init__(
        self,
        func = lambda x: sum(x*x),
        inputs = None
    ):
        self.func = func
        self.inputs = inputs
        self.n_inputs = len(self.inputs[0])
        self.dataset = self.get_dataset()

    def evaluate(self, x):
        s = 0
        for input, output in zip(*self.dataset):
            s += abs(x(*input) - output)
        return s/len(self.dataset),

    def get_dataset(self):
        inputs = self.inputs
        outputs = [self.func(*x) for x in inputs]
        return inputs, outputs


class Parity:

    def __init__(
        self,
        n_inputs: int = 6,
    ):
        self.n_inputs = n_inputs
        self.size = 2**self.n_inputs
        self.dataset = self.get_dataset()

    def evaluate(self, x):
        passed = 0
        for input, output in zip(*self.dataset):
            if x(*input) == output:
                passed += 1
        return passed,

    def get_dataset(self):
        inputs = [None] * self.size
        outputs = [None] * self.size

        for i in range(self.size):
            inputs[i] = [None] * self.n_inputs
            value = i
            dividor = self.size
            parity = 1
            for j in range(self.n_inputs):
                dividor /= 2
                if value >= dividor:
                    inputs[i][j] = 1
                    parity = int(not parity)
                    value -= dividor
                else:
                    inputs[i][j] = 0
            outputs[i] = parity
        return inputs, outputs


def if_then_else(condition, out1, out2):
    out1() if condition() else out2()


class AntSimulator(object):
    direction = ["north","east","south","west"]
    dir_row = [1, 0, -1, 0]
    dir_col = [0, 1, 0, -1]

    def __init__(self, max_moves):
        self.max_moves = max_moves
        self.moves = 0
        self.eaten = 0
        self.routine = None

    def _reset(self):
        self.row = self.row_start 
        self.col = self.col_start 
        self.dir = 1
        self.moves = 0  
        self.eaten = 0
        self.matrix_exc = copy.deepcopy(self.matrix)

    @property
    def position(self):
        return (self.row, self.col, self.direction[self.dir])

    def turn_left(self): 
        if self.moves < self.max_moves:
            self.moves += 1
            self.dir = (self.dir - 1) % 4

    def turn_right(self):
        if self.moves < self.max_moves:
            self.moves += 1    
            self.dir = (self.dir + 1) % 4

    def move_forward(self):
        if self.moves < self.max_moves:
            self.moves += 1
            self.row = (self.row + self.dir_row[self.dir]) % self.matrix_row
            self.col = (self.col + self.dir_col[self.dir]) % self.matrix_col
            if self.matrix_exc[self.row][self.col] == "food":
                self.eaten += 1
            self.matrix_exc[self.row][self.col] = "passed"

    def sense_food(self):
        ahead_row = (self.row + self.dir_row[self.dir]) % self.matrix_row
        ahead_col = (self.col + self.dir_col[self.dir]) % self.matrix_col        
        return self.matrix_exc[ahead_row][ahead_col] == "food"

    def if_food_ahead(self, out1, out2):
        return partial(if_then_else, self.sense_food, out1, out2)

    def run(self,routine):
        self._reset()
        while self.moves < self.max_moves:
            routine()

    def parse_matrix(self, matrix):
        self.matrix = list()
        for i, line in enumerate(matrix):
            self.matrix.append(list())
            for j, col in enumerate(line):
                if col == "#":
                    self.matrix[-1].append("food")
                elif col == ".":
                    self.matrix[-1].append("empty")
                elif col == "S":
                    self.matrix[-1].append("empty")
                    self.row_start = self.row = i
                    self.col_start = self.col = j
                    self.dir = 1
        self.matrix_row = len(self.matrix)
        self.matrix_col = len(self.matrix[0])
        self.matrix_exc = copy.deepcopy(self.matrix)
