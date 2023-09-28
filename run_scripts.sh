#!/bin/bash

# Use a cronjob to run this every couple minutes (I recommend every 30 minutes or so)
PATH=$PATH:~/gameping && \

source ~/gameping/menv/bin/activate && \
python ~/gameping/scripts/confirm.py && \
python ~/gameping/scripts/scraper.py