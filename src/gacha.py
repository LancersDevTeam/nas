import os
import numpy as np
from random import random

GACHA_WIN_RATE = float(os.environ['GACHA_WIN_RATE'])


def select_prize():
    prizes = ['prize_1', 'prize_2', 'prize_3', 'prize_4', 'prize_5']
    return np.random.choice(prizes)


def roll_a_gacha():
    roll_a_rate = random()
    if roll_a_rate > (1-GACHA_WIN_RATE):
        prize = select_prize()
        return prize

    return ''
