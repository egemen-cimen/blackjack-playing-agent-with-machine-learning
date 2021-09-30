import Settings
import Strategy
import CountingSystems
import numpy as np
import math

VERBOSE = Settings.VERBOSE


class CardCounter(object):

    def __init__(self, player_id, total_cards_in_shoe, strategy_name):
        self.running_count = 0
        self.player_id = player_id
        self.strategy = Strategy.Strategy()
        self.strategy_name = strategy_name
        self.counting_rule = CountingSystems.get_system_counting_rules_by_name(self.strategy_name)
        self.total_cards_in_shoe = total_cards_in_shoe
        self.played_card_count = 0

        if self.counting_rule.size != 0:
            self.betting_level = np.amax(self.counting_rule)
        else:
            self.betting_level = 0

        self.true_count = 0
        self.is_ml = False
        self.generate_csv = False

        if self.strategy_name == Settings.COUNT_SYSTEM_TO_WATCH and Settings.GENERATE_COUNT_CSV:
            self.generate_csv = True
            self.count_list = []
            self.count_of_each_card = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            self.count_of_each_card_this_hand = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        if self.strategy_name == Settings.ML_MODEL_TO_UTILIZE and Settings.UTILIZE_ML_MODEL:
            self.ml_model = Settings.ml_model
            self.is_ml = True
            self.count_of_each_card = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            self.count_of_each_card_this_hand = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def calculate_true_count(self):

        # check this condition first because ml's betting level is 0. dont want to return 0
        if self.is_ml:
            # TODO check if the order of variables are correct for the model to predict
            # TODO NOW use & zero the ml count list after each calculation of true count

            # get prediction from model
            if Settings.PER_HAND:
                array = np.array([self.count_of_each_card_this_hand]) / self.total_cards_in_shoe
            else:
                array = np.array([self.count_of_each_card]) / self.total_cards_in_shoe

            array = array[:, None]
            y_one = self.ml_model.predict(array)

            # round the prediction and set as true count
            # self.true_count = int(round(y_one[0][0]))

            self.true_count = int(np.trunc(y_one[0][0]))  # truncate or round?

            return

        if self.betting_level == 0:
            self.true_count = 0
            return

        remaining_half_decks = (self.total_cards_in_shoe - self.played_card_count) / 26  # 26 is 52/2
        remaining_decks = math.floor(remaining_half_decks) / 2  # /2 to make half deck full again
        remaining_decks_with_betting_level = remaining_decks * self.betting_level

        if remaining_decks_with_betting_level < 0.5:
            remaining_decks_with_betting_level = 0.5  # prevent divide by 0 errors
        self.true_count = int(self.running_count / remaining_decks_with_betting_level)

    def zero_counter(self):
        self.running_count = 0
        self.true_count = 0
        self.played_card_count = 0

        if self.is_ml:
            self.count_of_each_card = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        if self.generate_csv:
            self.count_of_each_card = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            self.count_of_each_card_this_hand = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def count_card_values(self, card):
        self.played_card_count += 1

        # counting strategy changes with the strategy
        if self.counting_rule.size != 0:  # basic and machine learning don't need any so they are empty arrays.
            #  if size > 0 then array is not empty

            self.running_count += self.counting_rule[card - 2]  # e.g. card 2 is at index 0. e.g. card 11 is at index 9

        if self.generate_csv or self.is_ml:
            self.count_of_each_card[card - 2] += 1
            self.count_of_each_card_this_hand[card - 2] += 1

    def get_recommended_bet(self, min_bet, max_bet, bankroll):
        self.calculate_true_count()
        # player_advantage = (0.515 * self.true_count) - 0.540
        # bet_amount = max(player_advantage * bankroll, min_bet)

        if self.generate_csv:

            tmp = [None] * 22  # (10 for count of each card, 1 for shoe progress,
            #  1 for true count, 10 for per-hand-counts)
            tmp[10] = self.played_card_count / self.total_cards_in_shoe  # shoe progress (where we're in the shoe)
            tmp[11] = self.true_count

            for i in range(len(self.count_of_each_card)):
                tmp[i] = self.count_of_each_card[i] / self.total_cards_in_shoe  # normalize values

            # do the same for the other list
            for i in range(len(self.count_of_each_card_this_hand)):
                tmp[i+12] = self.count_of_each_card_this_hand[i] / self.total_cards_in_shoe  # normalize values

            self.count_list.append(tmp)  # append list of correct true count value to

        if self.generate_csv or self.is_ml:  # make sure the hand gets zeroed
            # Zero the count list for count_of_each_card_this_hand after getting the bet & writing
            for i in range(len(self.count_of_each_card_this_hand)):
                self.count_of_each_card_this_hand[i] = 0

        # assuming you have -½% return on a freshly shuffled deck
        # return improves by 1% for each +2 change in true count

        # true count -> advantage
        # 0 -> -0.5%
        # 1 ->  0.0%
        # 2 ->  0.5%
        # 3 ->  1.5%
        # 4 ->  2.0%

        #bet_amount = max((bankroll / 1000) * (self.true_count - 1/2), min_bet)
        ## bet_amount = max((self.true_count - 1) * 5 * (bankroll / 1000), min_bet) # test
        #bet_amount = int(round(bet_amount))

        player_calc_advantage = 0.005*self.true_count - 0.005
        bet_amount = max(int(round(player_calc_advantage * bankroll)), min_bet)

        #print(f'self.true_count:{self.true_count}')
        #print(f'bet:{min(bet_amount, max_bet)}')
        #print()

        return min(bet_amount, max_bet)

    def play_strategy(self, hand, is_split, dealer_hand,
                      can_double):  # take is_split bc we need it for split controlling once

        hand_value = hand.calculate_hand()

        # better player logic with card counter and basic strategy
        if hand_value <= 21:

            # get action from strategy
            action = self.strategy.play_strategy(hand, dealer_hand, can_double, is_split)
            # with the third argument for 'can_double : boolean' add boolean for can split??? maybe needed?

            hand.state = action

            if action == 102 and not is_split:

                if VERBOSE:
                    print('CardCounter: split')

                hand.state = 102  # 102 means SPLIT

            elif action == 105:
                assert False

            elif action == 103:
                if can_double:
                    hand.state = 103  # DOUBLE
                else:
                    assert False
                    hand.state = 101  # HIT

            elif action == 104:
                if can_double:
                    hand.state = 103  # DOUBLE
                else:
                    assert False
                    hand.state = 100  # STAND

            if VERBOSE:
                print('CardCounter: ', hand.state)

            return hand.state

        elif hand_value > 21:

            if VERBOSE:
                print('CardCounter: bust')

            hand.state = 99
            return hand.state  # 99 means bust

        else:

            print('CardCounter: wrong hand_value->', hand_value, '(exit)')
            exit()
