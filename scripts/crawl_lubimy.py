#!/usr/bin/env python

import asyncio
import json
import sys
from collections import namedtuple

import aiohttp
from lxml import html

URL = 'http://lubimyczytac.pl/szukaj/ksiazki?phrase='
Book = namedtuple('Book', 'title author note people')
Pair = namedtuple('Pair', 'audio lubimy')
null_book = Book(None, None, None, None)

pairs = []
try:
    with open(sys.argv[2], 'r') as f:
        owned = json.load(f)
except FileNotFoundError:
    owned = {}
else:
    for v in owned.values():
        a = v['audio']
        l = v['lubimy']
        a = Book(a['title'], a['author'], None, None)
        l = Book(l['title'], l['author'], l['note'], l['people'])
        pairs.append(Pair(a, l))


async def main():
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)

    conn = aiohttp.TCPConnector(limit=100)
    print(f'Audioteka books:{len(data)}')
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = []
        for i in data:
            a = Book(i['title'], i['author'], None, None)
            if a.title in owned:
                continue
            tasks.append(asyncio.ensure_future(fetch_book(session, a)))
        pairs.extend(await asyncio.gather(*tasks))


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def fetch_book(session, a):
    p = Pair(a, null_book)
    print(f"Parsing {a.title} --- {a.author}")
    url = URL + '+'.join(a.title.split())
    try:
        text = await fetch(session, url)
    except Exception as e:
        print(f'Cannot fetch: {a.title}. Reason; {e}')
    else:
        tree = html.fromstring(text)
        books = tree.find_class("book")
        for book in books:
            links = book.cssselect('a')
            title = links[1].text
            try:
                author = links[2].text
            except IndexError:
                author = None

            stats = book.cssselect('.book-stats span')
            try:
                people = int(stats[0].text)
                note = float(stats[2].text.replace(',', '.'))
            except IndexError:
                print(f'Cannot parse: {a.title}')
                continue

            l = Book(title, author, note, people)
            p = Pair(a, l)
            break
        else:
            print(f'Cannot find:{a.title}')
    return p


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        with open(sys.argv[2], 'w') as f:
            json.dump({p.audio.title: {'audio': p.audio._asdict(),
                                       'lubimy': p.lubimy._asdict()} for p in pairs},
                      f, indent=2)
