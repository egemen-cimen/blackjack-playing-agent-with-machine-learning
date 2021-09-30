import numpy as np


class GameDataDump(object):
    def __init__(self, shuffled_cards, min_bet, max_bet, no_of_decks, no_of_players,
                 player_start_bankroll, no_of_games_played, no_of_hands_played,
                 player_bankrolls, player_counts, player_systems, needs_reshuffle,
                 total_card_count, played_card_count, remaining_card_count, player_total_bets):
        self.shuffled_cards = np.copy(shuffled_cards)
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.no_of_decks = no_of_decks
        self.no_of_players = no_of_players
        self.player_start_bankroll = player_start_bankroll
        self.no_of_games_played = no_of_games_played
        self.no_of_hands_played = no_of_hands_played
        self.player_systems = player_systems
        self.player_counts = player_counts
        self.player_bankrolls = player_bankrolls
        self.player_total_bets = player_total_bets
        self.total_card_count = total_card_count
        self.played_card_count = played_card_count
        self.remaining_card_count = remaining_card_count
        self.needs_reshuffle = needs_reshuffle
