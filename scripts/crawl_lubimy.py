#!/usr/bin/env python

import re
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
    counter = 0
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)

    conn = aiohttp.TCPConnector(limit=100)
    print(f'Audioteka books:{len(data)}')
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = []
        re_sep = (r'\Wt.\s*\d+',
                  r'\Wtom\s*\d+',
                  r'\Wtom\s*I+',
                  r'\Wcz\.?\s*\d+',
                  r'\Wcz\.?\s*I+',
                  r'\Wpart\s*I+',
                  r'\Wksięga\s*I+',
                  r'\Wwydanie\s*I+',
                  r'\Wczęść\s*\d+',
                  r'\Wczęść\s*I+',
                  r'\Wodcinek\s*\d+',
                  r'\WI+$',
                  )
        for i in data[:100]:
            a = Book(i['title'], i['author'].split(',')[0].strip(), None, None)

            # if a.title in owned:
            #     continue

            search_text = a.title
            for rs in re_sep:
                s = re.split(rs, a.title, flags=re.IGNORECASE)
                if len(s) > 1:
                    search_text = s[0].strip('-,. ')
                    break

            tasks.append(asyncio.ensure_future(fetch_book(session, a, search_text)))
            counter += 1
        pairs.extend(await asyncio.gather(*tasks))
        print(f'Number of parsed books: {counter}')


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def fetch_book(session, a, search_text):
    p = Pair(a, null_book)
    print(f"Parsing {a.title} --- {a.author}")
    url = URL + '+'.join(search_text.split())
    try:
        text = await fetch(session, url)
    except Exception as e:
        print(f'Cannot fetch: {a.title}. Reason; {e}')
        return p

    tree = html.fromstring(text)
    books = tree.find_class("book")
    if not books:
        return p
    match = null_book
    for book in books:
        l = await parse_book(book)
        if l == null_book:
            continue
        if match == null_book:
            match = l

        a_surname = a.author.split()[-1]
        try:
            l_surnames = l.author.split(', ')
        except AttributeError:
            continue
        for sur in l_surnames:
            sur = sur.strip()
            s = sur.split()[-1]

            if a_surname == s:
                if match.title.lower().startswith(a.title.lower()[:1]):
                    match = l
                    break
        else:
            continue
        break
    else:
        print(f'Cannot find:{a.title}')

    if match != null_book and match.title.lower().startswith(a.title.lower()[:1]):
        p = Pair(a, match)

    return p


async def parse_book(book):
    links = book.cssselect('a')
    title = links[1].text
    try:
        author = ', '.join((link.text for link in book.cssselect('span')[0].cssselect('a') if link.text))
    except IndexError:
        author = None
    author = author or None
    stats = book.cssselect('.book-stats span')
    try:
        people = int(stats[0].text)
        note = float(stats[2].text.replace(',', '.'))
    except IndexError:
        # Probably not a book
        return null_book
    return Book(title, author, note, people)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        with open(sys.argv[2], 'w') as f:
            json.dump({p.audio.title: {'audio': p.audio._asdict(),
                                       'lubimy': p.lubimy._asdict()} for p in pairs},
                      f, indent=2)
