#!/usr/bin/env python


'''
    huffman.py
    ~~~~~~~~~~

    (C) 2013 buckket

    This program is free software. It comes without any warranty, to
    the extent permitted by applicable law. You can redistribute it
    and/or modify it under the terms of the Do What The Fuck You Want
    To Public License, Version 2, as published by Sam Hocevar. See
    http://sam.zoy.org/wtfpl/COPYING for more details.
'''


import sys
import math
import pydot

from collections import defaultdict
from bitarray import bitarray


class Node(object):

    def __init__(self, symbol, weight=0, left=None, right=None):
        self.symbol = symbol
        self.weight = weight
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "<Node symbol:%s weight:%s left:%s right:%s>" % (self.symbol, self.weight, self.left, self.right)


def calculate_frequency(data):
    symbols = defaultdict(int)
    for b in data:
        symbols[b] += 1
    return symbols

def create_nodes(symbols):
    elements = []
    for symbol, weight in symbols.items():
        elements.append(Node(symbol=symbol, weight=weight))
    return elements

def find_lowest(elements):
    n1 = Node(symbol=None, weight=sys.maxint)
    n2 = Node(symbol=None, weight=sys.maxint)
    for element in elements:
        if element.weight < n1.weight:
            if n1.weight < n2.weight:
                n2 = n1
            n1 = element
        elif element.weight < n2.weight:
            n2 = element
    return (n1, n2)

def merge_nodes(n1, n2):
    weight = n1.weight + n2.weight
    return Node(symbol=None, weight=weight, left=n1, right=n2)

def create_tree(nodes):
    while len(nodes) >= 2:
        (n1, n2) = find_lowest(nodes)
        m = merge_nodes(n1, n2)
        nodes.append(m)
        nodes.remove(n1)
        nodes.remove(n2)
    return nodes[0]

def create_codebook(root):
    codebook = {}
    weights = []

    def walk_tree(node, input):
        left = right = input
        if node.left is None and node.right is None:
            codebook[node.symbol] = input
        else:
            left = left + '1'
            right = right + '0'
            weights.append(node.weight)
            walk_tree(node.left, left)
            walk_tree(node.right, right)

    walk_tree(root, bitarray())
    return (codebook, weights)

def create_graph(root):
    graph = pydot.Dot(graph_type='digraph')
    graph.set_node_defaults(fontname='helvetica')
    graph.set_edge_defaults(fontname='helvetica', color='blue')

    def walk_tree(node, input):
        left = right = input
        name = 'root' if not input else ''.join(['root', str(input.to01())])

        if node.left is None and node.right is None:
            graph.add_node(pydot.Node(name, shape='record', label="{{'%s'|%s}|%s}" % (node.symbol, node.weight, input.to01())))
            graph.add_edge(pydot.Edge(name[:-1], name, label=name[-1:]))

        else:
            graph.add_node(pydot.Node(name, label=node.weight))
            if name != 'root':
                graph.add_edge(pydot.Edge(name[:-1], name, label=name[-1:]))
            left = left + '1'
            right = right + '0'
            walk_tree(node.left, left)
            walk_tree(node.right, right)

    walk_tree(root, bitarray())
    graph.write_png('tree.png')

def print_output(string, codebook, weights):
    print ''
    print 'huffman.py'
    print '~~~~~~~~~~'
    data = str()
    sys.stdout.write('Symbols: '.ljust(10))
    for c in string:
        sys.stdout.write(" %s " % c.ljust(8))
    sys.stdout.write("|| %s Chars\n" % len(string))
    sys.stdout.write('Binary: '.ljust(10))
    lenght = 0
    for c in string:
        lenght += len(str(bin(ord(c)))[2:].zfill(8))
        sys.stdout.write(" %s " % str(bin(ord(c)))[2:].zfill(8))
    sys.stdout.write("|| %s Bits\n" % lenght)
    sys.stdout.write('Encoded: '.ljust(10))
    lenght = 0
    for c in string:
        lenght += len(codebook[c].to01())
        data = data + codebook[c].to01()
        sys.stdout.write(" %s " % codebook[c].to01().ljust(8))
    sys.stdout.write("|| %s Bits\n" % lenght)
    print ''
    print "%0.2f bits per symbol when using naive encoding" % (math.log(len(codebook), 2))
    print "%0.2f bits per symbol when using huffman encoding" % (float(sum(weights)) / float(len(string)))
    print ''


if __name__ == '__main__':
    string = "Hallo Welt"

    symbols = calculate_frequency(string)
    nodes = create_nodes(symbols)
    root = create_tree(nodes)
    (codebook, weights) = create_codebook(root)

    create_graph(root)
    print_output(string, codebook, weights)
