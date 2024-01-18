class KaryTreeNode:
    def __init__(self, value, children=[]):
        self.value = value
        self.children = children

def kary_avg_value(root):
    if not root:
        return None

    total_sum = 0
    total_count = 0

    queue = [root]

    while queue:
        node = queue.pop(0)
        total_sum += node.value
        total_count += 1

        for child in node.children:
            queue.append(child)

    return total_sum / total_count if total_count > 0 else 0


