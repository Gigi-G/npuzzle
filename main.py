# description: main file for the puzzle solver
# author: Seminara Luigi
# date: 2023-01-18
# tags: python, puzzle, puzzle_state, puzzle_solver

import argparse
from puzzle.puzzle_solver import PuzzleSolver
import sys
import numpy as np
import glob as glob
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QComboBox, QLineEdit

class PuzzleWidget(QWidget):
    
    # the chosen algorithm
    chosen_algorithm = "BFS"
    
    # the chosen heuristic
    chosen_heuristic = None
    
    # the number of random walks
    random_walks = 1
    
    # the puzzle size
    puzzle_size = 3
    
    # the solution
    solution = []
    
    # the experiment folder
    experiment_folder = "./experiments/"
    
    # the experiment file
    experiment_files = []
    
    # tiles dimension
    size = 100
    
    
    def __init__(self, *args, **kwargs):
        # call the QWidget constructor
        super().__init__(*args, **kwargs)
        
        # create the buttons grid layout
        self.grid_layout = QGridLayout(self)
        
        parser = argparse.ArgumentParser()
        parser.add_argument("--ps", type=int, help="Size of the puzzle (e.g. 3 for a 3x3 puzzle)", default=3)
        parser.add_argument("--ts", type=int, help="Size of the tiles (e.g. 50 for 50x50 pixels)", default=50)
        args = parser.parse_args()
        
        self.puzzle_size = int(args.ps)
        self.size = int(args.ts)
            
        self.create_solution()
        
        self.create_tiles()
        
        self.create_solve_button()
        
        self.create_random_button()
        
        self.create_text_box()
        
        self.create_reset_button()
        
        self.create_algorithm_combo_box()
        
        self.create_experiments_combo_box()
        
        # set the initial puzzle
        self.set_puzzle(self.solution)



    def create_solution(self):
        count = 1
        for _ in range(self.puzzle_size):
            row = []
            for _ in range(self.puzzle_size):
                row.append(count)
                count += 1
            self.solution.append(row)
        self.solution[self.puzzle_size-1][self.puzzle_size-1] = 0


    
    def create_tiles(self):
        self.buttons = []
        for row in range(self.puzzle_size):
            button_row = []
            for col in range(self.puzzle_size):
                button = QPushButton(self)
                button.setFixedSize(self.size, self.size)
                self.grid_layout.addWidget(button, row, col)
                button_row.append(button)
            self.buttons.append(button_row)



    def create_solve_button(self):
        button = QPushButton(self)
        button.setFixedSize(self.size, self.size)
        button.setText('SOLVE')
        button.clicked.connect(self.solve)
        self.grid_layout.addWidget(button, self.puzzle_size, 0)
        
    
    
    def create_random_button(self):
        button = QPushButton(self)
        button.setFixedSize(self.size, self.size)
        button.setText('RND')
        button.clicked.connect(self.create_random_puzzle)
        self.grid_layout.addWidget(button, self.puzzle_size + 1, 0)
        
        
        
    def create_random_puzzle(self):
        for _ in range(self.random_walks):
            empty_row, empty_col = self.get_empty_tile()
            row = np.random.randint(0, self.puzzle_size)
            col = np.random.randint(0, self.puzzle_size)
            if abs(row - empty_row) + abs(col - empty_col) == 1:
                self.buttons[empty_row][empty_col].setText(self.buttons[row][col].text())
                self.buttons[row][col].setText('')



    def create_text_box(self):
        self.textbox = QLineEdit()
        self.textbox.setFixedSize(self.size, self.size)
        self.textbox.setText('1')
        self.textbox.textChanged.connect(self.textbox_changed)
        self.grid_layout.addWidget(self.textbox, self.puzzle_size + 1, 1)
        
        
        
    def textbox_changed(self, text):
        if text.isdigit():
            if int(text) > 0:
                self.random_walks = int(text)
            else:
                self.random_walks = 1
                self.textbox.setText('1')
            print("Number of random walks: " + str(self.random_walks))



    def create_reset_button(self):
        button = QPushButton(self)
        button.setFixedSize(self.size, self.size)
        button.setText('RESET')
        button.clicked.connect(self.reset_puzzle)
        self.grid_layout.addWidget(button, self.puzzle_size + 2, 0)
    
    
    
    def reset_puzzle(self):
        self.set_puzzle(self.solution)
    
    
    
    def create_algorithm_combo_box(self):
        self.algorithm_combo_box = QComboBox(self)
        self.algorithm_combo_box.addItems(['BFS', 'DFS', 'A*', 'IDA*'])
        self.algorithm_combo_box.currentIndexChanged.connect(self.algorithm_changed)
        self.algorithm_combo_box.setCurrentIndex(0)
        self.algorithm_combo_box.setFixedSize(self.size, self.size)
        self.grid_layout.addWidget(self.algorithm_combo_box, self.puzzle_size, 1)


    
    def algorithm_changed(self):
        self.chosen_algorithm = self.algorithm_combo_box.currentText()
        print(f"Selected {self.chosen_algorithm} algorithm.")
        if(self.chosen_algorithm == 'A*' or self.chosen_algorithm == 'IDA*'):
            value = input(
                "Please choose a heuristic fucntion:"    +
                "\n[1] Manhattan Distance"               +
                "\n[2] Euclidean Distance"               +
                "\n[3] Linear Conflict"                  +
                "\n[4] Misplaced Tiles"                  +   
                "\n[5] Linear Manhattan Conflict\n"
            )
            if(value == str(1)):
                self.chosen_heuristic = "manhattan_distance"
            elif(value == str(2)):
                self.chosen_heuristic = "euclidean_distance"
            elif(value == str(3)):
                self.chosen_heuristic = "linear_conflict"
            elif(value == str(4)):
                self.chosen_heuristic = "misplaced_tiles"
            elif(value == str(5)):
                self.chosen_heuristic = "linear_manhattan_conflict"
            else: 
                raise Exception("Wrong input heuristic function!") 



    def create_experiments_combo_box(self):
        self.experiments_combo_box = QComboBox(self)
        if self.puzzle_size == 3:
            self.experiment_folder = "experiments/3x3*"
        elif self.puzzle_size == 4:
            self.experiment_folder = "experiments/4x4*"
        elif self.puzzle_size == 5:
            self.experiment_folder = "experiments/5x5*"
        else:
            self.experiment_folder = ""
        self.experiment_files = glob.glob(self.experiment_folder + "*.txt")
        self.experiments_combo_box.addItems(self.experiment_files)
        self.experiments_combo_box.currentIndexChanged.connect(self.experiment_changed)
        self.experiments_combo_box.setCurrentIndex(0)
        self.experiments_combo_box.setFixedSize(self.size, self.size)
        self.grid_layout.addWidget(self.experiments_combo_box, self.puzzle_size + 2, 1)



    def experiment_changed(self):
        self.chosen_experiment = self.experiment_files[self.experiments_combo_box.currentIndex()]
        print(f"Selected {self.chosen_experiment} experiment.")
        self.set_puzzle(self.read_experiment(self.chosen_experiment))
        
        
        
    def read_experiment(self, file_name):
        with open(file_name, 'r') as file:
            data = file.read()
        data = data.split('\n')
        matrix = []
        for line in data:
            row = []
            values = line.split()
            for v in values:
                row.append(int(v))
            matrix.append(row)
        return matrix



    def set_puzzle(self, tiles):
        # set the buttons texts and connections
        for row in range(self.puzzle_size):
            for col in range(self.puzzle_size):
                value = tiles[row][col]
                self.buttons[row][col].setText(str(value) if value else '')
                self.buttons[row][col].clicked.connect(lambda _, r=row, c=col: self.move(r, c))



    def move(self, row, col):
        # get the empty tile position
        empty_row, empty_col = self.get_empty_tile()
        
        # if the clicked tile is adjacent to the empty tile, swap them
        if abs(row - empty_row) + abs(col - empty_col) == 1:
            self.buttons[empty_row][empty_col].setText(self.buttons[row][col].text())
            self.buttons[row][col].setText('')



    def get_empty_tile(self):
        # get the position of the empty tile
        for row in range(self.puzzle_size):
            for col in range(self.puzzle_size):
                if not self.buttons[row][col].text():
                    return row, col



    def solve(self):
        # get the starting puzzle
        start_state = [[int(self.buttons[row][col].text()) if self.buttons[row][col].text() else 0 for col in range(self.puzzle_size)] for row in range(self.puzzle_size)]
        start_state = [item for sublist in start_state for item in sublist]
        sol = [item for sublist in self.solution for item in sublist]
        
        solver = PuzzleSolver(start_state, sol, self.chosen_algorithm, heuristic=self.chosen_heuristic)
        path = solver.solve()
        
        # if the puzzle has been solved, show the solution
        if path:
            for puzzle in path:
                self.set_puzzle(puzzle)
                QApplication.processEvents()
                QApplication.instance().thread().msleep(500)    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = PuzzleWidget()
    widget.show()
    sys.exit(app.exec_())