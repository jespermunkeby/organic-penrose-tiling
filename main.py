import numpy as np
from random import random

class Node:
    def __init__(self, x, y):
        self.data = np.array([x,y])
        self.next = None
        self.prev = None
    
    def has_next(self):
        return self.next != None

    def dist_to_next(self):
        return np.linalg.norm(self.data - self.next.data)

    def __str__(self):
        return f"({self.data[0]},{self.data[1]})"
    

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

    def adaptive_subdivision(self, max_dist):
        for node in self:
            if node.has_next():
                while node.dist_to_next() > max_dist:
                    x, y =  ((node.data + node.next.data)/2).tolist()
                    new_node = Node(x,y)
                    new_node.next = node.next
                    new_node.prev = node
                    node.next = new_node


class Grid:
    def __init__(self, gridsize):
        self.gridsize = gridsize
        self.ht = {}
    
    def clear(self):
        self.ht = {}
    
    def hash_node(self,node):
        return tuple(np.floor(node.data // self.gridsize).tolist())
    
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