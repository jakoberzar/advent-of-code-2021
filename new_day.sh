#!/usr/bin/env bash
# Strict mode
set -euo pipefail
IFS=$'\n\t'

# Variables
DAY_NAME=$1
INPUT_DAY_FOLDER="inputs/day-$DAY_NAME"
PYTHON_FOLDER="python"

# Make input files
mkdir "$INPUT_DAY_FOLDER"
touch "$INPUT_DAY_FOLDER/simple.txt"
touch "$INPUT_DAY_FOLDER/full.txt"
echo "Input files created"

# Make Python files
cp "$PYTHON_FOLDER/day-boilerplate.py" "$PYTHON_FOLDER/day$DAY_NAME.py"
echo "Python files created"
