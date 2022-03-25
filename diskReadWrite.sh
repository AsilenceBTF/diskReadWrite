#!/bin/bash
date=$(date +%Y-%m-%d)
smartctl -a disk0 > ./data/$date.txt
python3 ./dataHandler.py 

