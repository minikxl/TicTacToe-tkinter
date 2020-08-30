import tkinter as tk
from tkinter import messagebox


# ====================================
# ---------Klasa przycisków-----------
# ====================================

class Field(tk.Label):

    def __init__(self, parent, main):
        tk.Label.__init__(self, parent, justify="center", relief="raised")
        self.main = main
        self.x_img = tk.PhotoImage(file="assets\X1.png")
        self.o_img = tk.PhotoImage(file="assets\O1.png")
        self.blank_img = tk.PhotoImage(file=r"assets\blank.png")
        self.config(image=self.blank_img)
        self.marked = ''

        self.bind('<Button-1>', self.check)

    def check(self, event):
        if not self.marked:
            if self.main.turn == self.main.p1:
                self.main.whoLabel.config(text="Turn: {}".format(self.main.p2.get()))
                self.make_o()
                self.main.turn = self.main.p2
            else:
                self.main.whoLabel.config(text="Turn: {}".format(self.main.p1.get()))
                self.make_x()
                self.main.turn = self.main.p1

            self.main.check_win()

    def make_x(self):
        self.config(image=self.x_img)
        self.marked = 'x'

    def make_o(self):
        self.config(image=self.o_img)
        self.marked = 'o'


# ====================================
# ---------Klasa Główna --------------
# ====================================
class Main:
    def __init__(self, parent):
        self.root = parent
        self.p1 = tk.StringVar()
        self.p2 = tk.StringVar()
        self.turn = self.p1

        self.fg = '#fff'
        self.bg = '#000'
        self.yellow = '#fdbf00'

        self.create_widgets()

    # ====================================
    # --------- Rysowanie okna -----------
    # ====================================
    def create_widgets(self):

        # first frame
        self.mainFrame = tk.Frame(self.root, bg=self.bg)
        tk.Label(self.mainFrame, font=('Serreria Sobria', 50), text="Tic-Tac-Toe", fg=self.yellow, bg=self.bg).pack()

        self.subFrame = tk.Frame(self.mainFrame, bg=self.bg)
        tk.Label(self.subFrame, bg=self.bg, fg=self.fg, font=("", 10), text="O player name: ").grid()
        tk.Entry(self.subFrame, font=('', 10), textvariable=self.p1).grid(row=0, column=1)
        tk.Label(self.subFrame, bg=self.bg, fg=self.fg, font=("", 10), text="X player name: ").grid(row=1, column=0)
        self.last_entry = tk.Entry(self.subFrame, font=('', 10), textvariable=self.p2)
        self.last_entry.grid(row=1, column=1)
        self.subFrame.pack(padx=10, pady=22)

        self.buttonFrame = tk.Frame(self.mainFrame, bg=self.bg)
        self.start_game_button = tk.Button(self.buttonFrame, width=26, relief="groove", bg=self.yellow, fg=self.bg,
                                           font=("Serreria Sobria", 20), bd=0, text="PLAY!")
        self.start_game_button.pack()
        self.start_game_button.bind('<Button-1>', self.start)
        self.last_entry.bind('<Return>', self.start)

        self.buttonFrame.pack()
        self.mainFrame.pack()

        # self.create_menu()

    def create_menu(self):
        self.show_all = tk.BooleanVar()
        self.menu = tk.Menu(root)
        self.root.config(menu=self.menu)

        self.gamemenu = tk.Menu(self.menu)

        self.gamemenu.add_command(label="GAMEMODE", state="disabled")
        self.gamemenu.add_separator()

        self.gamemenu.add_checkbutton(label="vs Player")
        self.gamemenu.add_checkbutton(label="vs AI")
        self.gamemenu.add_cascade(label="Newbie", menu=self.gamemenu)
        # self.gamemenu.add_cascade(label="Pro", menu=self.gamemenu)
        # self.gamemenu.add_separator()

        self.gamemenu.add_command(label="Exit", command=root.quit)

        self.menu.add_cascade(label="Game Menu", menu=self.gamemenu)
        #
        self.multiplayermenu = tk.Menu(self.menubar, tearoff=0)
        self.multiplayermenu.add_command(label="Host")
        self.multiplayermenu.add_command(label="Join")
        self.menu.add_cascade(label="Multiplayer", menu=self.menu)




    # ====================================
    # --------- Rozpoczęcie gry ----------
    # ====================================
    def start(self, *args):

        if self.p1.get() == self.p2.get():
            messagebox.showwarning("Warring", "The names cannot be this same")
        else:
            self.subFrame.forget()
            self.buttonFrame.forget()

            ###INFO TABLE###
            self.win = 0
            self.infoTable = tk.Frame(self.mainFrame)
            self.whoLabel = tk.Label(self.infoTable, text="Turn: {}".format(self.turn.get()),
                                     font=("Serreria Sobria", 20), bg=self.bg, fg=self.fg)
            self.whoLabel.pack()
            self.infoTable.pack()

            # board frame
            self.board = tk.Frame(self.mainFrame, bg=self.bg)

            # buttons
            self.fields = []
            for y in range(3):
                for x in range(3):
                    field = Field(self.board, self)
                    field.grid(row=y, column=x, padx=1, pady=1)
                    self.fields.append(field)

            self.board.pack(pady=20)

    # ====================================
    # ------- Sprawdź kto wygrał ---------
    # ====================================
    def check_win(self):
        print("----------------------")
        print("{:1} | {:1} | {:1}\n"
              "{:1} | {:1} | {:1}\n"
              "{:1} | {:1} | {:1}".format(self.fields[0].marked, self.fields[1].marked, self.fields[2].marked,
                                          self.fields[3].marked, self.fields[4].marked, self.fields[5].marked,
                                          self.fields[6].marked, self.fields[7].marked, self.fields[8].marked))

        for a, b, c in [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 4, 8], [2, 4, 6], [0, 3, 6], [1, 4, 7], [2, 5, 8]]:
            if self.fields[a].marked == self.fields[b].marked == self.fields[c].marked == 'o':
                self.finish('o')  # sending Title, and content to msgbox
                return 1

            if self.fields[a].marked == self.fields[b].marked == self.fields[c].marked == 'x':
                self.finish('x')
                return 2

        # Draw
        checked = 0
        for field in self.fields:
            if field.marked != '':
                checked += 1
        if checked == 9:
            self.finish('DRAW')
            return 3

    def finish(self, who):
        self.win = 1
        if who == 'o':
            msgout = messagebox.showinfo("CIRCLE WIN!", "The winner is {}".format(self.p1.get()))
        elif who == 'x':
            msgout = messagebox.showinfo("CROSS WIN!", "The winner is {}".format(self.p2.get()))
        elif who == 'DRAW':
            messagebox.showinfo("DRAW", "NOBODY WIN!")

        self.infoTable.forget()
        self.board.forget()
        self.subFrame.pack(padx=10, pady=22)
        self.buttonFrame.pack()


# =================================
# ------------ START---------------
# =================================

if __name__ == '__main__':
    root = tk.Tk()  # Tworzenie okna
    root.resizable(False, False)  # Ustawianie rozszerzania X Y
    root.title('TicTacToe')
    root.iconbitmap('fav.ico')

    Main(root)  # Wywołanie klasy main

root.mainloop()
