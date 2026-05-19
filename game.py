import tkinter as tk
import random

SIZE = 4
CELL_SIZE = 100
WIDTH = SIZE * CELL_SIZE
HEIGHT = SIZE * CELL_SIZE

# Tile colors
COLORS = {
    0: "#cdc1b4",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e"
}

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game With Score")

        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0

        # Score Label
        self.score_label = tk.Label(
            root,
            text="Score: 0",
            font=("Arial", 20, "bold"),
            bg="black",
            fg="white",
            pady=10
        )
        self.score_label.pack(fill="x")

        # Game Canvas
        self.canvas = tk.Canvas(
            root,
            width=WIDTH,
            height=HEIGHT,
            bg="#bbada0"
        )
        self.canvas.pack()

        # Buttons Frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        # Restart Button
        restart_btn = tk.Button(
            button_frame,
            text="Restart",
            font=("Arial", 14, "bold"),
            command=self.restart_game,
            bg="green",
            fg="white",
            width=10
        )
        restart_btn.grid(row=0, column=0, padx=10)

        # Exit Button
        exit_btn = tk.Button(
            button_frame,
            text="Exit",
            font=("Arial", 14, "bold"),
            command=root.destroy,
            bg="red",
            fg="white",
            width=10
        )
        exit_btn.grid(row=0, column=1, padx=10)

        self.add_tile()
        self.add_tile()

        self.draw_board()

        self.root.bind("<Key>", self.key_press)
        
        # FILE HANDLING

def save_high_score(self):
    try:
        file = open("highscore.txt", "w")
        file.write(str(self.high_score))
        file.close()

    except Exception as e:
        print("File Save Error:", e)


def load_high_score(self):
    try:
        file = open("highscore.txt", "r")
        self.high_score = int(file.read())
        file.close()

    except:
        self.high_score = 0

    def restart_game(self):
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0

        self.add_tile()
        self.add_tile()

        self.update_score()
        self.draw_board()

    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")

    def add_tile(self):
        empty = []

        for i in range(SIZE):
            for j in range(SIZE):
                if self.board[i][j] == 0:
                    empty.append((i, j))

        if empty:
            i, j = random.choice(empty)
            self.board[i][j] = random.choice([2, 4])

    def draw_board(self):
        self.canvas.delete("all")

        for i in range(SIZE):
            for j in range(SIZE):
                value = self.board[i][j]

                x1 = j * CELL_SIZE
                y1 = i * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                color = COLORS.get(value, "#3c3a32")

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="#bbada0",
                    width=5
                )

                if value != 0:
                    self.canvas.create_text(
                        x1 + CELL_SIZE / 2,
                        y1 + CELL_SIZE / 2,
                        text=str(value),
                        font=("Arial", 24, "bold"),
                        fill="black"
                    )

    def compress(self, row):
        new_row = [num for num in row if num != 0]
        new_row += [0] * (SIZE - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(SIZE - 1):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                row[i + 1] = 0

                # Add score
                self.score += row[i]

        return row

    def move_left(self):
        changed = False
        new_board = []

        for row in self.board:
            compressed = self.compress(row)
            merged = self.merge(compressed)
            final = self.compress(merged)

            if final != row:
                changed = True

            new_board.append(final)

        self.board = new_board
        return changed

    def reverse(self, board):
        return [row[::-1] for row in board]

    def transpose(self, board):
        return [list(row) for row in zip(*board)]

    def move_right(self):
        self.board = self.reverse(self.board)
        changed = self.move_left()
        self.board = self.reverse(self.board)
        return changed

    def move_up(self):
        self.board = self.transpose(self.board)
        changed = self.move_left()
        self.board = self.transpose(self.board)
        return changed

    def move_down(self):
        self.board = self.transpose(self.board)
        changed = self.move_right()
        self.board = self.transpose(self.board)
        return changed

  # exception handling
    def key_press(self, event):

        try:
            key = event.keysym
            moved = False

            if key == "Left":
                moved = self.move_left()

            elif key == "Right":
                moved = self.move_right()

            elif key == "Up":
                moved = self.move_up()

            elif key == "Down":
                moved = self.move_down()

            if moved:
                self.add_tile()
                self.update_score()
                self.draw_board()

        except Exception as e:
            print("Error:", e)

root = tk.Tk()
game = Game2048(root)
root.mainloop()
