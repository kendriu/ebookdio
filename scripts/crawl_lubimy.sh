#!/usr/bin/env bash

PYTHONUNBUFFERED=1 ./crawl_lubimy.py ../tmp/audioteka.json ../tmp/books.json | tee ../tmp/log.txt
