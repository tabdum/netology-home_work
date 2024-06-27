class FlatIterator:
    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        res2 = []
        for i in self.list_of_list:
            for j in i:
                res2.append(j)
        if self.index + 1 > len(res2):
            raise StopIteration
        else:
            self.index += 1
            return res2[self.index - 1]
def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


if __name__ == '__main__':
    test_1()