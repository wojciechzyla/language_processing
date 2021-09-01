#!/usr/bin/python
# -*- coding: utf-8 -*-
from copy import deepcopy
from typing import List


class ListElement:
    def __init__(self, priority, data):
        self.priority = priority
        self.data = data

    def __eq__(self, other):
        if isinstance(other, ListElement):
            result = self.priority == other.priority
        else:
            result = False
        return result

    def __ne__(self, other):
        if isinstance(other, ListElement):
            result = self.priority != other.priority
        else:
            result = False
        return result

    def __lt__(self, other):
        if isinstance(other, ListElement):
            result = self.priority < other.priority
        else:
            result = False
        return result

    def __gt__(self, other):
        if isinstance(other, ListElement):
            result = self.priority > other.priority
        else:
            result = False
        return result

    def __le__(self, other):
        if isinstance(other, ListElement):
            result = self.priority <= other.priority
        else:
            result = False
        return result

    def __ge__(self, other):
        if isinstance(other, ListElement):
            result = self.priority >= other.priority
        else:
            result = False
        return result

    def __str__(self):
        return f"{self.priority}:{self.data}"


class HeapSort:
    def __init__(self):
        self.arr = []

    def is_empty(self):
        if len(self.arr) == 0:
            result = True
        else:
            result = False
        return result

    def peek(self):
        if len(self.arr) > 0:
            result = self.arr[0]
        else:
            result = None
        return result

    def heapify(self, lst: List[ListElement]):
        self.arr = deepcopy(lst)
        n = len(lst)
        for i in range((n-2)//2, -1, -1):
            root = i
            while 2*root+1 < n-1:
                child = 2*root+1
                if child+1 < n:
                    if self.arr[child+1] > self.arr[child]:
                        child += 1
                if self.arr[root] <= self.arr[child]:
                    self.arr[root], self.arr[child] = self.arr[child], self.arr[root]
                    root = child
                else:
                    break

    def dequeue(self):
        if self.is_empty():
            result = None
        else:
            self.arr[0], self.arr[-1] = self.arr[-1], self.arr[0]
            result = self.arr.pop()
            arr_length = len(self.arr)
            current = 0
            left = 1
            right = 2
            while left < arr_length:
                next_node = left
                if right < arr_length:
                    if self.arr[left] < self.arr[right]:
                        next_node = right
                if self.arr[current] < self.arr[next_node]:
                    self.arr[current], self.arr[next_node] = self.arr[next_node], self.arr[current]
                    left = 2 * next_node + 1
                    right = 2 * next_node + 2
                    current = next_node
                else:
                    break

        return result

    def sort(self, amount: int):
        sorted_lst = []
        i = 0
        while not self.is_empty() and i < amount:
            el = self.dequeue()
            sorted_lst.append(el.data)
            i += 1
        return sorted_lst
