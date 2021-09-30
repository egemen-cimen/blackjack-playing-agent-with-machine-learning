# import Settings


class TestResults(object):
    def __init__(self, no_of_games_played, no_of_hands_played, player_final_bankrolls,
                 player_against_control, strategy_names, time_elapsed, average_percentage_of_cards_played,
                 min_bet, max_bet, no_of_decks, player_start_bankroll, count_list, game_data_dump, player_total_bets):
        self.no_of_games_played = no_of_games_played
        self.no_of_hands_played = no_of_hands_played
        self.player_final_bankrolls = player_final_bankrolls  # list of doubles
        self.player_against_control = player_against_control  # list of integers
        self.strategy_names = strategy_names
        self.time_elapsed = time_elapsed
        self.average_percentage_of_cards_played = average_percentage_of_cards_played

        self.min_bet = min_bet
        self.max_bet = max_bet
        self.no_of_decks = no_of_decks
        self.player_start_bankroll = player_start_bankroll

        self.count_list = count_list

        self.game_data_dump = game_data_dump

        self.player_total_bets = player_total_bets
