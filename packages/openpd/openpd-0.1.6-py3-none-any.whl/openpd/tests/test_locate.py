import numpy as np
from .. import isArrayEqual

from .. import findFirst, findAll, binarySearch

def test_findFirst():
    goal = [1, 2, 3, 4]
    assert findFirst(1, goal) == 0
    assert findFirst(3, goal) == 2
    assert findFirst(5, goal) == -1

    goal = np.array([1, 2, 3, 4, 5])
    assert findFirst(1, goal) == 0
    assert findFirst(3, goal) == 2
    assert findFirst(6, goal) == -1

def test_findAll():
    goal = [1, 1, 3, 2, 4]
    assert isArrayEqual(findAll(1, goal), [0, 1])
    assert findAll(5, goal) == []

    goal = np.array([1, 1, 3, 2, 4])
    assert isArrayEqual(findAll(1, goal), [0, 1])
    assert findAll(5, goal) == []

def test_binarySearch():
    goal = [1, 2, 3, 4, 5, 6, 7]
    assert binarySearch(1, goal) == 0
    assert binarySearch(7, goal) == 6
    assert binarySearch(3.5, goal) == 2 
    assert binarySearch(5.5, goal) == 4
    assert binarySearch(10, goal) == 6

    goal = np.array([1, 2, 3, 4, 5, 6, 7])
    assert binarySearch(1, goal) == 0
    assert binarySearch(7, goal) == 6
    assert binarySearch(3.5, goal) == 2 
    assert binarySearch(5.5, goal) == 4
    assert binarySearch(10, goal) == 6

    goal = list(range(100))
    assert binarySearch(5.5, goal) == 5
    assert binarySearch(1000, goal) == 99