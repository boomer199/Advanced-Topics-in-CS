import os
from datetime import datetime

start = datetime.now()
 
def get_input_file_path():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(script_directory, "d4input.txt")
    return input_file_path

def part1(lines):
    total_points = 0

    for line in lines:
        winning, mycards = map(str.split, line.split('|'))

        # Find common elements between the sets
        common_elements = set(winning) & set(mycards)

        # Calculate points based on the number of common elements
        points = 1 if common_elements else 0

        # Accumulate points using a power of 2 formula
        for _ in range(len(common_elements) - 1):
            points *= 2

        total_points += points

    return total_points

def part2(lines):
    # Initialize a list to keep track of the number of ways to choose each set
    ways_to_choose_sets = [1] * len(lines)
    for i, line in enumerate(lines):
        winning, mycards = map(str.split, line.split('|'))

        # Count the number of common elements between the sets
        winning_count = len(set(winning) & set(mycards))
        for j in range(i + 1, min(i + 1 + winning_count, len(lines))):
            ways_to_choose_sets[j] += ways_to_choose_sets[i]

    # Return the sum of all elements in the list, representing the total ways to choose sets
    return sum(ways_to_choose_sets)

if __name__ == "__main__":
    input_file_path = get_input_file_path()
    with open(input_file_path, 'r') as file:
        input_lines = file.readlines()

    total_points_part1 = part1(input_lines)
    print("Part 1:", total_points_part1)

    total_ways_to_choose_sets_part2 = part2(input_lines)
    print("Part 2:", total_ways_to_choose_sets_part2)

print(datetime.now() - start)