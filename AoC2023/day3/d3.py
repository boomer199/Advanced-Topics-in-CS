import os
from collections import defaultdict

# Get the directory of the script and create the path for the input file
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "input.txt")

# Read the lines from the input file
with open(file_path) as file:
    lines = file.read().splitlines()

# Part 1: Sum the numbers around each digit in the grid
part1_sum = 0
current_num_str = ''

for row, line in enumerate(lines):
    line += '.'  # Adding a period to handle the last digit in the line
    for col, char in enumerate(line):
        if char.isdigit():
            current_num_str += char
        elif current_num_str:
            # Check the surrounding cells for digits and dots
            if any(lines[row1][col1] not in '.0123456789' for row1 in range(max(0, row - 1), min(len(lines), row + 2))
                   for col1 in range(max(0, col - 1 - len(current_num_str)), min(len(line) - 1, col + 1))):
                part1_sum += int(current_num_str)
            current_num_str = ''

print("Part 1:", part1_sum)

# Part 2: Create a defaultdict to store pairs of numbers around each '*'
coordinate_dict = defaultdict(list)
current_num_str = ''

for row, line in enumerate(lines):
    line += '.'  # Adding a period to handle the last digit in the line
    for col, char in enumerate(line):
        if char.isdigit():
            current_num_str += char
        elif current_num_str:
            # Check for '*' in the surrounding cells
            for row1 in range(max(0, row - 1), min(len(lines), row + 2)):
                for col1 in range(max(0, col - 1 - len(current_num_str)), min(len(line) - 1, col + 1)):
                    if lines[row1][col1] == '*':
                        coordinate_dict[row1, col1].append(int(current_num_str))
            current_num_str = ''

# Part 2: Sum the products of pairs of numbers around each '*'
part2_sum = sum(ab[0] * ab[1] for ab in coordinate_dict.values() if len(ab) == 2)
print("Part 2:", part2_sum)
