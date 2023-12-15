#!/bin/bash

# Check if the input is provided
if [ $# -eq 0 ]; then
    echo "Please provide a single integer as input."
    exit 1
fi

# Check if the input is a valid integer
if ! [[ $1 =~ ^[0-9]+$ ]]; then
    echo "Invalid input. Please provide a single integer."
    exit 1
fi

# Check if the input is within the valid range
if (( $1 < 1 || $1 > 25 )); then
    echo "Input should be between 1 and 25 (inclusive)."
    exit 1
fi

# Create the files
day_file="day_$1.py"
data_file="data/day_$1.txt"
test_file="data/day_$1_test.txt"

# If any files already exist cancel script
if [ -f "$day_file" ] || [ -f "$data_file" ] || [ -f "$test_file" ]; then
    echo "Files already exist. Please delete them before running this script."
    exit 1
fi

touch "$day_file"
mkdir -p "data"
touch "$data_file"
touch "$test_file"

echo "Files created successfully."
