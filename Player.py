import Settings
import Hand
import CardCounter
import logging

VERBOSE = Settings.VERBOSE
DEBUG = Settings.DEBUG

log = logging.getLogger(__name__)


class Player(object):
    def __init__(self, bankroll, player_id, total_card_count, strategy_name):
        self.hands = []  # Hand list
        self.initial_bankroll = bankroll
        self.bankroll = bankroll
        self.is_split = False
        self.is_split_aces = False
        self.delta_bankroll = 0
        self.player_id = player_id
        self.no_of_hands_played = 0
        self.card_counter = CardCounter.CardCounter(self.player_id, total_card_count, strategy_name)
        self.better_than_control_count = 0  # no of times player is better than control test
        self.total_bet_amount = 0

    # open new hand to play
    def open_hand(self, min_bet, max_bet):
        bet = self.card_counter.get_recommended_bet(min_bet, max_bet, self.bankroll)

        if bet < min_bet:
            log.fatal(f'WRONG bet amount')
            exit()
        elif bet > max_bet:
            log.fatal(f'WRONG bet amount')
            exit()

        opened_hand = Hand.Hand(bet)
        self.hands.append(opened_hand)

    def dealt_card(self, card, hand_index):
        self.hands[hand_index].dealt_card(card)

    def lost_hand(self, hand_index):
        bet = self.hands[hand_index].bet
        self.total_bet_amount += bet
        self.bankroll -= bet
        self.delta_bankroll -= bet

        log.info(f'Player has lost bet the bet of {bet}')
        log.info(f'Player\'s remaining bankroll is {self.bankroll}')
        log.info(f'Change in player\'s bankroll is {self.delta_bankroll}')

    def won_hand(self, hand_index):  # is_blackjack: means won a hand with a blackjack (21)
        bet = self.hands[hand_index].bet
        self.total_bet_amount += bet

        # blackjack winnings 1.5 for 3:2; 1.2 for 6:5
        if self.hands[hand_index].is_blackjack(self.is_split):
            self.bankroll += int(bet * 1.5)
            self.delta_bankroll += int(bet * 1.5)
        else:
            self.bankroll += bet
            self.delta_bankroll = bet

        log.info(f'Player has won bet the bet of {bet}')
        log.info(f'Player\'s remaining bankroll is {self.bankroll}')
        log.info(f'Change in player\'s bankroll is {self.delta_bankroll}')

    def push_hand(self, hand_index):  # its a draw
        bet = self.hands[hand_index].bet
        self.total_bet_amount += bet

        log.info(f'Player has received its bet of {bet} (push hand)')
        log.info(f'Player\'s remaining bankroll is {self.bankroll}')
        log.info(f'Change in player\'s bankroll is {self.delta_bankroll}')

    def play_hands(self, hand_index, dealer_hand):

        can_double = True  # if a hand has doubled it shouldn't call this method (rule: doubled hands stand)
        if len(self.hands[hand_index].cards) > 2:  # can't double with more than 2 cards
            can_double = False

        action = self.card_counter.play_strategy(self.hands[hand_index], self.is_split, dealer_hand, can_double)

        if action == 102 and not self.is_split:  # can split hand
            self.split_hand(hand_index)
            self.is_split = True

            if self.hands[hand_index].cards[0] == 11:  # if you split an ace
                self.is_split_aces = True

        elif action == 102 and self.is_split:
            log.critical('The player has split too much')
            return 1  # 1 is invalid. this shouldn't occur

        if action == 103:
            if not Settings.DOUBLE_AFTER_SPLIT:  # doubling after splitting is not allowed
                if self.is_split:
                    return 101  # HIT because cant double anymore

        return action

    def end_of_hand(self):  # return mean hand return
        self.is_split = False
        self.is_split_aces = False
        self.hands = []  # Hand list
        self.no_of_hands_played += 1

        log.info(f'Player\'s change in bankroll at the end of the hand is {self.delta_bankroll}')

        self.delta_bankroll = 0

        mean_hand_return = (self.bankroll - self.initial_bankroll) / self.no_of_hands_played

        return mean_hand_return  # hand means game (e.g. end of hand)

    def end_of_game(self):

        log.info('Game has ended zeroing counters, hands, etc.')

        self.card_counter.zero_counter()
        self.end_of_hand()  # call this before zeroing self.no_of_hands_played
        self.no_of_hands_played = 0  # call this after end_of_hands

    def split_hand(self, hand_index):

        card_0 = self.hands[hand_index].cards[0]
        card_1 = self.hands[hand_index].cards[1]
        bet = self.hands[hand_index].bet
        if card_0 == card_1:
            self.hands[hand_index] = Hand.Hand(bet)
            self.hands[hand_index].dealt_card(card_0)
            self.hands.append(Hand.Hand(bet))
            self.hands[len(self.hands) - 1].dealt_card(card_1)

        else:
            log.fatal(f'Can\'t split {card_0} and {card_1}')
            exit()

        if hand_index != 0:  # DEBUG
            # Already split once.
            log.fatal('Splitting multiple times is not allowed')

            hand_index = 0
            for hand in self.hands:
                log.fatal(f'Player {hand.cards}')
                hand_index += 1

            exit()
