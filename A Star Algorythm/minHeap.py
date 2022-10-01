from heapq import heappush, heappop, heapify


class BinaryHeap:
    def __init__(self):
        self.heap = []
        self.idx = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.idx += 1
        if self.idx >= len(self.heap):
            self.idx = -1
            raise StopIteration
        else:
            return self.heap[self.idx]

    def __str__(self):
        return self.heap

    def isEmpty(self):
        return len(self.heap) == 0

    def parent(self, idx):
        return (idx-1)/2

    def insert(self, key):
        heappush(self.heap, key)

    def decreaseKey(self, idx, new_val):
        self.heap[idx] = new_val
        while idx != 0 and self.heap[self.parent(idx)] > self.heap[idx]:
            self.heap[idx], self.heap[self.parent(idx)] = (self.heap[self.parent(idx)], self.heap[idx])

    def extractMin(self):
        return heappop(self.heap)

    def deleteKey(self, idx):
        self.decreaseKey(idx, float("-inf"))
        self.extractMin()

    def getMin(self):
        return self.heap[0]


