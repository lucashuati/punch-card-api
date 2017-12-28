from itertools import groupby
from datetime import timedelta

FIRST_IN = 0
FIRST_OUT = 1
SECCOND_IN = 2
SECCOND_OUT = 3


def group(iterable, key, value=lambda x: x):
    return dict((k, list(map(value, values))) for k, values in groupby(sorted(iterable, key=key), key))


def punchcards_group_by_day(punch_cards):
    return group(
        punch_cards,
        lambda punch_card: punch_card.hit_time.strftime('%d/%m/%y'),
        lambda punch_card: punch_card
    )


def sum_time(punch_cards_per_day):
    working_time = 0
    for key, punch_cards in punch_cards_per_day.items():
        nr_punch_cards = len(punch_cards)
        if not nr_punch_cards % 2:  # punch cards are correct, 2 or 4 hits per day
            first_turn = punch_cards[FIRST_OUT].hit_time - punch_cards[FIRST_IN].hit_time
            seccond_turn = timedelta(0)
            if nr_punch_cards > 2:  # if had lunch time
                seccond_turn = punch_cards[SECCOND_OUT].hit_time - punch_cards[SECCOND_IN].hit_time
            day_working = first_turn + seccond_turn
            working_time += day_working.seconds
    return {
        'seconds': int(working_time),
        'minutes': int(working_time / 60),
        'hours': int(working_time / 3600)
    }


def get_acumulate(punch_cards):
    punch_cards_per_day = punchcards_group_by_day(punch_cards)
    return sum_time(punch_cards_per_day)
