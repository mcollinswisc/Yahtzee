from DieModel import *
from ScoreCardModel import *


class YahtzeeModel:
    def __init__(self):
        self._players = []
        self._game_started = False
        self._game_complete = False
        self._current_player = -1
        self._turn = 0 # begin game calls next turn which at current player = 0 subtracts this down to 13
        self._rolls_remaining = 0
        self._dice = []
        self._winner = None
        self._current_score_card = None
        self._assigned_roll = False
        for die_index in range(5):
            self._dice.append(Die())

    @property
    def game_over(self):
        return self._game_complete

    @property
    def current_player(self):
        if len(self._players) > 0:
            return self._players[self._current_player]
        else:
            return None

    @property
    def score_card(self):
        return self._current_score_card

    @property
    def rolls_remaining(self):
        """Get the number of rolls remaining for the current turn"""
        return self._rolls_remaining

    @property
    def turn(self):
        """Return the number of turns remaining in the game"""
        return self._turn

    def start_game(self):
        self._game_complete = False
        if len(self._players) > 0:
            self._turn = len(self._players) * 13
            self._current_player = self.calculate_player_index()
            self.setup_turn()
            self._game_started = True
        else:
            raise Exception('There must be at least one player to start the game.')

    def calculate_player_index(self):
        return self._turn % len(self._players)

    def add_player(self, player):
        self._players.append(player)

    def remove_player(self, player_index):
        return self._players.pop(player_index)

    def get_dice(self):
        return [die.value for die in self._dice]

    def roll_dice(self):
        """Roll the dice that have been selected"""
        if self._rolls_remaining > 0 and not self._assigned_roll:
            for die_index, die in enumerate(self._dice):
                if die.selected:
                    die.roll()
            self._rolls_remaining = self._rolls_remaining - 1
        return self.get_dice()

    def assign_roll(self, box_name):
        # only assign roll if the box doesn't already have value and the roll hasn't already been assigned this turn
        if self._assigned_roll or self._current_score_card.get_box_assigned(box_name) or not self._game_started:
            return self._current_score_card.get_box_points(box_name)
        else:
            self._current_score_card.assign_roll(box_name, self._dice)
            self._assigned_roll = True
            return self._current_score_card.get_box_points(box_name)

    def setup_turn(self):
        #get player variables
        self._current_score_card = self._players[self.calculate_player_index()].score_card

        # Setup and roll dice
        self._rolls_remaining = 3
        self._assigned_roll = False
        for die in self._dice:
            die.selected = True
        self.roll_dice()

    def next_turn(self):
        """Proceed to next turn"""
        if self._game_started and not self._game_complete and self._assigned_roll == True:
            self._turn = self._turn - 1
            print(self._turn)
            if self._turn > 0:
                self.setup_turn()
            else:
                self.end_game()

    def end_game(self):
        """End the game and calculate winner"""
        self._game_started = False
        self._game_complete = True


