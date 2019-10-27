from tkinter import *
from tkinter import ttk as tk
import Die
from tkinter import *
from tkinter import ttk as tk


class DieView:
    def __init__(self, master, value=None):
        if value is None:
            value = 6
        self.image = PhotoImage(file="Die" + str(value) + ".png")
        self.selected = IntVar()
        self.view = tk.Checkbutton(master, image=self.image, variable=self.selected)

    def update_value(self, value):
        self.image = PhotoImage(file="Die" + str(value) + ".png")
        self.view.configure(image=self.image)


class DiceView:
    def __init__(self, master, number_of_dice, roll_fun):
        self.dice = []
        for die_index in range(number_of_dice):
            self.dice.append(DieView(master))
            self.dice[-1].view.pack()
        self.btn_roll = tk.Button(master, text="Roll Dice", command=roll_fun)
        self.btn_roll.pack()


class DiceController:
    def __init__(self, tk_master):
        self.dice = Die.Dice(5)
        self.dice_view = DiceView(tk_master, 5, self.roll_dice)

    def roll_dice(self):
        die_index = 0
        for die_view in self.dice_view.dice:
            if die_view.selected.get():
                self.dice.get_die(die_index).roll()
                die_view.update_value(self.dice.get_die(die_index).value)
            die_index += 1


Yahtzee = Tk()
dice_game = DiceController(Yahtzee)
Yahtzee.mainloop()

