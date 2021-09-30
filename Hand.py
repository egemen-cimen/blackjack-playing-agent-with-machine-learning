import Settings
import logging

log = logging.getLogger(__name__)

VERBOSE = Settings.VERBOSE
DEBUG = Settings.DEBUG


class Hand(object):

    def __init__(self, bet):
        self.cards = []
        self.bet = bet
        self.state = 0  # state of bust, stand, hit

    def dealt_card(self, card):
        self.cards.append(card)

    def is_blackjack(self, is_split):
        if self.calculate_hand() == 21 and not is_split and len(self.cards) == 2:
            return True
        else:
            return False

    def calculate_hand(self):

        hand_value = 0
        ace_count = 0

        # add values of cards
        log.debug(f'self.cards is {self.cards}')

        for i in self.cards:

            if i == 11:
                ace_count += 1

            hand_value += i

            # remove if goes over
            while hand_value > 21 and ace_count > 0:
                hand_value -= 10
                ace_count -= 1

        return hand_value

    def is_total_hard(self):

        hand_value = 0
        ace_count = 0

        for i in self.cards:

            if i == 11:
                ace_count += 1

            hand_value += i

            # remove if goes over
            while hand_value > 21 and ace_count > 0:
                hand_value -= 10
                ace_count -= 1

        if ace_count > 0:
            return False  # there is an ace that counts as 11
        else:
            return True  # all aces (if any) count as 1

    def calculate_hand_no_ace(self):  # calculates hand except aces. aces are ignored
        hand_value = 0

        for i in self.cards:

            if i != 11:
                hand_value += i

        return hand_value

    def double_hand(self):

        self.bet = int(2 * self.bet)

        log.info(f'Hand double from {self.bet / 2} to {self.bet}')
