#!/usr/bin/python3

import Settings
import Game
import CountingSystems
import csv  # to write count_list to a file for machine learning
import logging
import tkinter as tk
import numpy as np
import scipy as sp
from scipy import stats
import math

import os

DEBUG = False
VERBOSE = True

gui = Settings.GUI


class LoadStartScreen:

    def __init__(self, main_window):
        self.frame_top = tk.Frame(main_window)
        self.frame_top.pack()

        label_load_or_new_enquiry = tk.Label(self.frame_top, text="Load a results file or start a new test?")
        label_load_or_new_enquiry.pack()

        button_new_test = tk.Button(self.frame_top, text='Start a new test', fg='green', command=self.start_new_tests)

        button_new_test.pack()

    @staticmethod
    def load_results():
        logging.WARNING('load_results: stubbed')

    def start_new_tests(self):
        # if user wants to start a new test, ask parameters before starting
        self.frame_top.pack_forget()
        TestParameterScreen(main_window, self.frame_top)


class TestParameterScreen:
    def __init__(self, main_window, previous_frame):
        self.previous_frame = previous_frame  # for going back to that frame

        self.frame_top = tk.Frame(main_window)
        self.frame_top.pack()

        self.frame_bottom = tk.Frame(main_window)
        # self.frame_bottom.pack(side=tk.BOTTOM)

        self.frame_bottom.pack()

        # decks 4, 6, 8 for checkbutton
        self.intvar_no_of_decks = [tk.IntVar(), tk.IntVar(), tk.IntVar()]

        # players 1- 7 for checkbutton
        self.intvar_no_of_players = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]

        self.textvar_no_of_hands_per_session = tk.StringVar(self.frame_top, value='100')
        self.textvar_no_of_sessions_list = tk.StringVar(self.frame_top, value='1;2;3')
        self.textvar_no_of_test_repeats = tk.StringVar(self.frame_top, value='1000')
        self.textvar_starting_bankroll = tk.StringVar(self.frame_top, value='10000')
        self.textvar_min_bet = tk.StringVar(self.frame_top, value='10')
        self.textvar_max_bet = tk.StringVar(self.frame_top, value='1000')
        # self.textvar_thread_count = tk.StringVar(self.frame_top, value='2')

        label_no_of_decks_enquiry = tk.Label(self.frame_top, text="How many decks?")
        label_no_of_players_enquiry = tk.Label(self.frame_top, text="How many players?")
        label_no_of_sessions_enquiry_1 = tk.Label(self.frame_top, text="# of hands per session:")
        label_no_of_sessions_enquiry_2 = tk.Label(self.frame_top, text="# of sessions to be played list (; separated):")
        label_no_of_sessions_enquiry_3 = tk.Label(self.frame_top, text="# of times the tests to be repeated:")

        label_starting_bankroll_enquiry = tk.Label(self.frame_top, text="Starting bankroll?")
        label_min_bet_enquiry = tk.Label(self.frame_top, text="Minimum bet amount?")
        label_max_bet_enquiry = tk.Label(self.frame_top, text="Maximum bet amount?")
        # label_thread_count_enquiry = tk.Label(self.frame_top, text="Thread count?")

        frame_no_of_decks_enquiry = tk.Frame(self.frame_top)
        frame_no_of_players_enquiry = tk.Frame(self.frame_top)

        checkbutton_no_of_decks_enquiry = [
            tk.Checkbutton(frame_no_of_decks_enquiry, text='4', variable=self.intvar_no_of_decks[0]),
            tk.Checkbutton(frame_no_of_decks_enquiry, text='6', variable=self.intvar_no_of_decks[1]),
            tk.Checkbutton(frame_no_of_decks_enquiry, text='8', variable=self.intvar_no_of_decks[2])]

        checkbutton_no_of_players_enquiry = [
            tk.Checkbutton(frame_no_of_players_enquiry, text='1', variable=self.intvar_no_of_players[0]),
            tk.Checkbutton(frame_no_of_players_enquiry, text='2', variable=self.intvar_no_of_players[1]),
            tk.Checkbutton(frame_no_of_players_enquiry, text='3', variable=self.intvar_no_of_players[2]),
            tk.Checkbutton(frame_no_of_players_enquiry, text='4', variable=self.intvar_no_of_players[3]),
            tk.Checkbutton(frame_no_of_players_enquiry, text='5', variable=self.intvar_no_of_players[4]),
            tk.Checkbutton(frame_no_of_players_enquiry, text='6', variable=self.intvar_no_of_players[5]),
            tk.Checkbutton(frame_no_of_players_enquiry, text='7', variable=self.intvar_no_of_players[6])]

        # frame_no_of_sessions_start_end_multiply_enquiry = tk.Frame(self.frame_top)
        entry_no_of_hands_per_session_enquiry = tk.Entry(self.frame_top, textvariable=self.textvar_no_of_hands_per_session)
        entry_no_of_sessions_list_enquiry = tk.Entry(self.frame_top, textvariable=self.textvar_no_of_sessions_list)
        entry_no_of_test_repeats_enquiry = tk.Entry(self.frame_top, textvariable=self.textvar_no_of_test_repeats)

        entry_starting_bankroll_enquiry = tk.Entry(self.frame_top, textvariable=self.textvar_starting_bankroll)
        entry_min_bet_enquiry = tk.Entry(self.frame_top, textvariable=self.textvar_min_bet)
        entry_max_bet_enquiry = tk.Entry(self.frame_top, textvariable=self.textvar_max_bet)
        # entry_thread_count_enquiry = tk.Entry(self.frame_top, textvariable=self.textvar_thread_count)

        label_no_of_decks_enquiry.grid(row=0, column=0, sticky=tk.E)
        label_no_of_players_enquiry.grid(row=1, column=0, sticky=tk.E)
        label_no_of_sessions_enquiry_1.grid(row=2, column=0, sticky=tk.E)
        label_no_of_sessions_enquiry_2.grid(row=3, column=0, sticky=tk.E)
        label_no_of_sessions_enquiry_3.grid(row=4, column=0, sticky=tk.E)

        label_starting_bankroll_enquiry.grid(row=5, column=0, sticky=tk.E)
        label_min_bet_enquiry.grid(row=6, column=0, sticky=tk.E)
        label_max_bet_enquiry.grid(row=7, column=0, sticky=tk.E)
        # label_thread_count_enquiry.grid(row=8, column=0, sticky=tk.E)

        frame_no_of_decks_enquiry.grid(row=0, column=1, sticky=tk.W)

        checkbutton_index = 0
        while checkbutton_index < len(checkbutton_no_of_decks_enquiry):
            checkbutton_no_of_decks_enquiry[checkbutton_index].grid(row=0, column=1 + checkbutton_index, sticky=tk.W)

            checkbutton_index += 1

        frame_no_of_players_enquiry.grid(row=1, column=1, sticky=tk.W)

        checkbutton_index = 0
        while checkbutton_index < len(checkbutton_no_of_players_enquiry):
            checkbutton_no_of_players_enquiry[checkbutton_index].grid(row=1, column=1 + checkbutton_index, sticky=tk.W)

            checkbutton_index += 1

        # frame_no_of_sessions_start_end_multiply_enquiry.grid(row=2, column=1, sticky=tk.W)
        entry_no_of_hands_per_session_enquiry.grid(row=2, column=1, sticky=tk.W)
        entry_no_of_sessions_list_enquiry.grid(row=3, column=1, sticky=tk.W)
        entry_no_of_test_repeats_enquiry.grid(row=4, column=1, sticky=tk.W)

        entry_starting_bankroll_enquiry.grid(row=5, column=1, sticky=tk.W)
        entry_min_bet_enquiry.grid(row=6, column=1, sticky=tk.W)
        entry_max_bet_enquiry.grid(row=7, column=1, sticky=tk.W)
        # entry_thread_count_enquiry.grid(row=8, column=1, sticky=tk.W)

        button_confirm_tests = tk.Button(self.frame_bottom, text='Confirm tests', fg='green',
                                         command=self.confirm_tests)
        button_cancel = tk.Button(self.frame_bottom, text='Cancel & Exit', fg='red', command=self.frame_bottom.quit)
        button_back = tk.Button(self.frame_bottom, text='Go back', fg='gray21', command=self.go_back)

        button_confirm_tests.pack(side=tk.RIGHT)
        button_cancel.pack(side=tk.RIGHT)
        button_back.pack(side=tk.RIGHT)

    def confirm_tests(self):

        exception_occurred = False
        no_of_hands_per_session = 0
        no_of_sessions_list = []
        no_of_test_repeats = 0
        starting_bankroll = 0
        min_bet = 0
        max_bet = 0

        try:
            no_of_hands_per_session = int(self.textvar_no_of_hands_per_session.get())
        except ValueError:
            self.textvar_no_of_hands_per_session.set('wrong value!')
            exception_occurred = True

        try:
            tmp_list = self.textvar_no_of_sessions_list.get().split(';')
            for number in tmp_list:
                if int(number) > 0:
                    no_of_sessions_list.append(int(number))
        except ValueError:
            self.textvar_no_of_sessions_list.set('wrong value!')
            exception_occurred = True

        try:
            no_of_test_repeats = int(self.textvar_no_of_test_repeats.get())
            if no_of_test_repeats < 1:
                no_of_test_repeats = 1  # cant repeat with 0
        except ValueError:
            self.textvar_no_of_test_repeats.set('wrong value!')
            exception_occurred = True

        try:
            starting_bankroll = int(int(self.textvar_starting_bankroll.get()))
        except ValueError:
            self.textvar_starting_bankroll.set('wrong value!')
            exception_occurred = True

        try:
            min_bet = int(self.textvar_min_bet.get())
        except ValueError:
            self.textvar_min_bet.set('wrong value!')
            exception_occurred = True

        try:
            max_bet = int(self.textvar_max_bet.get())
        except ValueError:
            self.textvar_max_bet.set('wrong value!')
            exception_occurred = True

        # check if deck and player checkboxes have at least one check
        i = 0
        total = 0
        while i < len(self.intvar_no_of_decks):
            total += self.intvar_no_of_decks[i].get()
            i += 1
        if total == 0:  # means nothing selected
            exception_occurred = True

        i = 0
        total = 0
        while i < len(self.intvar_no_of_players):
            total += self.intvar_no_of_players[i].get()
            i += 1
        if total == 0:  # means nothing selected
            exception_occurred = True

        if not exception_occurred:

            if DEBUG:
                i = 0
                while i < len(self.intvar_no_of_decks):
                    logging.DEBUG(4 + i * 2, 'Decks:', self.intvar_no_of_decks[i].get() == 1)
                    i += 1

                i = 0
                while i < len(self.intvar_no_of_players):
                    logging.DEBUG(2 + i, 'Players:', self.intvar_no_of_players[i].get() == 1)
                    i += 1

                logging.DEBUG('Starting bankroll:', starting_bankroll)
                logging.DEBUG('No of sessions:', no_of_hands_per_session, 'to',
                              no_of_sessions_list, 'with', no_of_test_repeats, 'repeats')
                logging.DEBUG('Bet range:', min_bet, '-', max_bet)

            self.frame_top.pack_forget()
            self.frame_bottom.pack_forget()

            TestScreen(main_window=main_window, no_of_hands_per_session=no_of_hands_per_session,
                       no_of_sessions_list=no_of_sessions_list, no_of_repeats=no_of_test_repeats,
                       list_of_decks=self.intvar_no_of_decks, list_of_players=self.intvar_no_of_players,
                       starting_bankroll=starting_bankroll, min_bet=min_bet, max_bet=max_bet)

    def go_back(self):  # TODO give the extra parameters (top and bottom frames) or don't and destroy these
        self.frame_top.destroy()
        self.frame_bottom.destroy()

        # pack the previous frame back
        self.previous_frame.pack()


class TestScreen:
    def __init__(self, main_window, no_of_hands_per_session, no_of_sessions_list, no_of_repeats,
                 list_of_decks, list_of_players, starting_bankroll, min_bet, max_bet):
        # self.previous_frame = previous_frame # for going back to that frame

        random_seeds = Settings.RANDOM_LIST

        np.random.seed(42)  # seed np.shuffle with a number to get same seeds/cards
        np.random.shuffle(random_seeds)

        self.frame_top = tk.Frame(main_window)
        self.frame_top.pack()

        self.frame_bottom = tk.Frame(main_window)
        self.frame_bottom.pack()

        self.list_of_games = no_of_sessions_list

        self.list_of_decks = []
        i = 0
        while i < len(list_of_decks):
            if list_of_decks[i].get() == 1:
                self.list_of_decks.append(4 + i * 2)
            i += 1

        self.list_of_players_extend = []
        self.list_of_players = []
        i = 0
        column_count = 0
        while i < len(list_of_players):
            if list_of_players[i].get() == 1:
                column_count += (i + 1) * 2  # 2 information per player (bankroll, against control)

                self.list_of_players.append(i + 1)

                for tmp in range(i + 2):
                    self.list_of_players_extend.append(tmp)

            i += 1

        row_count = len(self.list_of_games) * len(self.list_of_decks)

        label_rows = []
        stringvar_rows = []
        i = 0
        game_index = -1
        deck_index = -1
        while i < row_count:

            # add no of games and no of decks information labels
            if i % len(self.list_of_decks) == 0:
                game_index += 1

            deck_index += 1
            if deck_index % len(self.list_of_decks) == 0:
                deck_index = 0

            label_cols = []

            label_temp = tk.Label(self.frame_top, relief=tk.RIDGE)
            text = '%d sessions; %d decks' % (self.list_of_games[game_index], self.list_of_decks[deck_index])

            label_temp.config(text=text)
            label_temp.grid(row=i + 1, column=0, sticky=tk.W)

            label_cols.append(label_temp)  # information label

            # fill table
            stringvar_cols = []

            # add information labels players and bankroll/advantage
            player_index = -1
            bankroll_vs_advantage = -1

            j = 0
            while j < column_count:

                if j % 2 == 0:  # 2 is for bankroll/advantage
                    player_index += 1

                bankroll_vs_advantage += 1
                if bankroll_vs_advantage % 2 == 0:  # 2 is for bankroll/advantage
                    bankroll_vs_advantage = 0

                label_temp = tk.Label(self.frame_top, relief=tk.RIDGE)

                player_no = self.list_of_players_extend[player_index % len(self.list_of_players_extend)]
                if bankroll_vs_advantage == 0:
                    if player_no == 0:
                        label_temp.config(fg='blue', text=f'Player {player_no}\'s ({Settings.SYSTEMS[player_no]})\nbankroll Δ% ±(95% CI)')
                        # paint first player of an experiment into blue
                    else:
                        label_temp.config(text=f'Player {player_no}\'s ({Settings.SYSTEMS[player_no]})\nbankroll Δ% ±(95% CI)')
                else:
                    label_temp.config(text='Player%d\'s advantage\n±(95%% CI)' % player_no)  # player advantage info labels
                    # label_temp.config(background='white')
                    pass

                label_temp.grid(row=0, column=j + 1, sticky=tk.W)

                stringvar_text = tk.StringVar()
                stringvar_cols.append(stringvar_text)

                e = tk.Label(self.frame_top, relief=tk.RIDGE, textvariable=stringvar_text)
                e.grid(row=i + 1, column=j + 1, sticky=tk.E)

                stringvar_text.set('-')
                # stringvar_text.set('%d.%d' % (i, j))

                label_cols.append(e)

                j += 1

            label_rows.append(label_cols)
            stringvar_rows.append(stringvar_cols)

            i += 1

        # button_save_to_file = tk.Button(self.frame_bottom, text='Save to file', fg='green', command=self.save_to_file)
        button_exit = tk.Button(self.frame_bottom, text='Exit', fg='red', command=self.frame_bottom.quit)

        # button_save_to_file.pack(side=tk.RIGHT)
        button_exit.pack(side=tk.RIGHT)

        # count_list = []

        count_filename = 'count_list_for_ml.csv'
        game_dump_filename = 'game_dump_info.csv'
        with open(game_dump_filename, 'w') as myfile:
            count_writer = csv.writer(myfile)

            count_writer.writerow(['min_bet', 'max_bet', 'no_of_decks', 'no_of_players',
                                   'player_start_bankroll', 'no_of_games_played', 'no_of_hands_played',
                                   'needs_reshuffle',
                                   'player_bankrolls', 'player_total_bets', 'player_counts', 'player_systems',
                                   'total_card_count', 'remaining_card_count', 'played_card_count', 'shuffled_cards'])

        total_file_len = 0
        with open(count_filename, 'w') as myfile:
            count_writer = csv.writer(myfile)

            count_writer.writerow(
                ['card2', 'card3', 'card4', 'card5', 'card6', 'card7', 'card8', 'card9', 'card10', 'card11',
                 'shoe_pen', 'f_count', 'card2_per_hand', 'card3_per_hand', 'card4_per_hand', 'card5_per_hand',
                 'card6_per_hand', 'card7_per_hand', 'card8_per_hand', 'card9_per_hand', 'card10_per_hand',
                 'card11_per_hand'])

            session_index = 0
            for session in self.list_of_games:
                deck_index = 0
                for deck in self.list_of_decks:
                    column_index = 0
                    for player in self.list_of_players:
                        # run test

                        tmp = self.run_one_test(random_seeds=random_seeds,  # same seeds for every game
                                                stringvar_rows=stringvar_rows,
                                                column_index=session_index * len(self.list_of_decks) + deck_index,
                                                row_index=column_index,
                                                no_of_decks=deck,
                                                no_of_players=player,
                                                no_of_games=session,  # doesnt really matter here
                                                no_of_hands_limit=session*no_of_hands_per_session,
                                                no_of_repeats=no_of_repeats,
                                                player_start_bankroll=starting_bankroll,
                                                min_bet=min_bet,
                                                max_bet=max_bet,
                                                main_window=main_window)

                        for row in tmp:
                            count_writer.writerow(row)

                        total_file_len += len(tmp)

                        column_index += (player * 2)
                        player_index += 1
                    deck_index += 1
                session_index += 1

        print('Written to', count_filename, '(', total_file_len, ')')

    # do actual simulation work and fill in the table

    @staticmethod
    def save_to_file():
        print('save_to_file: stubbed')

    @staticmethod
    def run_one_test(random_seeds, stringvar_rows, column_index, row_index, no_of_decks, no_of_players, no_of_games,
                     no_of_hands_limit, no_of_repeats, player_start_bankroll, min_bet, max_bet, main_window):

        game = [None] * no_of_repeats
        test_result = [None] * no_of_repeats

        if no_of_repeats > len(random_seeds):
            print(f'BlackjackSimulatorMain: {no_of_repeats} repeats are requested'
                  f' but there are only {len(random_seeds)} random seeds')
        i = 0
        while i < no_of_repeats:
            systems = Settings.SYSTEMS  # TODO IMPORTANT change systems sometime

            game[i] = Game.Game(seed=random_seeds[i % len(random_seeds)],  # a different random seed for every repeat
                                no_of_decks=no_of_decks,
                                no_of_players=no_of_players,
                                no_of_games_to_be_played=no_of_hands_limit,  # doesnt matter
                                # no_of_games_to_be_played=no_of_games,
                                player_start_bankroll=player_start_bankroll,
                                no_of_hands_limit=no_of_hands_limit,
                                min_bet=min_bet,
                                max_bet=max_bet,
                                systems=systems)
            i += 1

        game_dump_filename = 'game_dump_info.csv'
        total_file_len = 0

        with open(game_dump_filename, 'a') as myfile:
            count_writer = csv.writer(myfile)

            i = 0
            while i < no_of_repeats:
                test_result[i] = game[i].start_game()

                for data in test_result[i].game_data_dump:
                    row = [data.min_bet,
                           data.max_bet,
                           data.no_of_decks,
                           data.no_of_players,
                           data.player_start_bankroll,
                           data.no_of_games_played-1,
                           data.no_of_hands_played+1,
                           data.needs_reshuffle,
                           data.player_bankrolls,
                           data.player_total_bets,
                           data.player_counts,
                           data.player_systems,
                           data.total_card_count,
                           data.remaining_card_count,
                           data.played_card_count,
                           data.shuffled_cards
                           ]

                    if Settings.WRITE_DUMP:
                        count_writer.writerow(row)

                if Settings.WRITE_DUMP:
                    total_file_len += len(test_result[i].game_data_dump)

                i += 1

        print('Written to', game_dump_filename, '(', total_file_len, ')')


        #while i < no_of_repeats:
        #    total_no_of_hands_played += test_result[i].no_of_hands_played
        #    total_time_elapsed += test_result[i].time_elapsed
        #    advantage = (test_result[i].player_final_bankrolls[0] - player_start_bankroll) / player_start_bankroll
        #    total_advantage_of_basic += advantage

        #    count_list.extend(test_result[i].count_list)

        #    i += 1

        #average_number_of_hands_played = total_no_of_hands_played / no_of_repeats
        #average_time_elapsed = total_time_elapsed / no_of_repeats
        #average_gain_of_basic = total_advantage_of_basic / no_of_repeats * 100
        #advantage_of_basic = average_gain_of_basic / average_number_of_hands_played

        total_no_of_hands_played = 0
        total_time_elapsed = 0
        total_bankroll_change_of_basic = 0
        total_bets_of_basic = 0

        count_list = []

        for result in test_result:
            total_no_of_hands_played += result.no_of_hands_played
            total_time_elapsed += result.time_elapsed

            total_bankroll_change_of_basic += (result.player_final_bankrolls[0] - player_start_bankroll)
            total_bets_of_basic += result.player_total_bets[0]

            count_list.extend(result.count_list)

        average_number_of_hands_played = total_no_of_hands_played / no_of_repeats
        average_time_elapsed = total_time_elapsed / no_of_repeats

        assert total_bets_of_basic > 0
        assert no_of_repeats == len(test_result)

        # advantage_of_basic = total_bankroll_change_of_basic / total_bets_of_basic

        player_index = 0
        write_to_players_index = 0
        while write_to_players_index < len(test_result[0].player_final_bankrolls) * 2:
            total_player_bankrolls = 0
            total_bankroll_change = 0
            total_bets = 0

            bankroll_change_array = np.array([-1]*no_of_repeats)
            total_bet_array = np.array([-1]*no_of_repeats)

            i = 0
            for result in test_result:
                total_player_bankrolls += result.player_final_bankrolls[player_index]
                bankroll_change = (result.player_final_bankrolls[player_index] - player_start_bankroll)
                total_bankroll_change += bankroll_change
                total_bet_of_game = result.player_total_bets[player_index]
                total_bets += result.player_total_bets[player_index]

                bankroll_change_array[i] = bankroll_change
                total_bet_array[i] = total_bet_of_game

                i += 1

            average_player_final_bankrolls = total_player_bankrolls / no_of_repeats  # take average of no_of_repeat runs
            bankroll_change = ((average_player_final_bankrolls - player_start_bankroll) / player_start_bankroll * 100)

            no_of_observations, _, mean, variance, _, _ = sp.stats.describe(bankroll_change_array/player_start_bankroll*100)
            std_dev = math.sqrt(variance)
            confidence_interval = 1.960 * (std_dev / math.sqrt(no_of_observations))  # for 95% CI, Z is 1.960
            bankroll_change_string = '{:+.3f}%'.format(mean) + ' ±({:.3f}%)'.format(confidence_interval)

            stringvar_rows[column_index][row_index + write_to_players_index].set(bankroll_change_string)

            advantages_array = bankroll_change_array / total_bet_array
            no_of_observations, _, mean, variance, _, _ = sp.stats.describe(advantages_array)
            std_dev = math.sqrt(variance)
            confidence_interval = 1.960 * (std_dev/math.sqrt(no_of_observations))  # for 95% CI, Z is 1.960

            player_advantage_string = '{:+.5f}'.format(mean) + ' ±({:.5f})'.format(confidence_interval)
            stringvar_rows[column_index][row_index + 1 + write_to_players_index].set(player_advantage_string)

            main_window.update()  # update the results screen fo the user doesn't get bored watching an empty screen

            if VERBOSE and player_index == 0:
                print(no_of_repeats, 'run average of', int(average_number_of_hands_played), 'hands played in',
                      round(average_time_elapsed, 2), 'seconds in average; advantage:', round(mean, 5))

            write_to_players_index += 2
            player_index += 1

        return count_list


if __name__ == "__main__":

    try:
        os.remove('./simulator.log')
    except FileNotFoundError:
        pass

    logging.basicConfig(filename='simulator.log', level=Settings.LOGGING_LEVEL)

    if gui:
        logging.info('GUI started')

        main_window = tk.Tk()
        main_window.wm_title('Blackjack Simulator')
        main_window.resizable(0, 0)

        # ask user whether they want to load a results file or start a new test
        load_start_screen = LoadStartScreen(main_window)

        main_window.mainloop()

        logging.info('GUI stopped')

    else:
        logging.info('No GUI stated')

        game = Game.Game(Settings.NO_OF_DECKS, Settings.NO_OF_PLAYERS, Settings.NO_OF_GAMES_TO_BE_PLAYED,
                         Settings.NO_OF_HANDS_LIMIT, Settings.PLAYER_START_BANKROLL,
                         Settings.MIN_BET, Settings.MAX_BET)
        test_result = game.start_game()

        if DEBUG:
            logging.DEBUG('Main: End of game # ', test_result.no_of_games_played)
            logging.DEBUG('Main: End of hand # ', test_result.no_of_hands_played)
            logging.DEBUG('Main: Time elapsed ', round(test_result.time_elapsed, 2), 'seconds')
            logging.DEBUG('Main: Average percentage of cards played ',
                          round(test_result.average_percentage_of_cards_played, 2), '%')

            player_index = 0
            while player_index < len(test_result.strategy_names):
                strategy_name = test_result.strategy_names[player_index]
                bankroll = test_result.player_final_bankrolls[player_index]
                against_control_count = test_result.player_against_control[player_index]
                logging.DEBUG('Main: Player #', player_index, 'strategy name:', strategy_name)
                logging.DEBUG('Main: Player #', player_index, 'strategy rule:',
                              CountingSystems.get_system_counting_rules_by_name(strategy_name))
                logging.DEBUG('Main: Player #', player_index, 'bankroll:', bankroll)
                logging.DEBUG('Main: Player #', player_index, 'against control count:', against_control_count)

                player_index += 1
