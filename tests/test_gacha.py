# -*- coding: utf-8 -*-
from src.gacha import select_prize, roll_a_gacha


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


def test_roll_a_gacha():
    """Gacha spinning function
    Turn the gacha based on a predetermined probability.
    If the prize is won, the prize is determined by the select_prize() function.
    It's just a matter of turning the gacha. Record writing, etc. is done by another function.

    Return:
        str: hit prize name
    """
    prizes_and_empty = ['prize_1', 'prize_2', 'prize_3', 'prize_4', 'prize_5', '']
    assert roll_a_gacha() in prizes_and_empty
