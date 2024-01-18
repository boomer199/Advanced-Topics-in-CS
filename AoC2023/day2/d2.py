import os
import re
from math import prod 

script_dir = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(script_dir, "input.txt")


def runPart1(filename):    
    lines = open(filename).read().splitlines()
    ans = 0
    for line in lines:
        id = int(re.findall(r'Game (\d+):', line)[0])
        if all([int(match)<=limit for color, limit in[("red",12),("green", 13),("blue",14)] for match in re.findall(rf'(\d+) {color}',line)]):
            ans += id
    return ans

def runPart2(filename):
    lines = open(filename).read().splitlines() 
    ans = 0 
    for line in lines: 
        ans += prod(max(int(match)for match in re.findall(rf'(\d+) {color}',line)) for color in["red", "green", "blue"]) 
    return ans

print(runPart1(file))
print(runPart2(file))