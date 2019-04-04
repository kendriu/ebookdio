#!/usr/bin/env python

from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


print(similar('DrużynaPościg', 'PościgDrużyna'))
