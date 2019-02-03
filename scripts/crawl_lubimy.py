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


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)

    conn = aiohttp.TCPConnector(limit=20)
    print(f'Audioteka books:{len(data)}')
    async with aiohttp.ClientSession(connector=conn) as session:
        request_count = 0
        for index, i in enumerate(data):
            if request_count and request_count % 50 == 0:
                await asyncio.sleep(10)
            a = Book(i['title'], i['author'], None, None)
            title = a.title
            if a.title in owned:
                continue

            print(f"Parsing {index}:{a.title} --- {a.author}")

            url = URL + '+'.join(a.title.split())
            try:
                request_count += 1
                text = await fetch(session, url)
            except Exception as e:
                print(f'Cannot fetch: {a.title}. Reason; {e}')
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
                    pairs.append(Pair(a, null_book))
                    continue

                l = Book(title, author, note, people)
                pairs.append(Pair(a, l))
                break
            else:
                pairs.append(Pair(a, null_book))
                print(f'Cannot find:{a.title}')


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    with open(sys.argv[2], 'w') as f:
        json.dump({p.audio.title: {'audio': p.audio._asdict(), 'lubimy': p.lubimy._asdict()} for p in pairs},
                  f, indent=2)
