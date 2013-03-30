#!/bin/bash
cd `dirname $0`
python -m unittest discover -p '*_test.py'