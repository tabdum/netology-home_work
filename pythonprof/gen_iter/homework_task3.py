class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.index = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        def liner(listt):
            res = []
            for elem in listt:
                if isinstance(elem, list):
                    res.extend(liner(elem))
                else:
                    res.append(elem)
            return res
        res_list = liner(self.list_of_list)
        if self.index + 1 > len(res_list):
            raise StopIteration
        else:
            self.index += 1
            return res_list[self.index - 1]


def test_3():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


if __name__ == '__main__':
    test_3()