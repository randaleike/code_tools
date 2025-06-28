#!/bin/bash
python3 -m coverage run --include 'src/code_tools_grocsoftware/*' -m unittest discover -s tests/
python3 -m coverage report --fail-under=95
