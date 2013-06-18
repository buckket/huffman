#!/usr/bin/env python

import unittest
import huffman

from bitarray import bitarray


class Test(unittest.TestCase):

    def test_calculate_frequency(self):
        test_data = "aaabbc"
        test_result = {'a': 3, 'b': 2, 'c': 1}
        self.assertEqual(huffman.calculate_frequency(test_data), test_result)

    def test_create_nodes(self):
        test_data = {'a': 2, 'b': 1}
        test_result = [huffman.Node('a', 2), huffman.Node('b', 1)]
        self.assertEqual(huffman.create_nodes(test_data), test_result)

    def test_find_lowest(self):
        test_data = [huffman.Node('a', 3), huffman.Node('b', 2), huffman.Node('c', 1)]
        test_result = (huffman.Node('c', 1), huffman.Node('b', 2))
        self.assertEqual(huffman.find_lowest(test_data), test_result)

    def test_merge_nodes(self):
        n1 = huffman.Node('a', 1)
        n2 = huffman.Node('b', 2)
        test_result = huffman.Node(symbol=None, weight=3, left=n1, right=n2)
        self.assertEqual(huffman.merge_nodes(n1, n2), test_result)

    def test_create_tree(self):
        test_data = []
        test_data.append(huffman.Node('l', 1))
        test_data.append(huffman.Node('o', 2))
        test_data.append(huffman.Node('m', 1))
        test_result = huffman.Node(symbol=None, weight=4,
            left=huffman.Node('o', 2),
            right=huffman.Node(symbol=None, weight=2,
                left=huffman.Node('l', 1),
                right=huffman.Node('m', 1)
            )
        )
        self.assertEqual(huffman.create_tree(test_data), test_result)

    def test_create_codebook(self):
        test_data = huffman.Node(symbol=None, weight=4,
            left=huffman.Node('o', 2),
            right=huffman.Node(symbol=None, weight=2,
                left=huffman.Node('m', 1),
                right=huffman.Node('l', 1)
            )
        )
        test_result = ({'m': bitarray('01'), 'l': bitarray('00'), 'o': bitarray('1')}, [4, 2])
        self.assertEqual(huffman.create_codebook(test_data), test_result)


if __name__ == "__main__":
    unittest.main()

