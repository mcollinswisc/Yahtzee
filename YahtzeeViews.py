from tkinter import *
from tkinter import ttk as tk
import Die
from tkinter import *
from tkinter import ttk as tk


class DieView:
    """
    This is a class to display a single die that can be selected

    Attributes:
        selected (bool): Whether or not the die is selected
        last_roll (int): The number diplayed on the die

    """
    def __init__(self, master, initial_roll=None):
        self._last_roll = 6
        if initial_roll is None:
            self._last_roll = 6
        self._image = PhotoImage(file="Die" + str(self._last_roll) + ".png")
        self._selected = IntVar()
        self.view = tk.Checkbutton(master, image=self._image, variable=self.selected)

    @property
    def selected(self):
        """Get or set whether the die is selected. Toggles the checkbox control"""
        return self._selected

    @selected.setter
    def selected(self, is_selected):
        self._selected.set(is_selected)

    @property
    def last_roll(self):
        """Get or set the number displayed on the die"""
        return self._last_roll

    @last_roll.setter
    def last_roll(self, value):
        if 1 <= value <= 6:
            self._last_roll = value
            self._image = PhotoImage(file="Die" + str(value) + ".png")
            self.view.configure(image=self._image)
        else:
            raise Exception('Value of die view must be between 1 and 6')


class DiceView:
    def __init__(self, master, number_of_dice, initial_rolls, roll_fun):
        self.dice = []
        self._can_roll = True
        self._rolls_remaining = initial_rolls
        for die_index in range(number_of_dice):
            self.dice.append(DieView(master))
            self.dice[-1].view.pack()
        self._rollsRemainingTxt = StringVar()
        self._rollsRemainingTxt.set('Rolls Remaining: ' + str(initial_rolls))
        self._txt_rolls_remaining = tk.Label(master, textvariable=self._rollsRemainingTxt)
        self._txt_rolls_remaining.pack()
        self.btn_roll = tk.Button(master, text="Roll Dice", command=roll_fun)
        self.btn_roll.pack()

    @property
    def rolls_remaining(self):
        return self._rolls_remaining

    @rolls_remaining.setter
    def rolls_remaining(self, value):
        self._rolls_remaining = value
        self._rollsRemainingTxt.set('Rolls Remaining: ' + str(self._rolls_remaining))

    @property
    def can_roll(self):
        return self._can_roll

    @can_roll.setter
    def can_roll(self, enabled):
        self._can_roll = enabled
        if enabled:
            self.btn_roll.config(state=NORMAL)
        else:
            self.btn_roll.config(state=DISABLED)


score_box_view_types = {'Aces', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes', '3 of a Kind', '4 of a Kind', 'Full House', 'Small Straight', 'Large Straight', 'Yahtzee', 'Chance'}


class ScoreBoxView:
    """
    This is a class for an individual score box on a Yahtzee score sheet

    Attributes:
        name (str): The name of the score box
        frame (tk.frame): The tk frame object containing the score box UI elements
        points (int): The number of points in the scorebox
        enabled (bool): Whether or not the score box can be selected
    """

    def __init__(self, master, name, can_assign: bool, assignment_var: StringVar):
        """
        The constructor for ScoreBoxView

        Parameters:
            master (tk object): The tk master object to place the score box UI into
            name (str): The name of the score box, also displays as a text label next to the box on the UI. Should be one of the following values:
            'Aces', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes', '3 of a Kind', '4 of a Kind', 'Full House', 'Small Straight', 'Large Straight', 'Yahtzee', 'Chance'
            can_assign (bool): Whether a dice roll can be assigned to the score box (For Example: the grand total score box should have False passed here)
            assignment_var (tk StringVar): The variable where the selected score box will be stored. Passed from the larger score card view object.
        """
        self._frame = tk.Frame(master)
        self._name = name
        self._points_view = tk.Entry(self.frame, width=3, state='disabled')
        if can_assign:
            self._selector = tk.Radiobutton(self.frame, variable=assignment_var, text=name, width=11, value=name)
        else:
            self._selector = tk.Label(self.frame, text=name, width=13)

        self._selector.pack(side=LEFT, expand=True)
        self._points_view.pack(side=RIGHT, expand=True)

    @property
    def points(self):
        """Get or set the points displayed in the score box"""
        return self._points_view.get()

    @points.setter
    def points(self, value):
        self._points_view.configure(state=NORMAL)
        self._points_view.delete(0, END)
        self._points_view.insert(0, value)
        self._points_view.configure(state=DISABLED)

    @property
    def enabled(self):
        """Enabled or disable the score box from being able to be selected for assigning a dice roll"""
        return self._selector.state()

    @enabled.setter
    def enabled(self, enable):
        if enable:
            self._selector.configure(state=NORMAL)
        else:
            self._selector.configure(state=DISABLED)

    @property
    def frame(self):
        """Get the tk frame containing all the score box UI elements"""
        return self._frame

    @property
    def name(self):
        """Get the name of the score box"""
        return self._name


class ScoreCardView:
    """
    This is a class for an the UI of a Yahtzee score sheet

    Attributes:
        selection (str): The name of the score box that is selected
    """
    def __init__(self, master):
        """
        The constructor for ScoreCardView

        Parameters:
            master (tk object): The tk master object to place the score card UI into
            assign_fun (function): The function that is called when the assign roll button is clicked on the UI
        """
        box_setup_instructions = {
            'Aces': {'Can Assign': True},
            'Twos': {'Can Assign': True},
            'Threes': {'Can Assign': True},
            'Fours': {'Can Assign': True},
            'Fives': {'Can Assign': True},
            'Sixes': {'Can Assign': True},
            'Bonus': {'Can Assign': False},
            'Upper Total': {'Can Assign': False},
            '3 of a Kind': {'Can Assign': True},
            '4 of a Kind': {'Can Assign': True},
            'Full House': {'Can Assign': True},
            'Small Straight': {'Can Assign': True},
            'Large Straight': {'Can Assign': True},
            'Yahtzee': {'Can Assign': True},
            'Chance': {'Can Assign': True},
            'Lower Total': {'Can Assign': False},
            'Grand Total': {'Can Assign': False}
        }

        # Setup the main frame and variables
        self.mainFrame = tk.Frame(master)
        self.mainFrame.pack()
        self.assign_selection = StringVar()

        # Setup the score box UIs
        self.scoreBoxes = {}
        for box_setup in box_setup_instructions:
            assignable = box_setup_instructions[box_setup]['Can Assign']
            self.scoreBoxes[box_setup] = ScoreBoxView(self.mainFrame, box_setup, assignable, self.assign_selection)
        rw = 0
        for scoreBox in self.scoreBoxes:
            self.scoreBoxes[scoreBox].frame.grid(row=rw, column=0, sticky=NSEW)
            #self.scoreBoxes[scoreBox].frame.pack(side=TOP, expand=True)
            rw += 1

        # Setup button for assigning roll

    @property
    def selection(self):
        """Get or set the selected score box on the score card.  Pass an empty string to deselect all boxes."""
        return self.assign_selection.get()

    @selection.setter
    def selection(self, box_name):
        self.assign_selection.set(box_name)

    def assign_points(self, box_name, points):
        """
        Update the number of points displayed in a score box on the score card UI

        Parameters:
            box_name (tk str): The name of the box to update the points in
            points (bool): the number of points to place in the score box UI
        """
        self.scoreBoxes[box_name].points = points

    def box_enabled(self, box_name, enabled):
        """
        Update whether or not a score box on the score card UI can be selected

        Parameters:
            box_name (tk str): The name of the box to disable/enable
            enabled (bool): Whether or not the box can be selected
        """
        self.scoreBoxes[box_name].enabled = enabled