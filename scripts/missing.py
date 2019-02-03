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
    if l != null_book:
        continue
    pairs.append(Pair(a, l))

try:
    min_people = int(sys.argv[2])
except IndexError:
    min_people = 1

count = 0
for a, l in sorted(pairs, key=lambda p: (p.audio.title, p.audio.author)):
    count += 1
    try:
        print(f'{a.title}({a.author})')
    except BrokenPipeError:
        pass
print(f'Missing: {count}')

