#!/bin/bash

# check for build files
if [ -d "./dist" ]
then
    # Clean dist
    echo "Remove dist"
    rm -rf ./dist
fi
if [ -d "./code_tools_grocsoftware.egg-info" ]
then
    # Clean egg-info
    echo "Remove .egg-info"
    rm -rf ./code_tools_grocsoftware.egg-info
fi
if [ -d "./doc" ]
then
    # Clean doc files
    echo "Remove documantation"
    rm -rf ./doc
fi
