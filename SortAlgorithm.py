# some sort algorithm
import time


# Time the algorithm
def timeit(func):
    def wrapper(*args, **kwargs):
        print('The Algorithm %s Begins\n' % func.__name__)
        t_s = time.time()
        back = func(*args, **kwargs)
        t_e = time.time()
        print('\nThe Algorithm %s took %.8fs.' % (func.__name__, t_e - t_s))
        return back

    return wrapper


# Bubble Sort
@timeit
def BubbleSort(array):
    for i in range(len(array) - 1):
        for j in range(i + 1, len(array)):
            if array[i] > array[j]:
                array[i], array[j] = array[j], array[i]
        print('Current array is: %s' % array)

    return array


# Select Sort
@timeit
def SelectSort(array):
    for i in range(len(array) - 1):
        min = i
        for j in range(i + 1, len(array)):
            if array[j] < array[min]:
                min = j
        if min != i:
            array[i], array[min] = array[min], array[i]
        print('Current array is: %s' % array)

    return array


# Quick Sort
# @timeit
def QuickSort(array):
    if len(array) <= 1:
        return array

    return QuickSort([x for x in array[1:] if x < array[0]]) + \
           [array[0]] + \
           QuickSort([x for x in array[1:] if x > array[0]])


if __name__ == '__main__':
    array = [99, 88, 77, 66, 55, 44, 33, 22, 11, 0]
    array = BubbleSort(array)
    print('The sorted result is: %s\n\n' % array)

    array = [99, 88, 77, 66, 55, 44, 33, 22, 11, 0]
    array = SelectSort(array)
    print('The sorted result is: %s\n\n' % array)

    array = [99, 88, 77, 66, 55, 44, 33, 22, 11, 0]
    array = QuickSort(array)
    print('The sorted result is: %s\n\n' % array)
