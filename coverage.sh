#!/bin/bash
python3-coverage run --source=CAS run_tests.py
python3-coverage html
xdg-open htmlcov/index.html
