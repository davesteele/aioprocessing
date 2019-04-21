#!/bin/sh

python3 setup.py test 2>&1 > /dev/null

python3 -m pytest tests/
