import heapq

class Item:
    def __init__(self, name, ranks):
        self.name = name
        self.ranks = ranks

    def __repr__(self):
        return f"{self.name}: {self.ranks}"

class PriorityArray:
    def __init__(self, item):
        self.item = item

    def __lt__(self, other):
        for a, b in zip(self.item.ranks, other.item.ranks):
            if a > b:
                return True
            elif a < b:
                return False
        return False  # They are equal

    def __repr__(self):
        return repr(self.item)

# Max-Heap implementation
class MaxHeap:
    def __init__(self):
        self.heap = []
        self.item_map = {}  # To keep track of items by their name

    def push(self, item):
        if item.name in self.item_map:
            # Update the ranks of the existing item
            existing_item = self.item_map[item.name]
            existing_item.ranks = item.ranks
            # Rebuild the heap to maintain the heap property
            heapq.heapify(self.heap)
        else:
            # Add new item to the heap and map
            heapq.heappush(self.heap, PriorityArray(item))
            self.item_map[item.name] = item

    def pop(self):
        priority_item = heapq.heappop(self.heap)
        # Remove item from the map
        del self.item_map[priority_item.item.name]
        return priority_item.item

    def peek(self):
        return self.heap[0].item if self.heap else None

    def increment_rank(self, name, position, array_size):
        if name in self.item_map:
            # Update the rank at the specified position
            item = self.item_map[name]
            item.ranks[position] += 1
        else:
            # Create a new item with ranks initialized to 0
            ranks = [0] * array_size
            ranks[position] += 1
            item = Item(name, ranks)
            self.push(item)
        
        # Rebuild the heap to maintain the heap property
        heapq.heapify(self.heap)

    def __len__(self):
        return len(self.heap)

# Example usage
