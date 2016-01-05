#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from pprint import pprint
ROOT = os.path.join(os.path.dirname(__file__), '..')


def main():
    abooks = load_books('audioteka.json')
    ebooks = load_books('swiatczytnikow.json')
    m = match(abooks, ebooks, index)
    title_m = match(abooks, ebooks, title_index)
    diff = filter(lambda x: x not in m, title_m)
    # pprint({d['title']: find(d['title'], abooks + ebooks) for d in diff})
    print('Audiobooks: ', len(abooks))
    print('Ebooks: ', len(ebooks))
    print('Match: ', len(m))
    print('Tittles match: ', len(title_m))
    print('Diffrence Matched to Title Matched: ', len(diff))
    print('M2T ratio: ', round(len(m) / float(len(title_m)), 2))


def load_books(filename):
    with open(os.path.join(ROOT, 'tmp', filename), 'r') as f:
        return json.load(f, 'utf-8')


def index(books):
    # TODO: Normalize author
    # TODO: Normalize title
    return {(b['title'], b['author']): b for b in books}


def title_index(books):
    return {b['title']: b for b in books}


def find(title, books):
    return [book['author'] for book in books if book['title'] == title]


def match(a, b, index_func):
    index_a = index_func(a)
    index_b = index_func(b)
    m = set(index_a).intersection(set(index_b))
    return [index_a[k] for k in m]


if __name__ == "__main__":
    main()
