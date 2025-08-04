#!/bin/bash
pylint -d duplicate-code tests/ $(git ls-files '*.py')