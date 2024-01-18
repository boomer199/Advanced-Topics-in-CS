class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

def remove_duplicates(head):
    
    sorting = dict()
    non_dupes = []
    
    current = head
    while current:
        sorting[current.value] = sorting.get(current.value, 0) + 1 
        current = current.next
    
    for key in sorting.keys():
        if sorting.get(key) == 1:
            non_dupes.append(key)
    
    return non_dupes

