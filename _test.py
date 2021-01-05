import unittest
from main import Node, LinkedLine, Grid, Orientation, EdgeIdentity, OrganicPenrose
import numpy as np
from copy import deepcopy

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
    
    def test_translate(self):
        l = LinkedLine()
        l.add(0,0)
        l.add(1,0)
        l.translate([0,1])

        self.assertEqual(str(l), "(1,1) -> (0,1)")

        l.translate([-15,3])

        self.assertEqual(str(l), "(-14,4) -> (-15,4)")
    
    def test_rotate(self):
        l = LinkedLine()
        l.add(0,0)
        l.add(1,0)
        l.rotate(np.pi)

        self.assertAlmostEqual(l[0].pos[0],-1)     

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
            if nd.pos.tolist() == [1.5,1.5]:
                node1 = nd
                node2 = node1.next

        self.assertEqual(len(g.get_neighbourhood(node1)),8) #Middle tile, searching in 9 tiles excluding itself
        self.assertEqual(len(g.get_neighbourhood(node2)),5)

class TestOrientation(unittest.TestCase):
    def test_iter_oriented(self):
        l = LinkedLine()

        pos = [[0,0],[1,0],[1,1]]
        for p in pos:
            l.add(p[0],p[1])

        o = Orientation()
        for i,node in enumerate(o.iter_oriented(l)):
            a = pos[::-1][i]
            b = node.pos.tolist()

            self.assertAlmostEqual(a[0],b[0])
            self.assertAlmostEqual(a[1],b[1])

class TestEdgeIdentity(unittest.TestCase):
    def test___iter__(self):
        l = LinkedLine()
        l.add(0,0)
        l.add(1,0)

        ors_data = [[0,[0,0]],[np.pi,[1,1]],[0,[2,3]]]
        ors = [Orientation(*o) for o in ors_data]

        ei = EdgeIdentity(l,ors)
            
        for i,nodes in enumerate(ei):
            
            node1, node2, node3 = nodes

            #test node1
            self.assertAlmostEqual(node1.pos[0],l[i].pos[0])
            self.assertAlmostEqual(node1.pos[1],l[i].pos[1])

            #test node2
            l_copy = deepcopy(l)
            l_copy.rotate(ors_data[1][0])
            l_copy.translate(ors_data[1][1])
            self.assertAlmostEqual(node2.pos[0],l_copy[i].pos[0])

            #...

class TestOrganicPenrose(unittest.TestCase):
    def test_relax(self):
        pass
    

if __name__ == '__main__':
    unittest.main()