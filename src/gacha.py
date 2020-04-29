import os
import numpy as np

GACHA_WIN_RATE = os.environ['GACHA_WIN_RATE']


def select_prize():
    prizes = ['prize_1', 'prize_2', 'prize_3', 'prize_4', 'prize_5']
    return np.random.choice(prizes)
