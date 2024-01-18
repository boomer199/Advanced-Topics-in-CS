# Given, a String A, return all letters which occur the most often.  
# Ignore case, and if there is no letter return an empty list. 
# The function must run in an Average time complexity of O( n ) 
# where n is the size of A. Other complexities with receive partial credit.

def most_letters(str):
    if len(str) == 0:
        return []
    
    str_lower = str.lower()
    char_freq = {}
    
    for char in str_lower:
        char_freq[char] = char_freq.get(char, 0) + 1
    
    most_freq_counter = 0 
    most_freq_char = []
    
    maxValue = max(char_freq.values())
    for key in char_freq.keys():
        if char_freq.get(key) == maxValue:
            most_freq_char.append(key)
    
    return(most_freq_char)


            
