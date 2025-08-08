#!/bin/bash
clear
coverage run -m pytest -s
coverage report -m --fail-under=98
