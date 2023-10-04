"""Алгоритмы сортировки"""

def bubble_sort(a: list) -> list:
    """Сортировка пузырьком
    - Устойчивая
    - Время: O(n²)
    - Память: O(1)
    """
    n = len(a)
    swapped = False
    for i in range(n - 1):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True         
        if not swapped:
            return a
    return a


def selection_sort(a: list) -> list:
    """Сортировка выбором
    - Неустойчивая
    - Время: O(n²)
    - Память: O(1)
    """
    n = len(a)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if a[j] < a[min_index]:
                min_index = j
        a[i], a[min_index] = a[min_index], a[i]
    return a


def insertion_sort(a: list) -> list:
    """Сортировка вставками
    - Устойчивая
    - Время: O(n²)
    - Память: O(1)
    """
    n = len(a)
    for i in range(1, n):
        j = i - 1
        while j >= 0 and a[i] < a[j]:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = a[i]
    return a


def _partition(a: list, low: int, high: int) -> int:
    pivot = a[high]
    i = low - 1
    for j in range(low, high):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[high] = a[high], a[i + 1]
    return i + 1


def quickSort(a: list, low: int = None, high: int = None) -> list:
    if low is None:
        low = 0
    if high is None:
        high = len(a) - 1
    if low < high:
        p = _partition(a, low, high)
        quickSort(a, low, p - 1)
        quickSort(a, p + 1, high)
    return a
