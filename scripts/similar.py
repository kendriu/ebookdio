#!/usr/bin/env python
import json
import sys
from collections import namedtuple
from difflib import SequenceMatcher

Book = namedtuple('Book', 'title author note people')
Pair = namedtuple('Pair', 'audio lubimy ratio')
null_book = Book(None, None, None, None)

with open(sys.argv[1], 'r') as f:
    owned = json.load(f)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


pairs = []
for v in owned.values():
    a = v['audio']
    l = v['lubimy']
    a = Book(a['title'], a['author'], None, None)
    l = Book(l['title'], l['author'], l['note'], l['people'])
    if l == null_book:
        continue
    ratio = similar(f'{a.title}{a.author}', f'{l.title}{l.author}')
    pairs.append(Pair(a, l, ratio))
try:
    min_people = int(sys.argv[2])
except IndexError:
    min_people = 1

for a, l, r in sorted((p for p in pairs if p.lubimy.people >= min_people
                                           and p.audio.author.split()[-1] != p.lubimy.author.split()[-1]),
                      key=lambda p: p.ratio, reverse=True):
    try:
        print(f'[{r}]{l.note}({l.people}) {a.title}({a.author}) [{l.title}({l.author})]')
    except BrokenPipeError:
        pass

