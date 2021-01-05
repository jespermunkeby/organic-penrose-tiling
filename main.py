import numpy as np
from random import random
from copy import deepcopy
import matplotlib.pyplot as plt
from lloyd import Field

class Node:
    def __init__(self, x, y):
        self.pos = np.array([x,y])
        self.next = None
        self.prev = None
    
    def has_next(self):
        return self.next != None

    def dist_to_next(self):
        return np.linalg.norm(self.pos - self.next.pos)

    def __str__(self):
        return f"({self.pos[0]},{self.pos[1]})"
    

class LinkedLine:
    def __init__(self):
        self.head = None     

    def add( self, x,y ) :
        node = Node(x,y)
        if self.head == None :    
            self.head = node
        else :
            node.next = self.head
            node.next.prev = node                        
            self.head = node                

    def __str__( self ) :
        s = ""
        p = self.head
        if p != None :        
            while p.next != None :
                s += f"{p} -> "
                p = p.next
            s += f"{p}"
        return s

    def __iter__(self):
        node = self.head
        while node != None:
            yield node
            node = node.next
    
    def __getitem__(self, n):       
        return next(x for i,x in enumerate(self) if i==n)

    def adaptive_subdivision(self, max_dist):
        for node in self:
            if node.has_next():
                while node.dist_to_next() > max_dist:
                    x, y =  ((node.pos + node.next.pos)/2).tolist()
                    new_node = Node(x,y)
                    new_node.next = node.next
                    new_node.prev = node
                    node.next = new_node
    
    def translate(self, vec):
        for node in self:
            node.pos += vec
    
    def rotate(self, theta):
        c, s = np.cos(theta), np.sin(theta)
        rotmat = np.array(((c, -s), (s, c)))
        for node in self:
            node.pos = np.matmul(rotmat, node.pos)
        

class Grid:
    def __init__(self, gridsize):
        self.gridsize = gridsize
        self.ht = {}
    
    def clear(self):
        self.ht = {}
    
    def hash_node(self,node):
        return tuple(np.floor(node.pos // self.gridsize).tolist())
    
    def insert_line(self,line):
        for node in line:
            hsh = self.hash_node(node)
            if hsh in self.ht:
                self.ht[hsh].append(node)
            else:
                self.ht[hsh] = [node]
        
    def get_neighbourhood(self,node):
        hsh = self.hash_node(node)
        neighbours = []
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                neigh_hsh = (hsh[0]+dx,hsh[1]+dy)
                if neigh_hsh in self.ht:
                    neighbours.extend(self.ht[neigh_hsh])
        return [n for n in neighbours if n!=node]
    
    def __iter__(self):
        for key in self.ht:
            yield (key,self.ht[key])
    
    def __str__(self):
        s = ""
        for key, val in self:
            s += f"{key}: {val} \n"
        return s

class Orientation:
    def __init__(self, rotation = 0, translate = [0,0]):
        self.rotation = rotation
        self.translate = translate
    
    def iter_oriented(self, identity):
        orientation = deepcopy(identity)
        orientation.rotate(self.rotation)
        orientation.translate(self.translate)

        for node in orientation:
            yield node


class EdgeIdentity: #Line along with its orientations
    def __init__(self, identity, orientations):
        self.identity = identity
        self.orientations = orientations
    
    def __iter__(self):
        """
            Iterates through oriented copies of identity.
            Multipresent nodes are returned in a list, in which all
            nodes are equivalent
        """
        l = []
        for ori in self.orientations:
            nodes = []
            for node in ori.iter_oriented(self.identity):
                nodes.append(node)
            l.append(nodes)
            
        for nodes in zip(*l):
            yield nodes
        

class OrganicPenrose:
    def __init__(self):
        e1 = LinkedLine()
        e1.add(1,0)
        e1.add(0,0)

        phi = (1 + 5 ** 0.5) / 2

        e2 = LinkedLine()
        e2.add(1/phi,0)
        e2.add(0,0)

        e3 = LinkedLine()
        e3.add(1/phi,0)
        e3.add(0,0)

        self.edges = [e1,e2,e3]

        #Kite
        kite_e1_ors = [
            Orientation(rotation=np.deg2rad(180-36),translate=[1,0]),
            Orientation(rotation=np.deg2rad(180+36),translate=[1,0])
            ]

        kite_e2_ors = [
            Orientation(rotation=np.deg2rad(72) ),
            ]

        kite_e3_ors = [
            Orientation(rotation=np.deg2rad(-72) ),
            ]
        
        self.kite = [
            EdgeIdentity(e1, kite_e1_ors),
            EdgeIdentity(e2, kite_e2_ors),
            EdgeIdentity(e3, kite_e3_ors)
            ]

        #Probably right
        pos1 = [np.cos(np.deg2rad(72)), np.sin(np.deg2rad(36))]
        pos2 = [np.cos(np.deg2rad(72)), -np.sin(np.deg2rad(36))]

        dart_e1_ors = [
            Orientation(rotation=np.deg2rad(180+36),translate=pos1),
            Orientation(rotation=np.deg2rad(180-36),translate=pos2)
            ]

        dart_e2_ors = [
            Orientation(rotation=np.deg2rad(180+72),translate=pos1),
            ]

        dart_e3_ors = [
            Orientation(rotation=np.deg2rad(180-72),translate=pos2),
            ]
        
        self.dart = [
            EdgeIdentity(e1, dart_e1_ors),
            EdgeIdentity(e2, dart_e2_ors),
            EdgeIdentity(e3, dart_e3_ors)
            ]
    
    def view(self):
        for eid in self.kite:
            coors = [[] for _ in range(len(eid.orientations))]
            for nodes in eid:
                for i,n in enumerate(nodes):
                    coors[i].append(n.pos.tolist())
            for coo_list in coors:
                xs = []
                ys = []
                for coo in coo_list:
                    xs.append(coo[0])
                    ys.append(coo[1])
                plt.plot(xs,ys)
                plt.scatter(xs,ys)
        plt.show()

        for eid in self.dart:
            coors = [[] for _ in range(len(eid.orientations))]
            for nodes in eid:
                for i,n in enumerate(nodes):
                    coors[i].append(n.pos.tolist())
            for coo_list in coors:
                xs = []
                ys = []
                for coo in coo_list:
                    xs.append(coo[0])
                    ys.append(coo[1])
                plt.plot(xs,ys)
                plt.scatter(xs,ys)
        plt.show()