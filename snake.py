import keyboard
import sys
from collections import deque
import os
import random


class Snake:
    def __init__(self):
        self.length = 1
        self.positions = deque()
        self.velocity = 150  # In Iterations count
        self.direction = "r"  # Default direction
        self.iters = 0

    def moveSnakeRight(self) -> None:
        self.direction = "r"
        head = self.positions[0]
        self.positions.appendleft((head[0], head[1] + 1))
        self.positions.pop()

    def moveSnakeLeft(self) -> None:
        self.direction = "l"
        head = self.positions[0]
        self.positions.appendleft((head[0], head[1] - 1))
        self.positions.pop()

    def moveSnakeUp(self) -> None:
        self.direction = "u"
        head = self.positions[0]
        self.positions.appendleft((head[0] - 1, head[1]))
        self.positions.pop()

    def moveSnakeDown(self) -> None:
        self.direction = "d"
        head = self.positions[0]
        self.positions.appendleft((head[0] + 1, head[1]))
        self.positions.pop()

    def runSnake(self) -> None:
        if self.direction == "u":
            self.moveSnakeUp()
        elif self.direction == "d":
            self.moveSnakeDown()
        elif self.direction == "l":
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

    def __init__(self, snake: Snake):
        self.snake: Snake = snake
        self.initializeSnake()
        self.food_position: tuple | None = None
        self.last_food_position: deque = deque()
        self.generateFood()
        self.highscore: int = 0
        self.score: int = 0

    def generateFood(self) -> None:
        while True:
            i = random.randint(1, Board.rows - 2)
            j = random.randint(1, Board.cols - 2)
            pos = (i, j)
            if pos not in self.snake.positions:
                self.food_position = pos
                break

    def initializeSnake(self) -> None:
        self.snake.positions.append((Board.rows // 2, Board.cols // 2))

    def checkFoodEaten(self) -> None:
        if self.snake.positions[0] == self.food_position:
            self.last_food_position.append(self.food_position)
            self.generateFood()
            self.score += 1

    def resetCursor(self) -> None:
        sys.stdout.write(Board.line_up * Board.rows + Board.col1)

    def showGrid(self) -> bool:
        flag = True
        for i in range(Board.rows):
            for j in range(Board.cols + 20):
                if i == 0 or i == Board.rows - 1 or j == 0 or j == Board.cols - 1:
                    if self.snake.positions[0] == (i, j):
                        flag = False
                    print("#", end="")
                elif (i, j) in self.snake.positions:
                    print("0", end="")
                elif (i, j) == self.food_position:
                    print("$", end="")
                elif j < Board.cols:
                    print(" ", end="")
                elif j > Board.cols:
                    if i == 2 and j == Board.cols + 3:
                        print(f" High Score: {self.highscore}", end="")
                    elif i == 4 and j == Board.cols + 3:
                        print(f" Your Score: {self.score}", end="")
                    else:
                        print(" ", end="")
            print("")
        return flag and not self.snake.checkBodyCollision()


def hideCursor() -> None:
    sys.stdout.write("\033[?25l")


def showCursor() -> None:
    sys.stdout.write("\033[?25h")


def clearTerminal() -> None:
    if os.name == "nt":  # For Windows
        os.system("cls")
    else:  # For Linux and Mac
        os.system("clear")


def initializeGame() -> Board:
    # Clear the terminal
    clearTerminal()
    # Hide the cursor
    hideCursor()
    snake = Snake()
    board = Board(snake)
    high_score = loadHighScore()
    if board.score > high_score:
        updateHighScore(board.score)
    board.highscore = high_score
    print("")
    board.showGrid()
    return board


def loadHighScore() -> int:
    high_score = 0
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            try:
                high_score = int(f.read().strip())
            except:
                high_score = 0
    return high_score


def updateHighScore(new_score: int) -> None:
    try:
        high_score = loadHighScore()
        if new_score > high_score:
            with open("highscore.txt", "w") as f:
                f.write(str(new_score))
    except:
        pass


def quitGame() -> None:
    showCursor()
    clearTerminal()
    print("Thank You for playing!")
    sys.exit(0)


def main():
    board = initializeGame()
    direction = None
    try:
        while True:
            board.snake.iters += 1
            if keyboard.is_pressed("k"):
                user_input = input("Press y to continue or any other key to exit: ")
                if user_input and user_input.lower()[-1] == "y":
                    clearTerminal()
                else:
                    updateHighScore(board.score)
                    print("Thank You!")
                    break
            elif keyboard.is_pressed("w"):
                if board.snake.direction != "d":
                    direction = "u"
            elif keyboard.is_pressed("s"):
                if board.snake.direction != "u":
                    direction = "d"
            elif keyboard.is_pressed("a"):
                if board.snake.direction != "r":
                    direction = "l"
            elif keyboard.is_pressed("d"):
                if board.snake.direction != "l":
                    direction = "r"
            if board.snake.iters == board.snake.velocity:
                if direction:
                    board.snake.direction = direction
                board.snake.iters = 0
                last_tail = board.snake.positions[-1]
                board.snake.runSnake()
                if (
                    board.last_food_position
                    and board.last_food_position[0] == last_tail
                ):
                    board.last_food_position.popleft()
                    board.snake.positions.append(last_tail)
            board.checkFoodEaten()
            board.resetCursor()
            if not board.showGrid():
                updateHighScore(board.score)
                print("Game Over!")
                user_input = input("Press y to continue or any other key to exit: ")
                if user_input and user_input.lower()[-1] == "y":
                    board = initializeGame()
                    direction = None
                    continue
                else:
                    # Clear input buffer
                    keyboard.clear_all_hotkeys()
                    keyboard.unhook_all()
                    break

    except:
        pass
    finally:
        quitGame()


if __name__ == "__main__":
    main()
