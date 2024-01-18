
def calculate_calibration_sum(lines):
    total = 0
    for line in lines:
        line = line.replace("one", "o1e")
        line = line.replace("two", "t2o")
        line = line.replace("three", "t3e")
        line = line.replace("four", "f4r")
        line = line.replace("five", "f5e")
        line = line.replace("six", "s6x")
        line = line.replace("seven", "s7n")
        line = line.replace("eight", "e8t")
        line = line.replace("nine", "n9e")
        save = []
        for char in line:
            if char.isdigit():
                save.append(char)
        if len(save) > 1:
            total += int(save[0] + save[-1])
        else:
            total += int(save[0] + save[0])
    return total


def read_lines_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

# Read lines from the file
file_lines = read_lines_from_file("test.txt")

# Calculate calibration sum
result = calculate_calibration_sum(file_lines)

# Print the result
print(result)