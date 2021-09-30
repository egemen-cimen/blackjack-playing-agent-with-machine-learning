from logging import Logger

import Player
import Dealer
import TestResults
import GameDataDump
# import Settings
import time
# import random
import numpy as np
import logging

log: Logger = logging.getLogger(__name__)


class Game(object):

    def __init__(self, seed, no_of_decks, no_of_players, no_of_games_to_be_played, no_of_hands_limit,
                 player_start_bankroll, min_bet, max_bet, systems):
        self.shuffled_cards = np.array([])
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.no_of_decks = no_of_decks
        self.no_of_players = no_of_players
        self.player_start_bankroll = player_start_bankroll
        self.no_of_games_to_be_played = no_of_games_to_be_played
        self.no_of_hands_limit = no_of_hands_limit
        self.dealer = Dealer.Dealer()
        self.players = []
        np.random.seed(seed)
        self.game_data_dump = []
        self.systems = systems

        # print(f'{no_of_decks}, {no_of_players}, {no_of_games_to_be_played},
        # {no_of_hands_limit}, {player_start_bankroll}, {min_bet}, {max_bet}')

        # initialize players
        for i in range(self.no_of_players):
            self.players.append(Player.Player(self.player_start_bankroll, i, 52 * self.no_of_decks, self.systems[i]))

    def start_game(self):

        no_of_games_played = 0
        no_of_hands_played = 0  # information purposes only
        start_time = time.time()
        total_percentage_of_cards_played = 0  # for information only. will divide by no of games played

        log.debug('Init started')

        # generate the deck (only one suit for now)
        one_deck = np.array([11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10])  # 11 is ace, 10's are 10 j q k

        # complete the one deck
        for i in range(2):   # make 4 copies of basic cards to get one deck (2^2 = 4)
            one_deck = np.append(one_deck, one_deck)

        self.shuffled_cards = np.copy(one_deck)

        # copy one deck to get desired number of decks
        for i in range(self.no_of_decks-1):
            self.shuffled_cards = np.append(self.shuffled_cards, one_deck)

        for no_of_games_played in range(1, self.no_of_games_to_be_played+1):
            # shuffle deck
            np.random.shuffle(self.shuffled_cards)

            total_card_count = self.shuffled_cards.size
            remaining_card_count = total_card_count

            log.info(f'Shuffled Cards:\n{self.shuffled_cards}')
            log.info(f'Remaining Card Count:\t{remaining_card_count}')
            log.info(f'Total Card Count:\t{total_card_count}')

            played_card_count = 0
            needs_reshuffle = False

            percentage_of_cards_played = 0
            while not needs_reshuffle:

                log.info(f'Will now deal cards and play')

                # deal all players one card
                for player in self.players:
                    player.open_hand(self.min_bet, self.max_bet)

                    # they only have one hand at the beginning of the hand
                    hand_index = 0

                    card = self.shuffled_cards.item(played_card_count)
                    played_card_count += 1
                    remaining_card_count -= 1
                    # give card to player
                    player.dealt_card(card, hand_index)

                    # card counting advertisement to all card counter(s)
                    for player_to_advertise in self.players:
                        player_to_advertise.card_counter.count_card_values(card)

                    log.info(f'Gave {card}\tto the player #{player.player_id} hand #{hand_index}. '
                             f'Hand is now {player.hands[hand_index].cards}')

                # deal card to the dealer
                card = self.shuffled_cards.item(played_card_count)
                played_card_count += 1
                remaining_card_count -= 1
                # give card to dealer
                self.dealer.dealt_card(card)

                # card counting advertisement to card counter(s)
                for player_to_advertise in self.players:
                    player_to_advertise.card_counter.count_card_values(card)

                log.info(f'Gave {card} to the dealer. Hand is now {self.dealer.hand.cards}')

                # deal all players one more card
                for player in self.players:
                    # players still have one hand
                    hand_index = 0

                    card = self.shuffled_cards.item(played_card_count)
                    played_card_count += 1
                    remaining_card_count -= 1
                    # give card to player
                    player.dealt_card(card, hand_index)

                    # card counting advertisement to card counter(s)
                    for player_to_advertise in self.players:
                        player_to_advertise.card_counter.count_card_values(card)

                    log.info(f'Gave {card}\tto the player #{player.player_id} hand #{hand_index}. '
                             f'Hand is now {player.hands[hand_index].cards}')

                # deal one more card to the dealer but don't show it yet
                dealer_second_card = self.shuffled_cards.item(played_card_count)

                log.info(f'Taken {dealer_second_card} for the dealer. Card is NOT advertised yet')

                played_card_count += 1
                remaining_card_count -= 1
                # don't advertise the card yet

                # allow players to play
                for player in self.players:
                    hand_index = 0
                    while hand_index < len(player.hands):

                        # repeat until player's hands stand or bust
                        while True:

                            hit_or_stand = player.hands[hand_index].state
                            # take the state player was in. player could be in STAND or BUST
                            # state so they wont need another card

                            # don't allow busted or stood down hands to play again. play other states here
                            if hit_or_stand != 100 and hit_or_stand != 99:
                                hit_or_stand = player.play_hands(hand_index, self.dealer.hand)
                            else:
                                break  # stop checking

                            if hit_or_stand == 101:  # 101 = HIT
                                # deal one more card to the player
                                card = self.shuffled_cards.item(played_card_count)
                                played_card_count += 1
                                remaining_card_count -= 1
                                player.dealt_card(card, hand_index)

                                # card counting advertisement to card counter(s)
                                for player_to_advertise in self.players:
                                    player_to_advertise.card_counter.count_card_values(card)

                                log.info(f'Gave {card}\tto the player #{player.player_id} hand #{hand_index}. '
                                         f'Hand is now {player.hands[hand_index].cards}')

                            elif hit_or_stand == 100:  # 100 = STAND

                                log.info(f'Player #{player.player_id}\'s hand #{hand_index} stands with '
                                         f'{player.hands[hand_index].cards} and count '
                                         f'{player.hands[hand_index].calculate_hand()}')

                                break  # stop checking

                            elif hit_or_stand == 99:  # 99 = BUST

                                log.info(f'Player #{player.player_id}\'s hand #{hand_index} busts with '
                                         f'{player.hands[hand_index].cards} and count '
                                         f'{player.hands[hand_index].calculate_hand()}')

                                break  # stop checking

                            elif hit_or_stand == 102:  # 102 = SPLIT

                                log.info(f'Player #{player.player_id}\'s hand #{hand_index} splits with '
                                         f'{player.hands[hand_index].cards} and count '
                                         f'{player.hands[hand_index].calculate_hand()}')

                                # deal first card to the player
                                card = self.shuffled_cards.item(played_card_count)
                                played_card_count += 1
                                remaining_card_count -= 1
                                player.dealt_card(card, hand_index)

                                # card counting advertisement to card counter(s)
                                for player_to_advertise in self.players:
                                    player_to_advertise.card_counter.count_card_values(card)

                                log.info(f'Gave {card}\tto the player #{player.player_id} hand #{hand_index}. '
                                         f'Hand is now {player.hands[hand_index].cards}')

                                # deal second card to player
                                card = self.shuffled_cards.item(played_card_count)
                                played_card_count += 1
                                remaining_card_count -= 1
                                player.dealt_card(card, hand_index + 1)
                                # WARNING:because multiple splits are not available, hand_index+1 shouldn't be a problem

                                # card counting advertisement to card counter(s)
                                for player_to_advertise in self.players:
                                    player_to_advertise.card_counter.count_card_values(card)

                                # TODO check correctness
                                if player.is_split_aces:  # if the player has split aces. make it stand
                                    player.hands[hand_index].state = 100  # 100 = STAND

                                log.info(f'Gave {card}\tto the player #{player.player_id} hand #{hand_index + 1}. '
                                         f'Hand is now {player.hands[hand_index + 1].cards}')

                            elif hit_or_stand == 103:  # 103 = DOUBLE DOWN
                                # deal one more card to the player and stand
                                card = self.shuffled_cards.item(played_card_count)
                                played_card_count += 1
                                remaining_card_count -= 1
                                player.dealt_card(card, hand_index)
                                player.hands[hand_index].double_hand()  # double the bet

                                # card counting advertisement to card counter(s)
                                for player_to_advertise in self.players:
                                    player_to_advertise.card_counter.count_card_values(card)

                                log.info(f'Gave {card}\tto the player #{player.player_id} hand #{hand_index}. '
                                         f'Hand is now {player.hands[hand_index].cards}')
                                log.info(f'Player #{player.player_id}\'s hand #{hand_index} stands because '
                                         f'double down with {player.hands[hand_index].cards} and count '
                                         f'{player.hands[hand_index].calculate_hand()}')

                                player.hands[hand_index].state = 100
                                # 100 = STAND (its a rule to stand after doubling down)

                            else:
                                log.fatal('WRONG input ', hit_or_stand)
                                exit()
                                break

                        hand_index += 1

                # !!!!!ALLOW PLAYERS TO MAKE CHOICE BEFORE THEY SEE THE DEALER'S CLOSED CARD!!!!!!!

                self.dealer.dealt_card(dealer_second_card)

                log.info(f'Gave {dealer_second_card} to the dealer. Card is NOT advertised yet. '
                         f'Hand is now {self.dealer.hand.cards}')

                # card counting of dealers second card advertisement to card counter(s)
                for player_to_advertise in self.players:
                    player_to_advertise.card_counter.count_card_values(dealer_second_card)

                log.info(f'Dealer advertises card {dealer_second_card}')

                # repeat until dealer stands or busts
                while True:

                    # allow dealer to play
                    hit_or_stand = self.dealer.play_hand()

                    if hit_or_stand == 101:  # 101 = HIT
                        # deal one more card to the dealer
                        card = self.shuffled_cards.item(played_card_count)
                        self.dealer.dealt_card(card)
                        played_card_count += 1
                        remaining_card_count -= 1

                        # card counting advertisement to card counter(s)
                        for player_to_advertise in self.players:
                            player_to_advertise.card_counter.count_card_values(card)

                        log.info(f'Gave {card} to the dealer. Hand is now {self.dealer.hand.cards}')

                    elif hit_or_stand == 100:  # 100 = STAND

                        log.info(f'Dealer stands with {self.dealer.hand.cards} and count '
                                 f'{self.dealer.hand.calculate_hand()}')

                        break

                    elif hit_or_stand == 99:  # 99 = BUST

                        log.info(f'Dealer busts with {self.dealer.hand.cards} and count '
                                 f'{self.dealer.hand.calculate_hand()}')

                        break

                    else:
                        log.fatal('WRONG input ', hit_or_stand)
                        exit()
                        break

                # check if the player won here TODO: fix if needed

                dealer_hand_calculation = self.dealer.hand.calculate_hand()
                for player in self.players:
                    hand_index = 0

                    while hand_index < len(player.hands):

                        state = player.hands[hand_index].state

                        if state == 100:  # 100 = STAND (NOT BUST)

                            log.info(f'Player #{player.player_id}\'s hand #{hand_index} previously '
                                     f'"Stand"ed with {player.hands[hand_index].cards} and count '
                                     f'{player.hands[hand_index].calculate_hand()}')

                            player_hand_calculation = player.hands[hand_index].calculate_hand()

                            assert player_hand_calculation <= 21

                            if player_hand_calculation == 21 and dealer_hand_calculation == 21:
                                is_blackjack = player.hands[hand_index].is_blackjack(player.is_split)
                                is_dealer_blackjack = self.dealer.hand.is_blackjack(False)

                                if is_blackjack and is_dealer_blackjack:
                                    player.push_hand(hand_index)
                                elif is_blackjack and not is_dealer_blackjack:
                                    player.won_hand(hand_index)
                                elif not is_blackjack and is_dealer_blackjack:
                                    player.lost_hand(hand_index)
                                elif not is_blackjack and not is_dealer_blackjack:
                                    player.push_hand(hand_index)
                                else:
                                    log.fatal('WRONG logic')
                                    exit()

                            elif dealer_hand_calculation > 21:  # player has STANDed so player cant lose
                                player.won_hand(hand_index)

                            elif player_hand_calculation > dealer_hand_calculation:
                                player.won_hand(hand_index)

                            elif player_hand_calculation == dealer_hand_calculation:
                                player.push_hand(hand_index)

                            else:
                                player.lost_hand(hand_index)

                        elif state == 99:  # 99 = BUST

                            log.info(f'Player #{player.player_id}\'s hand #{hand_index} previously '
                                     f'"Bust"ed with {player.hands[hand_index].cards} and count '
                                     f'{player.hands[hand_index].calculate_hand()}')

                            player.lost_hand(hand_index)

                        else:
                            log.fatal('WRONG input ', state)
                            exit()

                        hand_index += 1

                player_bankrolls = []
                player_counts = []
                player_systems = []
                player_total_bets = []
                for player in self.players:
                    player_bankrolls.append(player.bankroll)
                    player.card_counter.calculate_true_count()  # TODO hope this doesnt break things esp. LSTM!!!!
                    player_counts.append(player.card_counter.true_count)
                    player_systems.append(player.card_counter.strategy_name)
                    player_total_bets.append(player.total_bet_amount)

                log.info(f'The game hand has ended')
                log.info(f'played_card_count is {played_card_count}')

                total_cards = remaining_card_count + played_card_count

                log.info(f'total_cards is {total_cards}')

                percentage_of_cards_played = played_card_count / total_cards

                log.info(f'percentage_of_cards_played is {percentage_of_cards_played}')

                if percentage_of_cards_played > 0.80:  # check penetration. reshuffle before done
                    needs_reshuffle = True

                self.game_data_dump.append(GameDataDump.GameDataDump(shuffled_cards=self.shuffled_cards,
                                                                     min_bet=self.min_bet, max_bet=self.max_bet,
                                                                     no_of_decks=self.no_of_decks,
                                                                     no_of_players=self.no_of_players,
                                                                     player_start_bankroll=self.player_start_bankroll,
                                                                     no_of_games_played=no_of_games_played,
                                                                     no_of_hands_played=no_of_hands_played,
                                                                     needs_reshuffle=needs_reshuffle,
                                                                     player_bankrolls=player_bankrolls,
                                                                     player_total_bets=player_total_bets,
                                                                     player_counts=player_counts,
                                                                     player_systems=player_systems,
                                                                     total_card_count=total_card_count,
                                                                     played_card_count=played_card_count,
                                                                     remaining_card_count=remaining_card_count))

                self.dealer.end_of_hand()  # clears dealer hand

                for player in self.players:
                    mean_hand_return = player.end_of_hand()  # clears players' hands and counts

                    if player.player_id == 0:
                        control_mean_hand_return = mean_hand_return
                    elif mean_hand_return > control_mean_hand_return:
                        player.better_than_control_count += 1
                        log.info(f'Player #{player.player_id} is better than control with mean hand return of '
                                 f'{mean_hand_return} vs controls mean hand return {control_mean_hand_return}')

                # end of hand
                no_of_hands_played += 1

                # early stop. be careful with going over this limit!!
                if self.no_of_hands_limit == no_of_hands_played:
                    log.info(f'Stopped at hand #{no_of_hands_played} due to early stopping')
                    break

            # end of the deck

            total_percentage_of_cards_played += percentage_of_cards_played

            log.info(f'percentage_of_cards_played in this game is {percentage_of_cards_played}')

            for player in self.players:
                log.info(f'Player #{player.player_id}\'s running count is {player.card_counter.running_count}')
                player.end_of_game()  # clears players' hands and counts

            log.info(f'End of game #{no_of_games_played}')

            # early stop
            if self.no_of_hands_limit == no_of_hands_played:
                log.info(f'Stopped at hand #{no_of_hands_played} due to early stopping')
                break

        end_time = time.time()

        log.info(f'End of game #{no_of_games_played}')
        log.info(f'End of hand #{no_of_hands_played}')

        player_final_bankrolls = []
        player_against_control = []
        strategy_names = []
        count_list = []

        for player in self.players:
            log.info(f'Player #{player.player_id}\'s bankroll is {player.bankroll}')
            log.info(f'Player #{player.player_id}\'s times better than control is {player.better_than_control_count}')

            player_final_bankrolls.append(player.bankroll)
            player_against_control.append(player.better_than_control_count)
            strategy_names.append(player.card_counter.strategy_name)

            if player.card_counter.generate_csv:
                count_list = player.card_counter.count_list

        return TestResults.TestResults(no_of_games_played, no_of_hands_played,
                                       player_final_bankrolls, player_against_control, strategy_names,
                                       end_time - start_time,
                                       total_percentage_of_cards_played / no_of_games_played * 100,
                                       # average percentage
                                       self.min_bet, self.max_bet, self.no_of_decks, self.player_start_bankroll,
                                       count_list, self.game_data_dump, player_total_bets)
