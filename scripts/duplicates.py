#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import json
import sys

with open(sys.argv[1], 'r') as f:
    data = json.load(f, 'utf-8')

c = collections.Counter((i['title'] for i in data))

dups = (k for k, v in c.items() if v > 1)

result = []
i = 0
for du in dups:
    i += 1
    for d in data:
        if d['title'] == du:
            print d

print("Number of duplicates: " + str(i))
