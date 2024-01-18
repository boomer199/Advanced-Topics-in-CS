def check_anagram(str1, str2):
    str1_lower = str1.lower()
    str2_lower = str2.lower()

    char1_freq = {}
    char2_freq = {}
    
    for char in str1_lower:
        char1_freq[char] = char1_freq.get(char, 0) + 1 
        
    for char in str2_lower:
        char2_freq[char] = char2_freq.get(char, 0) + 1 
        
    return char1_freq == char2_freq

