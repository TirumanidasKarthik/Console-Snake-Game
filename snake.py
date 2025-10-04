import keyboard
import sys
from collections import deque
import os
import random

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = deque()
        self.velocity = 150 # In Iterations count
        self.direction = 'r' # Default direction
        self.iters = 0
 
    def moveSnakeRight(self):
        self.direction = 'r'
        head = self.positions[0]
        self.positions.appendleft((head[0], head[1] + 1))
        self.positions.pop()
    
    def moveSnakeLeft(self):
        self.direction = 'l'
        head = self.positions[0]
        self.positions.appendleft((head[0], head[1] - 1))
        self.positions.pop()

    def moveSnakeUp(self):
        self.direction = 'u'
        head = self.positions[0]
        self.positions.appendleft((head[0] - 1, head[1]))
        self.positions.pop()

    def moveSnakeDown(self):
        self.direction = 'd'
        head = self.positions[0]
        self.positions.appendleft((head[0] + 1, head[1]))
        self.positions.pop()
    
    def runSnake(self):
        if self.direction == 'u':
            self.moveSnakeUp()
        elif self.direction == 'd':
            self.moveSnakeDown()
        elif self.direction == 'l':
            self.moveSnakeLeft()
        else:
            self.moveSnakeRight()

    def checkBodyCollision(self) -> bool:
        head = self.positions[0]
        if head in list(self.positions)[1:]:
            return True
        return False

class Board:
    rows = 15
    cols = 55
    line_up = "\033[A"
    col1 = "\033[1G"

    def __init__(self, snake : Snake):
        self.snake = snake
        self.initializeSnake()
        self.food_position = None
        self.last_food_position = None
        self.generateFood()
    
    def generateFood(self):
        while True:
            i = random.randint(1, Board.rows - 2)
            j = random.randint(1, Board.cols - 2)
            pos = (i, j)
            if pos not in self.snake.positions:
                self.food_position = pos
                break

    
    def initializeSnake(self):
        self.snake.positions.append((Board.rows // 2, Board.cols // 2))
    
    def checkFoodEaten(self):
        if self.snake.positions[0] == self.food_position:
            self.last_food_position = self.food_position
            self.generateFood()

    def resetCursor(self) -> None:
        sys.stdout.write(Board.line_up * Board.rows + Board.col1)
    

    def showGrid(self) -> bool:
        flag = True
        for i in range(Board.rows):
            for j in range(Board.cols):
                if i == 0 or i == Board.rows - 1 or j == 0 or j == Board.cols - 1:
                    if self.snake.positions[0] == (i, j):
                        flag = False
                    print("#", end="")
                elif (i, j) in self.snake.positions:
                    print("0", end="")
                elif (i, j) == self.food_position:
                    print("$", end="")
                else:
                    print(" ", end="")
            print("")
        return flag and not self.snake.checkBodyCollision()



def hideCursor():
    sys.stdout.write("\033[?25l")

def showCursor():
    sys.stdout.write("\033[?25h")

def clearTerminal():
    if os.name == "nt": # For Windows
        os.system("cls")
    else: # For Linux and Mac
        os.system("clear")

def main():
    # Clear the terminal
    clearTerminal()
    # Hide the cursor
    hideCursor()
    snake = Snake()
    board = Board(snake)
    print("")
    board.showGrid()
    direction = None
    try:
        while True:
            board.snake.iters += 1
            if keyboard.is_pressed('k'):
                print("Thank You!")
                break
            elif keyboard.is_pressed('w'):
                if board.snake.direction != 'd':
                    direction = 'u'
            elif keyboard.is_pressed('s'):
                if board.snake.direction != 'u':
                    direction = 'd'
            elif keyboard.is_pressed('a'):
                if board.snake.direction != 'r':
                    direction = 'l'
            elif keyboard.is_pressed('d'):
                if board.snake.direction != 'l':
                    direction = 'r'
            if board.snake.iters == board.snake.velocity:
                if direction:
                    board.snake.direction = direction
                board.snake.iters = 0
                last_tail = board.snake.positions[-1]
                board.snake.runSnake()
                if board.last_food_position and board.last_food_position == last_tail:
                    board.last_food_position = None
                    board.snake.positions.append(last_tail)
            board.checkFoodEaten()
            board.resetCursor()
            if not board.showGrid():
                print("Game Over!")
                print(f"your Score: {len(board.snake.positions)}")
                break
            
    except:
        pass
    finally:
        showCursor()

if __name__ == "__main__":
    main()