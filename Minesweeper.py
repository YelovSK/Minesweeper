#Meno: Patrik Hampel

import tkinter as tk
from tkinter import messagebox
from random import randint
import time
from PIL import Image, ImageTk


class Plocha:
    def __init__(self, w, h):
        self.c = Program.c = Square.c = Explosion.c = tk.Canvas(
            width=w, height=h, bg="#bcbcbc"
        )
        self.c.pack()


class Square:
    c = None

    def __init__(self, x, y, rev, what, obr):
        self.x, self.y = x * 30 + 30, y * 30 + 85
        self.i_x, self.i_y = x, y
        self.rev = rev
        self.what = what
        self.id = self.c.create_image(self.x, self.y, image=obr)

    def change(self, obr):
        self.c.itemconfig(self.id, image=obr)


class Explosion:
    c = None

    def __init__(self, x, y, arr):
        self.id = self.c.create_image(x * 30 + 30, y * 30 + 85)
        self.arr = arr
        self.img = 0
        self.animate()

    def animate(self):
        self.c.itemconfig(self.id, image=self.arr[self.img])
        self.img += 1
        if self.img < len(self.arr):
            self.c.after(120, self.animate)


class Button:
    c = None

    def __init__(self, **param):
        self.id = tk.Button(**param, font="arial 12 bold", bg="#c8c8c8")

    def place(self, x_p, y_p):
        self.id.place(x=x_p, y=y_p)


class Program:
    c = None

    def __init__(self):
        self.settings()
        self.vars()
        self.width, self.height = (
            30 * self.x_size + 30,
            30 * self.y_size + 120,
        )
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        self.root.iconbitmap("imgs/icon.ico")
        self.root.resizable(0, 0)
        Plocha(self.width, self.height)
        self.main_fun()
        self.root.mainloop()

    def vars(self):
        self.width, self.height = (
            30 * self.x_size + 30,
            30 * self.y_size + 120,
        )
        self.time = 0
        self.add = 0
        self.generated = False
        self.do_timer = False
        self.index_x = self.index_y = None
        self.over = False

    def main_fun(self):
        self.binds()
        self.menu_bar()
        self.draw_basic()
        self.images()
        self.place_buttons()
        self.empty_field()

    def menu_bar(self):
        menu = tk.Menu(self.root,)
        self.root.config(menu=menu)

        subMenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=subMenu)
        
        subMenu.add_command(label="Save", command=self.save)
        subMenu.add_command(label="Load", command=self.load)
        subMenu.add_command(label="Exit", command=self.exit)

        subMenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Edit", menu=subMenu)
        subMenu.add_command(
            label="Change number of mines", command=self.pref
        )
        subMenu.add_command(
            label="Reset high scores", command=self.reset_hs
        )
        subMenu.add_command(
            label="Reset everything", command=self.default
        )

        subMenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="View", menu=subMenu)
        subMenu.add_command(label="Show high scores", command=self.show_hs)

    def timer(self):
        if self.do_timer:
            self.time = round(time.time() - self.start) + self.add
            self.c.itemconfig(self.time_text, text=f"{self.time:03}")
            self.c.after(1000, self.timer)

    def exit(self):
        if tk.messagebox.askyesno(
            "Exit", "Do you really want to quit Minesweeper?"
        ):
            self.root.destroy()

    def default(self):
        if tk.messagebox.askyesno(
            "Reset", "Do you want to reset high scores and mine values?"
        ):
            with open("txt/diffs.txt", "w") as file:
                file.write("10 10 10 \n")
                file.write("15 13 40 \n")
                file.write("30 16 99")
            with open("txt/highscores.txt", "w") as file:
                file.write("TBD TBD TBD")
            self.diffs = [[10, 10, 10], [15, 13, 40], [30, 16, 99]]
            self.change_diff(self.diff)

    def pref(self):
        self.prev_diffs = self.diffs
        self.prefs = tk.Toplevel()
        self.prefs.title("Preferences")
        self.prefs.iconbitmap("imgs/icon.ico")
        self.prefs.geometry("278x252")
        self.prefs.resizable(0, 0)
        self.pc = tk.Canvas(self.prefs, width=278, height=252)
        self.pc.pack()
        self.pc.create_image(0, 0, image=self.imgs["prefs2"], anchor="nw")

        self.sliders = {}
        vals = ((3, 80), (30, 160), (50, 400))
        self.outputs = [
            self.diffs[0][2],
            self.diffs[1][2],
            self.diffs[2][2],
        ]
        prev_outputs = list(self.outputs)

        self.sliders[0] = tk.Scale(
            self.prefs,
            orient="horizontal",
            bd=0,
            from_=vals[0][0],
            to=vals[0][1],
            command=lambda x: self.update(0),
        )

        self.sliders[1] = tk.Scale(
            self.prefs,
            orient="horizontal",
            bd=0,
            from_=vals[1][0],
            to=vals[1][1],
            command=lambda x: self.update(1),
        )

        self.sliders[2] = tk.Scale(
            self.prefs,
            orient="horizontal",
            bd=0,
            from_=vals[2][0],
            to=vals[2][1],
            command=lambda x: self.update(2),
        )

        for i in range(3):
            self.sliders[i].set(self.outputs[i])
            self.sliders[i].pack()
        y_coor = (60, 105, 145)

        for i in range(3):
            self.sliders[i].place(x=115, y=y_coor[i])
        self.save = tk.Button(
            self.prefs,
            text="Save",
            width=7,
            bd=3,
            command=lambda: self.change_prefs(self.outputs, prev_outputs),
        )
        self.save.place(x=70, y=215)
        self.cancel = tk.Button(
            self.prefs,
            text="Cancel",
            width=7,
            bd=3,
            command=lambda: self.prefs.destroy(),
        )
        self.cancel.place(x=150, y=215)

        self.prefs.mainloop()

    def change_prefs(self, vals, prev_vals):
        changed = [False, False, False]
        diff = ["beginner", "intermediate", "expert"]
        string = ""
        for i in range(3):
            if vals[i] != prev_vals[i]:
                changed[i] = True
                string += f"{diff[i]}, "
        string = string[:-2]
        if string == "":
            ask = "Do you want to keep above values?"
        else:
            ask = f"High scores for {string} will be reset, proceed?"
        
        if tk.messagebox.askyesno(
            "Warning", ask
        ):
            for i in range(3):
                self.diffs[i][2] = vals[i]
            with open("txt/diffs.txt", "w") as file:
                for j in range(3):
                    for i in range(3):
                        file.write(f"{self.diffs[j][i]} ")
                    file.write("\n")
            with open("txt/highscores.txt", "r") as file:
                scores = file.read().split()
            with open("txt/highscores.txt", "w") as file:
                for i in range(3):
                    if changed[i]:
                        file.write("TBD ")
                    else:
                        file.write(f"{scores[i]} ")
            self.prefs.destroy()

    def update(self, i):
        self.outputs[i] = self.sliders[i].get()

    def reset_hs(self):
        if tk.messagebox.askyesno(
            "Reset", "Do you want to reset high scores?"
        ):
            with open("txt/highscores.txt", "w") as file:
                file.write("TBD TBD TBD")

    def save(self):
        if self.over or not self.do_timer:
            tk.messagebox.showerror("Error", "Cannot save")
        elif tk.messagebox.askyesno(
            "Save", "Do you want to save the state of the current game?"
        ):
            with open("txt/saved_game.txt", "w") as file:
                file.write(f"{self.diff} {self.time} \n")
                for riadok in self.squares:
                    for inst in riadok:
                        file.write(f"{inst.what} ")
                    file.write("\n")
                file.write("\n")
                for riadok in self.squares:
                    for inst in riadok:
                        file.write(f"{inst.rev} ")
                    file.write("\n")

    def load(self):
        try:
            if tk.messagebox.askyesno(
                "Load game", "Do you want to load the last saved game?"
            ):
                with open("txt/saved_game.txt") as file:
                    riadok = file.readline().split()
                    self.diff = int(riadok[0])
                    self.change_diff(self.diff, True)
                    self.add = int(riadok[1])
                    self.do_timer = True
                    self.start = time.time()
                    self.timer()
                    self.generated = True
                    self.c.itemconfig(
                        self.time_text, text=f"{self.time:03}"
                    )
                    for i, riadok in enumerate(file):
                        if riadok == "\n":
                            break
                        for j, prvok in enumerate(riadok.split()):
                            inst = self.squares[i][j]
                            try:
                                inst.what = int(prvok)
                            except:
                                inst.what = prvok
                    for i, riadok in enumerate(file):
                        if riadok == "\n":
                            break
                        for j, prvok in enumerate(riadok.split()):
                            inst = self.squares[i][j]
                            if prvok == "False":
                                self.change_square(inst, False)
                            elif prvok == "True":
                                self.change_square(inst, True)
                            elif prvok == "flagged":
                                self.change_square(inst, "flagged")
            self.count_unrevealed()
        except FileNotFoundError:
            tk.messagebox.showerror("Error", "No saved game")

    def place_buttons(self):
        self.beginner = Button(
            text="Beginner", width=7, bd=3, command=lambda: self.ask_diff(0)
        )
        self.beginner.place(13, self.height - 39)

        self.intermediate = Button(
            text="Intermediate",
            width=10,
            bd=3,
            command=lambda: self.ask_diff(1),
        )
        self.intermediate.place(self.width // 2 - 53, self.height - 39)

        self.expert = Button(
            text="Expert", width=7, bd=3, command=lambda: self.ask_diff(2)
        )
        self.expert.place(self.width - 93, self.height - 39)

    def binds(self):
        self.c.bind_all("<ButtonPress-1>", self.push_down)
        self.c.bind_all("<ButtonRelease-1>", self.check)
        self.c.bind_all("<Button-3>", self.mark)

    def settings(self):
        self.diffs = [[], [], []]
        try:
            with open("txt/diffs.txt") as file:
                for i, line in enumerate(file):
                    self.diffs[i] = line.split()
            for x, line in enumerate(self.diffs):
                for y, prv in enumerate(line):
                    self.diffs[x][y] = int(prv)
        except:
            with open("txt/diffs.txt", "w") as file:
                file.write("10 10 10 \n")
                file.write("15 13 40 \n")
                file.write("30 16 99")
            self.diffs = [[10, 10, 10], [15, 13, 40], [30, 16, 99]]
        self.diff = 0
        self.x_size = self.diffs[self.diff][0]
        self.y_size = self.diffs[self.diff][1]
        self.mines = self.diffs[self.diff][2]

    def ask_diff(self, num):
        if tk.messagebox.askyesno(
            "Change difficulty", "Do you really want to restart?"
        ):
            self.change_diff(num)

    def change_diff(self, diff, timer=False):
        self.diff = diff
        self.x_size = self.diffs[self.diff][0]
        self.y_size = self.diffs[self.diff][1]
        self.mines = self.diffs[self.diff][2]
        self.change_size()
        self.empty_field()
        self.c.itemconfig(self.smiley, image=self.imgs["s1"])

    def images(self):
        self.imgs = {}
        for i, name in enumerate(
            (
                "mine",
                "button",
                "button_p",
                "flag",
                "exploded",
                "mineF",
                "s1",
                "s2",
                "s3",
                "s4",
                "s5",
                "prefs2",
            )
        ):
            self.imgs[name] = tk.PhotoImage(file=f"imgs/{name}.png")
        self.cut_anim()

    def cut_anim(self):
        self.explosion = []
        img = Image.open("imgs/explosion.png")
        width, height = img.width // 6, img.height
        for i in range(0, img.width, width):
            self.explosion.append(
                ImageTk.PhotoImage(img.crop((i, 0, i + width, height)))
            )

    def change_size(self):
        self.vars()
        self.root.geometry(f"{self.width}x{self.height+4}")
        self.c.delete("all")
        self.draw_basic()
        self.c.config(width=self.width, height=self.height)
        self.beginner.place(13, self.height - 39)
        self.intermediate.place(self.width // 2 - 53, self.height - 39)
        self.expert.place(self.width - 93, self.height - 39)

    def empty_field(self):
        self.smiley = self.c.create_image(
            self.width // 2, 35, image=self.imgs["s1"]
        )
        self.squares = []

        for i in range(self.x_size):
            self.squares.append([])
            for j in range(self.y_size):
                self.squares[i].append(
                    Square(i, j, False, None, self.imgs["button"])
                )

    def field(self, k_x, k_y):
        self.generated = True
        placed_num = 0
        self.do_timer = True
        self.start = time.time()
        self.timer()

        while placed_num != self.mines:
            x = randint(0, self.x_size - 1)
            y = randint(0, self.y_size - 1)
            placed = False
            while placed == False:
                inst = self.squares[x][y]
                if inst.what != "m" and (
                    x < k_x - 1 or x > k_x + 1 or y > k_y + 1 or y < k_y - 1
                ):
                    inst.what = "m"
                    placed = True
                    placed_num += 1
                else:
                    x = randint(0, self.x_size - 1)
                    y = randint(0, self.y_size - 1)
        for i, riadok in enumerate(self.squares):
            for j, inst in enumerate(riadok):
                neigh = 0
                inst = self.squares[i][j]
                if inst.what != "m":
                    for k in range(i - 1, i + 2):
                        for p in range(j - 1, j + 2):
                            if (
                                k < 0
                                or p < 0
                                or k > self.x_size - 1
                                or p > self.y_size - 1
                                or (i == k and j == p)
                            ):
                                pass
                            else:
                                if self.squares[k][p].what == "m":
                                    neigh += 1
                    inst.what = neigh

    def draw_basic(self):
        self.c.create_rectangle(
            11,
            66,
            self.width - 11,
            self.height - 46,
            fill="#646464",
            outline="",
        )
        self.c.create_rectangle(
            11, 10, self.width - 11, 60, fill="#646464", outline=""
        )
        self.c.create_rectangle(
            14, 13, self.width - 14, 57, fill="#333", outline=""
        )
        self.time_text = self.c.create_text(
            self.width - 25,
            35,
            text=f"{self.time:03}",
            font="helvetica 25",
            fill="red",
            anchor="e",
        )
        self.mine_text = self.c.create_text(
            25,
            35,
            text=f"{self.mines:03}",
            font="helvetica 25",
            fill="red",
            anchor="w",
        )

    def reveal(self, won):
        self.over = True

        for riadok in self.squares:
            for inst in riadok:
                if inst.what == "m" and not won:
                    if inst.rev == "flagged":
                        inst.change(self.imgs["mineF"])
                        Explosion(inst.i_x, inst.i_y, self.explosion)
                    else:
                        inst.change(self.imgs["mine"])
                        Explosion(inst.i_x, inst.i_y, self.explosion)
                elif inst.what == "m":
                    inst.change(self.imgs["flag"])
                elif won:
                    inst.change(self.imgs["button_p"])
                    self.surrounding(inst, inst.what)

    def check(self, event):
        self.c.itemconfig(self.smiley, image=self.imgs["s1"])

        if (
            event.y > 16
            and event.y < 53
            and event.x > self.width // 2 - 16
            and event.x < self.width // 2 + 16
        ):
            self.change_diff(self.diff)
        elif not self.over and self.index_x != None:
            k_x, k_y = self.check_boundaries(event.x, event.y)
            inst = self.squares[k_x][k_y]
            inst_prev = self.squares[self.index_x][self.index_y]
            if (
                self.index_x != k_x or self.index_y != k_y
            ):
                if inst_prev.rev == "half":
                    self.change_square(inst_prev, False)
            elif inst.rev != "flagged":
                if not self.generated:
                    self.field(k_x, k_y)
                if inst.what == "m":
                    self.reveal(False)
                    self.do_timer = False
                    inst.change(self.imgs["exploded"])
                    self.c.itemconfig(self.smiley, image=self.imgs["s2"])
                else:
                    self.change_square(inst, True)
                if inst.what == 0:
                    self.floodfill(k_x, k_y)
        self.check_win()

    def check_win(self):
        if self.count_unrevealed() and not self.over:
            self.do_timer = False
            self.c.itemconfig(self.smiley, image=self.imgs["s4"])
            self.reveal(True)
            self.over = True
            self.update_hs()

    def update_hs(self):
        try:
            with open("txt/highscores.txt") as file:
                scores = file.read().split()
                new_scores = scores
                if scores[self.diff] == "TBD" or self.time < int(
                    scores[self.diff]
                ):
                    scores[self.diff] = str(self.time)
                    new_scores = scores
                    messagebox.showinfo(":)", "You beat your high score!")
            with open("txt/highscores.txt", "w") as file:
                for score in new_scores:
                    file.write(f"{score} ")
        except:
            with open("txt/highscores.txt", "w") as file:
                new_scores = ["TBD", "TBD", "TBD"]
                new_scores[self.diff] = str(self.time)
                for score in new_scores:
                    file.write(f"{score} ")

    def show_hs(self):
        try:
            with open("txt/highscores.txt") as file:
                scores = file.read().split()
                for i in range(len(scores)):
                    if scores[i] != "TBD":
                        scores[i] = scores[i] + "s"
                messagebox.showinfo(
                    "High scores",
                    f"Beginner: {scores[0]} \nIntermediate: {scores[1]} \nExpert: {scores[2]}",
                )
        except:
            messagebox.showerror("Error", "No high scores")

    def push_down(self, event):
        if (
            event.y > 16
            and event.y < 53
            and event.x > self.width // 2 - 16
            and event.x < self.width // 2 + 16
        ):
            self.c.itemconfig(self.smiley, image=self.imgs["s5"])
        elif (
            type(self.check_boundaries(event.x, event.y)[0]) == bool
            or self.over
        ):
            pass
        else:
            self.index_x, self.index_y = self.check_boundaries(
                event.x, event.y
            )
            inst = self.squares[self.index_x][self.index_y]
            if not inst.rev:
                self.c.itemconfig(self.smiley, image=self.imgs["s3"])
                self.change_square(inst, "half")

    def mark(self, event):
        if (
            type(self.check_boundaries(event.x, event.y)[0]) == bool
            or self.over
        ):
            pass
        elif not self.over:
            index_x, index_y = self.check_boundaries(event.x, event.y)
            inst = self.squares[index_x][index_y]
            if inst.rev == "flagged":
                self.change_square(inst, False)
            elif not inst.rev:
                self.change_square(inst, "flagged")
        self.check_win()

    def check_boundaries(self, x, y):
        if y < 70 or y >= self.height - 52:
            return False, False
        elif x <= 14 or x >= self.width - 15:
            return False, False
        else:
            return (x - 15) // 30, (y - 70) // 30

    def surrounding(self, inst, num):
        cols = (
            "blue",
            "green",
            "red",
            "navy",
            "brown4",
            "skyblue1",
            "black",
            "gray",
        )
        if num != 0:
            self.c.create_text(
                inst.x,
                inst.y,
                fill=cols[num - 1],
                text=num,
                font="verdana 15 bold",
            )

    def floodfill(self, x, y):
        for k in range(x - 1, x + 2):
            for p in range(y - 1, y + 2):
                if (
                    k < 0
                    or p < 0
                    or k > self.x_size - 1
                    or p > self.y_size - 1
                    or (x == k and y == p)
                ):
                    pass
                else:
                    inst = self.squares[k][p]
                    if inst.what == 0 and inst.rev == False:
                        self.change_square(inst, True)
                        self.floodfill(k, p)
                    elif inst.what != "m" and inst.rev != "flagged":
                        self.change_square(inst, True)

    def count_unrevealed(self):
        flag = unrev = flag_total = 0

        for i, riadok in enumerate(self.squares):
            for j, inst in enumerate(riadok):
                if not inst.rev:
                    unrev += 1
                if inst.what == "m" and inst.rev == "flagged":
                    flag += 1
                    flag_total += 1
                elif inst.rev == "flagged":
                    flag_total += 1
        self.c.itemconfig(
            self.mine_text, text=f"{self.mines-flag_total:03}"
        )
        if (flag == self.mines or flag + unrev == self.mines) and flag == flag_total:
            return True
        return False

    def change_square(self, inst, rev):
        inst.rev = rev
        if rev == False:
            inst.change(self.imgs["button"])
        elif rev == "half":
            inst.change(self.imgs["button_p"])
        elif rev == "flagged":
            if self.over and inst.what == "m":
                inst.change(self.imgs["mineF"])
            else:
                inst.change(self.imgs["flag"])
        else:
            if inst.what == "m":
                inst.change(self.imgs["mine"])
            else:
                inst.change(self.imgs["button_p"])
                if inst.what != 0:
                    self.surrounding(inst, inst.what)


Program()
