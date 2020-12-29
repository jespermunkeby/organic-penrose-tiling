import unittest
from main import Node, LinkedLine, Grid
import numpy as np

class TestLinkedLine(unittest.TestCase):
    def test_adaptive_subdivision(self):
        l = LinkedLine()
        l.add(0,0)
        l.add(1,0)

        self.assertEqual(str(l), "(1,0) -> (0,0)")

        l.adaptive_subdivision(0.25)

        self.assertEqual(str(l), "(1,0) -> (0.75,0.0) -> (0.5,0.0) -> (0.25,0.0) -> (0,0)")

        l.adaptive_subdivision(0.25)

        self.assertEqual(str(l), "(1,0) -> (0.75,0.0) -> (0.5,0.0) -> (0.25,0.0) -> (0,0)")

        l.adaptive_subdivision(0.24)

        self.assertEqual(sum([1 for each in l]), 9)

class TestGrid(unittest.TestCase):
    def test_insert_line(self):
        l = LinkedLine()
        l.add(0,0)
        l.add(1,0)

        g = Grid(0.1)
        g.insert_line(l)

        self.assertTrue(((0,0) and (9,0)) in [e for e in g.ht.keys()])

        g.clear()
        l = LinkedLine()

        for i in range(20):
            for j in range(20):
                l.add(i,j)
        
        g.insert_line(l)

        for node in l:
            self.assertTrue(node in g.ht[g.hash_node(node)])

    def test_get_neighbourhood(self):
        l = LinkedLine()

        for i in range(3):
            for j in range(3):
                l.add(i+0.5,j+0.5)
        
        g = Grid(1)
        g.insert_line(l) 
        
        node1 = None
        node2 = None
        for nd in l:
            if nd.data.tolist() == [1.5,1.5]:
                node1 = nd
                node2 = node1.next

        self.assertEqual(len(g.get_neighbourhood(node1)),8) #Middle tile, searching in 9 tiles excluding itself
        self.assertEqual(len(g.get_neighbourhood(node2)),5)
    

if __name__ == '__main__':
    unittest.main()