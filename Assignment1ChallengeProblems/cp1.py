#Given two arrays, A and B, return the first element in A which is not in B.  
# If no such element exists, return the language's version of null. 
# Your function must run with an Average case time complexity of O(n), 
# where n is the maximum size of A and B.  Other complexities with receive partial credit


def first_element(a, b):
    myset = set(b)
    for i in a:
        if i not in myset:
            return i 

