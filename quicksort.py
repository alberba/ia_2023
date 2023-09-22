def quicksort(array: list) -> list:
    less = list()
    equal = list()
    greater = list()

    if len(array) > 1:
        pivot = array[-1]
        for x in array:
            if x < pivot:
                less.append(x)
            elif x == pivot:
                equal.append(x)
            else:
                greater.append(x)
        quicksort(less)
        quicksort(greater)
        array = less + equal + greater
    return array