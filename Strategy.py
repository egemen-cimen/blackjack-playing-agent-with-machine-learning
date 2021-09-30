import Settings
import numpy as np
import csv

VERBOSE = Settings.VERBOSE
DEBUG = Settings.DEBUG


class Strategy(object):
    def __init__(self):

        # h (height) = dealer's up card
        # w (width) = your hand

        # csv legend:
        # s == STAND (enum: 100)
        # h == HIT (enum: 101)
        # d == DOUBLE if allowed else HIT (enum: 103)
        # ds == DOUBLE if allowed else STAND (enum: 104)
        # p == SPLIT (enum: 102)
        # ph == SPLIT if DOUBLE after SPLIT allowed / HIT if DOUBLE after SPLIT not allowed (enum: 105)

        # csv locations:
        # 0th column: indexes
        # 1-17th columns: hard totals 5 - 21
        # 18-26th columns: soft totals a2 - a10
        # 27-36th columns: pair splitting 2-2 - a-a

        # if cant double down then hit  # TODO not exactly right (DS is stand if cant double)

        w, h = 36, 10
        # Create a list containing h (height) lists, each of w (width) items, all set to 0
        basic_strategy = [[0 for x in range(w)] for y in range(h)]

        # get basic strategy from csv file
        with open('basic-strategy.csv', newline='') as csv_file:
            reader = csv.reader(csv_file, skipinitialspace=True, delimiter=',', quoting=csv.QUOTE_NONE)

            j = -1  # ignore first row
            for row in reader:
                i = 0

                if j != -1:
                    while i < w:
                        action = row[i + 1]  # ignore first entry

                        action_enum = 0
                        if action == 's':
                            action_enum = 100
                        elif action == 'h':
                            action_enum = 101
                        elif action == 'p':
                            action_enum = 102
                        elif action == 'd':
                            action_enum = 103
                        elif action == 'ds':
                            action_enum = 104
                        elif action == 'ph':
                            action_enum = 105

                        else:
                            print('Strategy: WRONG enum from csv!')
                            exit()

                        basic_strategy[j][i] = action_enum
                        i += 1

                # print(', '.join(row))

                j += 1
        # print(', '.join(row))

        self.basic_strategy = np.matrix(basic_strategy)

    def play_strategy(self, hand, dealer_hand, can_double, is_split):  # play strategy based on the hand

        # dealer_hand_value = dealer_hand.calculate_hand()
        hand_value = hand.calculate_hand()
        hand_value_no_ace = hand.calculate_hand_no_ace()
        is_total_hard = hand.is_total_hard()
        is_pair = False

        if VERBOSE:
            print('Strategy: dealer_hand.cards->', dealer_hand.cards)
            print('Strategy: player hand cards->', hand.cards)

        assert len(dealer_hand.cards) == 1

        if len(dealer_hand.cards) == 1:
            h = dealer_hand.cards[0] - 2  # e.g. dealer (up-card) value 2 is at index 0 (2-2=0).
            # e.g. dealer value a is at index 9 (11-2=9).
        else:  # this function is called at a wrong time  #TODO remove
            print('Strategy: >>>>>>>>>>>>This should not have happened')
            exit()

        if DEBUG:
            print('Strategy: ', hand.cards)

        card_0 = hand.cards[0]
        card_1 = hand.cards[1]

        if len(hand.cards) == 2:

            if card_0 == card_1:
                is_pair = True

                # TODO: check aces in this case
                w = card_0 + 24  # e.g. hand value 2 - 2 is at index 26 (2+24=26).
                # e.g. hand value aa is at index 35 (11+24=35).

            else:
                # copy of below code
                if is_total_hard:
                    w = hand_value - 5  # e.g. hand value 5 is at index 0 (5-5=0).
                    # e.g. hand value 21 is at index 16 (21-5=16).
                else:  # total is soft
                    w = hand_value_no_ace + 15  # hand_value_no_ace is the other card (there are two cards in hand)
                    # e.g. hand value w/o aces 2 is at index 17 (2+15=17).
                    # e.g. hand value w/o aces 9 is at index 24 (9+15=24).

        else:  # more than two cards in hand
            # copy of above code
            if is_total_hard:
                w = hand_value - 5  # e.g. hand value 5 is at index 0 (5-5=0).
                # # e.g. hand value 21 is at index 16 (21-5=16).
            else:  # total is soft
                w = hand_value_no_ace + 15  # e.g. hand value w/o aces 2 is at index 17 (2+15=17).
                #  e.g. hand value w/o aces 9 is at index 24 (9+15=24).

        if DEBUG:
            print('Strategy: is_split?', is_split, ', is_pair?', is_pair)

        if is_pair and is_split:  # if its a pair and is already split so cant split again
            # lookup the hand as a hard total
            if hand_value == 4:  # 2-2
                w = 0
            else:  # hand_value > 5
                w = hand_value - 5  # e.g. hand value 5 is at index 0 (5-5=0).

        if DEBUG:
            print('Strategy: h?', h, ', w?', w)

        if w < 0 or h < 0:  # TODO assert this and remove
            print('Strategy: w cant be smaller than 0', w)
            print('Strategy: h cant be smaller than 0', h)
            exit()

        action = self.basic_strategy[h, w]

        # check double after split rule
        if Settings.DOUBLE_AFTER_SPLIT and action == 105:
            return 102  # SPLIT
        elif not Settings.DOUBLE_AFTER_SPLIT and action == 105:
            return 101  # HIT

        # check if it can double
        if not can_double and action == 104:  # ds == DOUBLE if allowed else STAND (enum: 104)
            return 100  # STAND
        # if can double=> returns 104 so calling method will know to double (no need for that method to check condition)
        elif not can_double and action == 103:  # d == DOUBLE if allowed else HIT (enum: 103)
            return 101  # HIT
        # if can double=> returns 103 so calling method will know to double (no need for that method to check condition)

        return self.basic_strategy[h, w]
