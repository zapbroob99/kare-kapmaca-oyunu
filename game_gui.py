import tkinter as tk

class GameGUI:
    def __init__(self, pieces, row, col):
        self.pieces = pieces
        self.row = row
        self.col = col
        self.window = tk.Tk()
        self.window.title("Squares Game")
        self.canvas = tk.Canvas(self.window, width=600, height=600)
        self.canvas.pack()
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        cell_size = 600 // (self.row + 1)

        for i in range(self.row):
            for j in range(self.col):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                if self.pieces[i][j] == 0:
                    fill_color = "white"
                elif self.pieces[i][j] == "W":
                    fill_color = "white"
                elif self.pieces[i][j] == "B":
                    fill_color = "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black")
                if self.pieces[i][j] != 0:
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=self.pieces[i][j], fill="red")

    def update_board(self, pieces):
        self.pieces = pieces
        self.draw_board()

    def run(self):
        self.window.mainloop()
