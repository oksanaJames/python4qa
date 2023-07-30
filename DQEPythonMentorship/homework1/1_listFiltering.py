# encoding=utf-8


# Create function which filter only integer elements from list
# should be 3 versions of code for:
# 1) for loop
# 2) list comprehension
# 3) filter() + lambda

l = [1, 2, '3', 4, None, 10, 33, 'Python', -37.5]


# 1) for loop
def filtering_for(inputList):
    outputList = []
    for item in inputList:
        if isinstance(item, int):
            outputList.append(item)
    return outputList


# 2) list comprehension
def list_comprehension(inputList):
    inputList = [it for it in inputList if isinstance(it, int)]
    return inputList


# 3) filter() + lambda
def filter_lambda(inputList):
    inputList = list(filter(lambda x: isinstance(x, int), inputList))
    return inputList


if __name__ == '__main__':
    print("Input list: {}".format(l))
    print("--------------------------")
    print("Filtered input with 'for' loop: {}".format(filtering_for(l)))
    print("--------------------------")
    print("Filtered input with 'list comprehension': {}".format(list_comprehension(l)))
    print("--------------------------")
    print("Filtered input with 'filter() + lambda': {}".format(filter_lambda(l)))
