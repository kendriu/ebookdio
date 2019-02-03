#!/usr/bin/env python
import json
import sys
from collections import namedtuple

Book = namedtuple('Book', 'title author note people')
Pair = namedtuple('Pair', 'audio lubimy')
null_book = Book(None, None, None, None)

with open(sys.argv[1], 'r') as f:
    owned = json.load(f)

pairs = []
for v in owned.values():
    a = v['audio']
    l = v['lubimy']
    a = Book(a['title'], a['author'], None, None)
    l = Book(l['title'], l['author'], l['note'], l['people'])
    if l == null_book:
        continue
    pairs.append(Pair(a, l))

try:
    min_people = int(sys.argv[2])
except IndexError:
    min_people = 1

for a, l in sorted((p for p in pairs if p.lubimy.people >= min_people),
                   key=lambda p: (p.lubimy.note, p.lubimy.people), reverse=True):
    try:
        print(f'{l.note}({l.people}) {a.title}({a.author}) [{l.title}({l.author})]')
    except BrokenPipeError:
        pass

