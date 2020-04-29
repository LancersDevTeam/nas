# -*- coding: utf-8 -*-
import sys

from src.gacha import select_prize

sys.path.append('../')


def test_select_prize():
    """Functions for determining gacha prizes
    If you win the gacha, one of the prizes will be selected at random from the set prizes.
    The giveaway is defined in the function.
    I'd really like to cut it out somewhere, but it's too delicate to move it, so I'm writing it here.

    Return:
        str: hit prize name
    """
    prizes = ['prize_1', 'prize_2', 'prize_3', 'prize_4', 'prize_5']
    assert select_prize() in prizes
