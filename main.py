import numpy as np
from random import random
from copy import deepcopy

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
    def __init__(self, rotation = 0, translatement = [0,0]):
        self.rotation = rotation
        self.translatement = translatement
    
    def iter_oriented(self, identity):
        orientation = deepcopy(identity)
        orientation.rotate(self.rotation)
        orientation.translate(self.translatement)

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
            nodes are in some sense equivalent
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
        self.kite = []
        
    
    def get_dart_forces(self, l1, l2, l3):
        #1. Copy l1, l2, l3 into edges edges
        pass
    
    def get_kite_forces(self, l1, l2, l3):
        pass
    
    def grow(self,prob):
        pass
    
    def subdivide(self,max_dist):
        pass

    def differentiate(self):
        pass

    def update(self):
        pass