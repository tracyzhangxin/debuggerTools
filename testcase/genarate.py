from random import randint


def generate():
    n = randint(1, 100)
    alist = []
    for i in range(n):
        alist.append(randint(1,100))
    return alist


# bubblesort
def bubble_sort(alist):
    length = len(alist)

    for i in range(0, length - 1):

        for j in range(i + 1, length):

            if alist[i] > alist[j]:
                alist[i], alist[j] = alist[j], alist[i]

    return alist


def bubbleSort(arr):
    n = len(arr)

    # 遍历所有数组元素
    for i in range(n):

        # Last i elements are already in place
        for j in range(0, n - i - 1):

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def store(filename, i):
    file = open(filename, "w")
    select = randint(0, 1)
    if select == 0:
        alist = generate()
    else:
        alist = bubbleSort(generate())
        print(i)
    file.write(str(len(alist)) + "\n")
    for a in alist:
        file.write(str(a) + "\n")
    file.close()


def main():
    for i in range(1, 101):
        filename = "./sort/" + str(i) + ".in"
        store(filename, i)


if __name__ == '__main__':
    main()
