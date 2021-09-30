import numpy as np


# system counting information from: https://qfit.com/card-counting.htm
def get_system_counting_rules_by_name(system_name):
    if system_name == 'Hi-Lo':
        # 2,3,4,5,6 are +1; 7,8,9 are 0; 10,j,q,k,a are -1
        #                2  3  4  5  6  7  8  9  10   a
        return np.array([1, 1, 1, 1, 1, 0, 0, 0, -1, -1])

    elif system_name == 'Hi-Opt I':
        #                2  3  4  5  6  7  8  9  10  a
        return np.array([0, 1, 1, 1, 1, 0, 0, 0, -1, 0])

    elif system_name == 'Canfield Expert':
        #                2  3  4  5  6  7  8   9  10  a
        return np.array([0, 1, 1, 1, 1, 1, 0, -1, -1, 0])

    elif system_name == 'Canfield Master':
        #                2  3  4  5  6  7  8   9  10  a
        return np.array([1, 1, 2, 2, 2, 1, 0, -1, -2, 0])

    elif system_name == 'Hi-Opt II':
        #                2  3  4  5  6  7  8  9  10  a
        return np.array([1, 1, 2, 2, 1, 1, 0, 0, -2, 0])

    elif system_name == 'Silver Fox':
        #                2  3  4  5  6  7  8   9  10   a
        return np.array([1, 1, 1, 1, 1, 1, 0, -1, -1, -1])

    elif system_name == 'Zen':
        #                2  3  4  5  6  7  8  9  10   a
        return np.array([1, 1, 2, 2, 2, 1, 0, 0, -2, -1])

    elif system_name == 'ML':
        #                2  3  4  5  6  7  8  9 10  a
        return np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    else:
        return np.array([])
