import random as r


class Die:
    """
    This is a class for a 6 sided die that can be rolled

    Attributes:
        value (int): the value of the last roll
    """
    def __init__(self, value=None):
        if value is None:
            self._value = 0
            self.roll()
        else:
            if 1 <= value <= 6:
                self._value = value
            else:
                raise Exception('The value of a die must be between 1 and 6')

    def roll(self):
        """Rolls the die"""
        self._value = r.randrange(1, 7)

    def __str__(self):
        return "A die with value of " + str(self.value) + '\n'

    @property
    def value(self):
        return self._value

    def getvalue(self):
        return self._value

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return self.value + other

    def __int__(self):
        return self.value

    def __lt__(self, other):
        return self.value < other

    def __le__(self, other):
        return self.value <= other

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __ge__(self, other):
        return self.value >= other

    def __gt__(self, other):
        return self.value > other

    # def __long__(self):
    #     return self.value)

    def __float__(self):
        return float(self.value)

    def __oct__(self):
        return oct(self.value)

    def __hex__(self):
        return hex(self.value)

    def __complex__(self):
        return complex(self.value)

    def __neg__(self):
        return -self.value

    def __pos__(self):
        return self.value

    def __abs__(self):
        return abs(self.value)

    def __invert__(self):
        return ~self.value


def dice_roll_count(dice_list, value_to_count):
    return dice_list.count(value_to_count)

def check_yahtzee(dice_list):
    has_yahtzee = False
    for value in range(1,7):
        if dice_roll_count(dice_list, value) == 5:
            has_yahtzee = True
    return has_yahtzee


def check_full_house(dice_list):
    ones = dice_roll_count(dice_list, 1)
    twos = dice_roll_count(dice_list, 2)
    threes = dice_roll_count(dice_list, 3)
    fours = dice_roll_count(dice_list, 4)
    fives = dice_roll_count(dice_list, 5)
    sixes = dice_roll_count(dice_list, 6)
    if (ones == 2 or twos == 2 or threes == 2 or fours == 2 or fives == 2 or sixes == 2) and \
            (ones == 3 or twos == 3 or threes == 3 or fours == 3 or fives == 3 or sixes == 3):
        return True
    else:
        return False


def of_a_kind_size(dice_list):
    counts = [dice_roll_count(1, dice_list), dice_roll_count(2, dice_list), dice_roll_count(3, dice_list), dice_roll_count(4, dice_list), dice_roll_count(5), dice_list,
              dice_roll_count(6, dice_list)]
    return max(counts)


def straight_size(dice_list):
    values = []
    for die in dice_list:
        values.append(die.value)

    values.sort()
    values = list(set(values))
    straight_length = 1
    longest_straight = 1
    for die_index in range(1, len(values)):
        current_die = values[die_index]
        previous_die = values[die_index - 1]
        if current_die == previous_die + 1:
            straight_length += 1
            if straight_length > longest_straight:
                longest_straight = straight_length
        elif current_die == previous_die:
            straight_length = straight_length
        else:
            # Restart
            straight_length = 1

    return longest_straight

# Functions for score boxes

def aces_points(dice_list):
    return dice_roll_count(dice_list, 1) * 1


def twos_points(dice_list):
    return dice_roll_count(dice_list, 2) * 2


def threes_points(dice_list):
    return dice_roll_count(dice_list, 3) * 3


def fours_points(dice_list):
    return dice_roll_count(dice_list, 4) * 4


def fives_points(dice_list):
    return dice_roll_count(dice_list, 5) * 5


def sixes_points(dice_list):
    return dice_roll_count(dice_list, 6) * 6


def three_of_a_kind_points(dice_list):
    if of_a_kind_size(dice_list) >= 3:
        return sum(dice_list)
    else:
        return 0


def four_of_a_kind_points(dice_list):
    if of_a_kind_size(dice_list) >= 4:
        total = 0
        for die in dice_list:
            total += die.value
        return total
    else:
        return 0


def full_house_points(dice_list):
    if check_full_house(dice_list):
        return 25
    else:
        return 0


def small_straight_points(dice_list):
    if straight_size(dice_list) >= 4:
        return 30
    else:
        return 0


def large_straight_points(dice_list):
    if straight_size(dice_list) >= 5:
        return 40
    else:
        return 0


def yahtzee_points(dice_list):
    if of_a_kind_size(dice_list) >= 5:
        return 50
    else:
        return 0


def chance_points(dice_list):
    total = 0
    for die in dice_list:
        total += die.value
    return total


assign_function_lookup = {
    'Aces': aces_points,
    'Twos': twos_points,
    'Threes': threes_points,
    'Fours': fours_points,
    'Fives': fives_points,
    'Sixes': sixes_points,
    '3 of a Kind': three_of_a_kind_points,
    '4 of a Kind': four_of_a_kind_points,
    'Full House': full_house_points,
    'Small Straight': small_straight_points,
    'Large Straight': large_straight_points,
    'Yahtzee': yahtzee_points,
    'Chance': chance_points
}


class ScoreBox:

    def __init__(self, box_type):
        self._points = 0
        self._assigned = False
        self._name = box_type
        self._calculate_points = assign_function_lookup[box_type]

    @property
    def name(self):
        return self._name

    def getname(self):
        return self._name

    @property
    def points(self):
        return self._points

    def getpoints(self):
        return self._points

    @property
    def assigned(self):
        return self._assigned

    def getassigned(self):
        return self._assigned

    def assign_points(self, dice):
        if not self.assigned:
            self._assigned = True
            self._points = self._calculate_points(dice)

    def __str__(self):
        return self._name + ': ' + str(self._points)


class ScoreCard:
    def __init__(self):
        self._aces = ScoreBox('Aces')
        self._twos = ScoreBox('Twos')
        self._threes = ScoreBox('Threes')
        self._fours = ScoreBox('Fours')
        self._fives = ScoreBox('Fives')
        self._sixes = ScoreBox('Sixes')
        self._upperSum = 0
        self._upperTotal = 0
        self._bonus = 0
        self._threeOfAKind = ScoreBox('3 of a Kind')
        self._fourOfAKind = ScoreBox('4 of a Kind')
        self._fullHouse = ScoreBox('Full House')
        self._smallStraight = ScoreBox('Small Straight')
        self._largeStraight = ScoreBox('Large Straight')
        self._yahtzee = ScoreBox('Yahtzee')
        self._chance = ScoreBox('Chance')
        self._lowerTotal = 0
        self._grandTotal = 0
        self._upper_section = [self._aces, self._twos, self._threes, self._fours, self._fives, self._sixes]
        self._lower_section = [self._threeOfAKind, self._fourOfAKind, self._fullHouse, self._smallStraight, self._largeStraight, self._yahtzee, self._chance]
        self._boxes = [self._aces, self._twos, self._threes, self._fours, self._fives, self._sixes, self._threeOfAKind, self._fourOfAKind, self._fullHouse, self._smallStraight, self._largeStraight, self._yahtzee, self._chance]

    def print_points(self, box_index):
        return str(self._boxes[box_index])

    def update_points(self):

        #Calculate Upper Section
        total = 0
        for box in self._upper_section:
            total += box.points
        self._upperSum = total

        if total >= 63:
            self._bonus = 35
            total += 35
        self._upperTotal = total

        # Calculate Lower Section
        total = 0
        for box in self._lower_section:
            total += box.points

        self._lowerTotal = total

        #Total Points
        self._grandTotal = self._upperTotal + self._lowerTotal

    @property
    def total_points(self):
        return self._grandTotal

    @property
    def upper_total_points(self):
        return self._upperTotal

    @property
    def bonus_points(self):
        return self._bonus

    @property
    def lower_total_points(self):
        return self._lowerTotal

    def get_box(self, box_name):
        for box in self._boxes:
            if box.name == box_name:
                return box

    def assign_roll(self, box_name, dice):
        self.get_box(box_name).assign_points(dice)
        self.update_points()

    def get_box_points(self, box_name):
        return self.get_box(box_name).points

    def get_box_assigned(self, box_name):
        return self.get_box(box_name).assigned

    def __lt__(self, other):
        return self._grandTotal < other

    def __le__(self, other):
        return self._grandTotal <= other

    def __eq__(self, other):
        return self._grandTotal == other

    def __ne__(self, other):
        return self._grandTotal != other

    def __ge__(self, other):
        return self._grandTotal >= other

    def __gt__(self, other):
        return self._grandTotal > other


class YahtzeeModel:
    def __init__(self):
        self._turn = 13
        self._rolls_remaining = 3
        self._dice = []
        self._score_card = ScoreCard()
        self._selected_dice = [False for selected_index in range(5)]
        self._assigned_roll = False
        for die_index in range(5):
            self._dice.append(Die())

    @property
    def rolls_remaining(self):
        """Get the number of rolls remaining for the current turn"""
        return self._rolls_remaining

    @property
    def turn(self):
        """Return the number of turns remaining in the game"""
        return self._turn

    def roll_dice(self):
        """Roll the dice that have been selected"""
        if self._rolls_remaining > 0:
            for die in self._dice:
                die.roll()
        self._rolls_remaining = self._rolls_remaining - 1
        return [die.value for die in self._dice]

    def assign_roll(self, box_name):
        if self._assigned_roll:
            return self._score_card.get_box_points(box_name)
        else:
            self._score_card.assign_roll(box_name, self._dice)
            self._assigned_roll = True
            return self._score_card.get_box_points(box_name)

    def next_turn(self):
        """Proceed to next turn"""
        if self._turn > 0:
            self._turn -= 1
            self._rolls_remaining = 3
            self._assigned_roll = False
        else:
            self.end_game()

    def end_game(self):
        """End the game and calculate winner"""
        pass

    def toggle_die_for_roll(self, die_index, selected):
        """Select or un-select dice to be rolled"""
        self._selected_dice[die_index] = selected
        # return [self._selected_dice[selected_index] for selected_index in self._selected_dice]
