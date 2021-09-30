import Settings
import Hand

VERBOSE = Settings.VERBOSE


class Dealer(object):

    def __init__(self):
        self.hand = Hand.Hand(0)

    def dealt_card(self, card):
        self.hand.dealt_card(card)

    def play_hand(self):
        hand_value = self.hand.calculate_hand()

        if hand_value < 17:  # dealer stands on soft 17
            # hit
            if VERBOSE:
                print('Dealer: hit')

            return 101  # 101 means hit

        elif hand_value > 21:
            return 99  # 99 means bust

        else:

            if VERBOSE:
                print('Dealer: stand')

            return 100  # 100 means stand

    def end_of_hand(self):
        self.hand = Hand.Hand(0)
