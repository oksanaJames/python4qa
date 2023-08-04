# encoding=utf-8


"""Create function which filter only integer elements from list should be 3 versions of code for:
1) for loop
2) list comprehension
3) filter() + lambda
"""

mixed_elements = [1, 2, '3', 4, None, 10, 33, 'Python', -37.5]


def filter_with_for(input_file):
    # Filtering with for loop
    filtered_elements = []
    for item in input_file:
        if isinstance(item, int):
            filtered_elements.append(item)
    return filtered_elements


def filter_with_list_comprehension(input_file):
    # Filtering with list comprehension
    input_file = [item for item in input_file if isinstance(item, int)]
    return input_file


def filter_with_lambda(input_file):
    # Filtering with filter() + lambda
    input_file = list(filter(lambda x: isinstance(x, int), input_file))
    return input_file


if __name__ == '__main__':
    print("Input list: {}".format(mixed_elements))
    print("--------------------------")
    print("Filtered input with 'for' loop: {}".format(filter_with_for(mixed_elements)))
    print("--------------------------")
    print("Filtered input with 'list comprehension': {}".format(filter_with_list_comprehension(mixed_elements)))
    print("--------------------------")
    print("Filtered input with 'filter() + lambda': {}".format(filter_with_lambda(mixed_elements)))
