import logging

VERBOSE = False
DEBUG = False
LOGGING_LEVEL = logging.WARNING

SYSTEMS = ['Basic', 'ML', 'Hi-Lo', 'Silver Fox', 'Hi-Opt I', 'Hi-Opt II', 'Canfield Master', 'Canfield Expert']
#SYSTEMS = ['Basic', 'Hi-Lo', 'ML', 'Hi-Lo', 'Hi-Lo', 'Hi-Lo', 'Hi-Lo', 'Hi-Lo']  # TODO change or make gui select
#SYSTEMS = ['ML', 'Hi-Lo', 'ML', 'Hi-Lo', 'Hi-Lo', 'Hi-Lo', 'Hi-Lo', 'Hi-Lo']  # TODO change or make gui select

# WARNING: don't change or remove the first two;
# Info: only the first 7 are used

DOUBLE_AFTER_SPLIT = True
DOUBLE_ALLOWED = True

GENERATE_COUNT_CSV = True
COUNT_SYSTEM_TO_WATCH = 'Hi-Lo'  # must be in the list of SYSTEMS. this system must be playing the game

UTILIZE_ML_MODEL = True
ML_MODEL_TO_UTILIZE = 'ML'

if UTILIZE_ML_MODEL:
    import os
    os.environ['CUDA_VISIBLE_DEVICES'] = '1'  # Random device so tensorflow doesn't use the GPU
    from keras.models import load_model
    MODEL_PATH = './MachineLearningPlayer/machinelearningplayer.h5'
    ml_model = load_model(MODEL_PATH)
    print(ml_model.summary())

GUI = True

PER_HAND = False

WRITE_DUMP = False

# arguments for no-gui
NO_OF_DECKS = 8  # 4, 6, or 8
NO_OF_PLAYERS = 7  # 2-7 players
NO_OF_SESSIONS_LIMIT = -1
NO_OF_HANDS_LIMIT = NO_OF_SESSIONS_LIMIT * 100
NO_OF_GAMES_TO_BE_PLAYED = 1  # doesnt matter if there is a session limit
PLAYER_START_BANKROLL = 10000
MIN_BET = 10
MAX_BET = 500

# Timestamp: 2018-11-28 13:17:09 UTC
# RANDOM.ORG
# Random Integer Set Generator
# 1 set with 10000 unique random integers, taken from the [0,1000000000] range. The integers were not sorted.
# Here is your set:
RANDOM_LIST = []

with open('random_numbers.txt') as number_file:
    for line in number_file:
        numbers = line.split(',')
        for i in range(len(numbers)):
            RANDOM_LIST.append(int(numbers[i]))
