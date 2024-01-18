from datetime import datetime
start = datetime.now()


# Open the input file and read its content
with open("AoC2023/day5/d5input.txt") as f: # ty to big man lucas for getting this to work so i dont need OS import
    content = f.readlines()

# Extract the seeds from the file content
trash, rest = content[0].split(":") # haha trash go bye!
seeds = rest.split()

# Create a dictionary to store mappings between different stages
maps = {}

# Initialize variables for reading maps
read_map = True
map_type = ""

# Iterate through the content starting from index 2
for v1 in content[2:]:
    # Check for the end of a map section
    if v1 == "\n":
        read_map = True
        continue

    # If reading a map, store the map type and initialize an empty list
    if read_map:
        map_type = v1.strip()[:-5]
        maps[map_type] = []
        read_map = False
        continue

    # Parse the destination, source, and count from the current line
    dest, source, count = v1.strip().split()
    dest = int(dest) # cast from str to int (took wayyyy too long lol i got so many errors)
    source = int(source)
    count = int(count)
    maps[map_type].append([dest, source, count])

lowest_location = None

# Function to get the value from a map based on a given name and input value
def get_from_map(map_name, value):
    working_map = maps[map_name]
    for entry in working_map:
        dest, source, count = entry
        if source <= value < source + count:
            return dest + (value - source)
    return value

# Process each seed and track the transformation stages
for seed in seeds:
    seed = int(seed)
    soil = get_from_map('seed-to-soil', seed)
    fertilizer = get_from_map('soil-to-fertilizer', soil)
    water = get_from_map('fertilizer-to-water', fertilizer)
    light = get_from_map('water-to-light', water)
    temperature = get_from_map('light-to-temperature', light)
    humidity = get_from_map('temperature-to-humidity', temperature)
    location = get_from_map('humidity-to-location', humidity)
    
    # Update the lowest_location if it's None or the current location is lower
    if lowest_location is None or location < lowest_location:
        lowest_location = location

# Print the lowest_location obtained from the seeds
print(lowest_location)
print(datetime.now() - start)