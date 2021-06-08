#!/bin/zsh

# Clean up generated stuff that doesn't need to stick around

HERE=`pwd`
TOP=`dirname $HERE`

# clean up __pycache__ folders
find "$TOP" -type d -name __pycache__ -prune -exec rm -rf {} \;
