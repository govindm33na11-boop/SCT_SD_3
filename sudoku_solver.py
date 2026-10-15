import tkinter as tk
from tkinter import messagebox

class SudokuSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SCT_SD_3 - Sudoku Solver")
        self.root.geometry("620x720")
        self.root.config(bg="#f4f5f7")
        self.root.minsize(540, 640)

        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        header_frame = tk.Frame(root, bg="#f4f5f7")
        header_frame.pack(pady=(20, 10), fill="x")

        tk.Label(header_frame, text="🧩 Sudoku Solver Engine", font=("Helvetica", 18, "bold"), bg="#f4f5f7", fg="#1f2937").pack()
        tk.Label(header_frame, text="Enter a puzzle or load a sample, then hit Solve", font=("Helvetica", 10), bg="#f4f5f7", fg="#6b7280").pack(pady=(2, 0))

        card = tk.Frame(root, bg="#ffffff", bd=1, relief="solid")
        card.config(highlightbackground="#e5e7eb", highlightthickness=1)
        card.pack(padx=25, fill="both", expand=True, pady=(5, 15))

        card.rowconfigure(0, weight=1)
        card.columnconfigure(0, weight=1)

        grid_container = tk.Frame(card, bg="#1f2937", bd=2, relief="solid")
        grid_container.pack(padx=25, pady=20, expand=True)

        self.cells = [[None for _ in range(9)] for _ in range(9)]
        
        for r in range(9):
            for c in range(9):
                top_b = 3 if r % 3 == 0 else 1
                left_b = 3 if c % 3 == 0 else 1
                bot_b = 3 if r == 8 else 0
                right_b = 3 if c == 8 else 0

                cell_frame = tk.Frame(grid_container, bg="#1f2937", bd=0)
                cell_frame.grid(row=r, column=r, padx=(left_b, right_b), pady=(top_b, bot_b))

                ent = tk.Entry(
                    grid_container, width=2, font=("Helvetica", 16, "bold"),
                    justify="center", bg="#ffffff", fg="#111827", bd=0, relief="flat"
                )
                ent.grid(row=r, column=c, padx=left_b, pady=top_b, ipady=6, ipadx=4)
                self.cells[r][c] = ent

        btn_bar = tk.Frame(card, bg="#ffffff")
        btn_bar.pack(padx=25, fill="x", pady=(0, 20))

        self.btn_solve = tk.Button(btn_bar, text="Solve Puzzle", font=("Helvetica", 11, "bold"), bg="#059669", fg="#ffffff", activebackground="#047857", activeforeground="white", relief="flat", cursor="hand2", command=self.solve_sudoku)
        self.btn_solve.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 8))

        self.btn_sample = tk.Button(btn_bar, text="Load Sample", font=("Helvetica", 11, "bold"), bg="#4f46e5", fg="#ffffff", activebackground="#4338ca", activeforeground="white", relief="flat", cursor="hand2", command=self.load_sample)
        self.btn_sample.pack(side="left", fill="x", expand=True, ipady=10, padx=(4, 4))

        self.btn_clear = tk.Button(btn_bar, text="Clear Grid", font=("Helvetica", 11, "bold"), bg="#ef4444", fg="#ffffff", activebackground="#dc2626", activeforeground="white", relief="flat", cursor="hand2", command=self.clear_grid)
        self.btn_clear.pack(side="right", fill="x", expand=True, ipady=10, padx=(8, 0))

    def get_board(self):
        board = []
        for r in range(9):
            row = []
            for c in range(9):
                val = self.cells[r][c].get().strip()
                if val == "":
                    row.append(0)
                elif val.isdigit() and 1 <= int(val) <= 9:
                    row.append(int(val))
                else:
                    return None
            board.append(row)
        return board

    def set_board(self, board):
        for r in range(9):
            for c in range(9):
                self.cells[r][c].delete(0, tk.END)
                if board[r][c] != 0:
                    self.cells[r][c].insert(0, str(board[r][c]))
                    self.cells[r][c].config(fg="#059669")

    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_r, start_c = 3 * (row // 3), 3 * (col // 3)
        for r in range(3):
            for c in range(3):
                if board[start_r + r][start_c + c] == num:
                    return False
        return True

    def solve(self, board):
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, r, c, num):
                            board[r][c] = num
                            if self.solve(board):
                                return True
                            board[r][c] = 0
                    return False
        return True

    def solve_sudoku(self):
        board = self.get_board()
        if board is None:
            messagebox.showerror("Invalid Input", "Please enter only numbers between 1 and 9.")
            return

        if self.solve(board):
            self.set_board(board)
            messagebox.showinfo("Success", "Sudoku puzzle solved successfully!")
        else:
            messagebox.showerror("Unsolvable", "No valid solution exists for this configuration.")

    def load_sample(self):
        sample = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        for r in range(9):
            for c in range(9):
                self.cells[r][c].delete(0, tk.END)
                self.cells[r][c].config(fg="#111827")
                if sample[r][c] != 0:
                    self.cells[r][c].insert(0, str(sample[r][c]))

    def clear_grid(self):
        for r in range(9):
            for c in range(9):
                self.cells[r][c].delete(0, tk.END)
                self.cells[r][c].config(fg="#111827")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverApp(root)
    root.mainloop()