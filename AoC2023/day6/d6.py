import math
from datetime import datetime
start = datetime.now()


# Open the input file and read its content
with open("AoC2023/day6/d6input.txt") as f: # ty to big man lucas for getting this to work so i dont need OS import
    lines  = f.readlines()

times = lines[0].split(": ")[1].strip().split()
times = [int(t) for t in times]
distances = lines[1].split(": ")[1].strip().split()
distances = [int(d) for d in distances]

def ways_to_win(time, record_distance):
    ways = 0
    for i in range(time):
        speed = i
        time_remaining = time - i
        distance = speed * time_remaining
        if distance > record_distance:
            ways += 1
    return ways

total_ways = [ways_to_win(t, d) for t, d in zip(times, distances)]

print(f"Part 1: {math.prod(total_ways)}")

time = int("".join([str(t) for t in times]))
distance = int("".join([str(d) for d in distances]))

print(f"Part 2: {ways_to_win(time, distance)}")

print(datetime.now() - start)