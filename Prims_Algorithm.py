"""Author - Anantvir Singh, concept reference:= CLRS"""

# Prims Implementation using Min Priority Queue(Binary Min Heap) - which always gives minimum value

# --------------------------- Adjaceny Map Representation of a Graph ----------------------------------------
import math
class Vertex:
    def __init__(self,x,parent = None,key = None):
        self._element = x
        self._parent = parent
        self._key = key
    
    def element(self):
        return self._element
    
    def __hash__(self):
        return hash(id(self))       # Hash function created so that a vertex can be used as a key in a dict or set as dict keys need to be hashable objects !

class Edge:
    def __init__(self,u,v,x):
        self._origin = u
        self._destination = v
        self._element = x
    
    def endpoints(self):                    # return (u,v) tuple for end points of this edge
        return (self._origin,self._destination)
    
    def opposite(self,v):                   # return vertex opposite to the given vertex v
        return self._origin if v is self._destination else self._origin
    
    def element(self):                      # Return value associated with this edge
        return self._element
    
    def __hash__(self):                     # Make edge hashable so that it can be used as key of a map/set
        return hash((self._origin,self._destination))

class Graph:
    
    def __init__(self,directed = False):
        self._outgoing = {}                 # map to hold vertices as keys and their incidence collection dict as value
                                            # i.e _outgoing = {u: {v : e},v: {u : e,w : f}   --> vertex u is attached to vertex v via edge e, similarly vertex 'w' is attached to vertex 'v' via edge 'f'
        self._incoming = {} if directed == True else self._outgoing     # create another map called '_incoming' only if 'directed' is True else, just refer to _outgoing for undirected graphs

    def is_directed(self):
        return self._outgoing is not self._incoming         # if both _outgoing and _incoming maps are different, then it is a directed graph. 

    def vertex_count(self):
        return len(self._outgoing)
    
    def vertices(self):
        return self._outgoing.keys()                        # returns vertices of graph as a python list []

    def edge_count(self):
        edges = set()
        for eachDict in self._outgoing.values():
            edges.add(eachDict.values())
        return len(edges)
    
    def get_edge(self,u,v):
        return self._outgoing[u].get(v)                     # get(v) used because it returns None if v is not present in self._outgoing[u]. If we use self._outgoing[u][v], then it will give KeyError if v is not in self._outgoing[u]

    def degree(self,v,outgoing = True):
        dic = self._outgoing if outgoing else self._incoming
        return len(dic[v])
    
    def incident_edges(self,v,outgoing = True):
        dic = self._outgoing if outgoing else self._incoming
        for edge in dic[v].values():
            yield edge
    
    def insert_vertex(self,x = None):
        v = Vertex(x)                                       # Create new Vertex instance
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}                          # If directed graph, make an incoming edge
        return v
    
    def insert_edge(self,u,v,value = None):
        e = Edge(u,v,value)                                 # Create new Edge instance
        self._outgoing[u][v] = e
        self._incoming[v][u] = e

    def get_adj_map(self):
        return self._outgoing

class Min_Heap:
    class Node:
        def __init__(self,info,parent = None,left = None,right = None):
            self.info = info
            self.parent = parent
            self.left = left
            self.right = right
    
    def __init__(self):
        self.TREE = []
    
    """IMPORTANT ! --> For easier implementation, array TREE[0] contains None and index starts from 1"""
    def insert_heap(self,vertex):
        if len(self.TREE) == 0:
            self.TREE.append(None)
        self.TREE.append(vertex)
        ptr = self.TREE.index(vertex)
        while ptr > 1:
            par = math.floor(ptr/2)
            if vertex._key >= self.TREE[par]._key:
                self.TREE[ptr] = vertex
                return vertex
            self.TREE[ptr] = self.TREE[par]
            ptr = par
        if ptr == 1:
            self.TREE[ptr] = vertex
        return vertex
    
    def delete_heap(self):
        item = self.TREE[1]
        last = self.TREE.pop(-1)
        size = len(self.TREE[1:])
        ptr = 1
        left = 2 
        right = 3
        while right <= size:
            if last._key <= self.TREE[left]._key and last._key <= self.TREE[right]._key:
                self.TREE[ptr] = last
                return item
            if self.TREE[left]._key <= self.TREE[right]._key:
                self.TREE[ptr] = self.TREE[left]
                ptr= left
            else:
                self.TREE[ptr] = self.TREE[right]
                ptr = right
            left = 2*ptr
            right = 2*ptr + 1
        if left == size and last._key > self.TREE[left]._key:
            ptr = left
            self.TREE[ptr] = last
        return item
    
    def is_Empty(self):
        return len(self.TREE) == 1
    
    def get_heap(self):
        return self.TREE

    def Decrease_Key(self,v):
        i = self.TREE.index(v)
        par = math.floor(i/2)
        while i > 1 and self.TREE[par]._key > self.TREE[i]._key:
            temp = self.TREE[i]
            self.TREE[i] = self.TREE[par]
            self.TREE[par] = temp
            i = par

def MST_Prims(G,root):
    heap = Min_Heap()
    vertices = list(G.vertices())
    adj_map = G.get_adj_map()
    for vertex in vertices:
        vertex._key = math.inf
        vertex._parent = None
    root._key = 0
    for vertex in vertices:
        heap.insert_heap(vertex)
    heap_arr = heap.get_heap()
    while not heap.is_Empty():
        u = heap.delete_heap()
        for v in adj_map[u]:
            if v in heap_arr and adj_map[u][v]._element < v._key:
                v._parent = u
                v._key = adj_map[u][v]._element
                heap.Decrease_Key(v)
    print('MST Generated')


gr = Graph()
a = gr.insert_vertex('a')
b = gr.insert_vertex('b')
c = gr.insert_vertex('c')
d = gr.insert_vertex('d')
e = gr.insert_vertex('e')
f = gr.insert_vertex('f')
g = gr.insert_vertex('g')
h = gr.insert_vertex('h')
i = gr.insert_vertex('i')
gr.insert_edge(a,b,4)
gr.insert_edge(a,h,8)
gr.insert_edge(b,h,11)
gr.insert_edge(b,c,8)
gr.insert_edge(h,i,7)
gr.insert_edge(h,g,1)
gr.insert_edge(i,g,6)
gr.insert_edge(i,c,6)
gr.insert_edge(c,f,4)
gr.insert_edge(g,f,2)
gr.insert_edge(d,f,14)
gr.insert_edge(f,e,10)
gr.insert_edge(d,e,9)
gr.insert_edge(c,d,7)

MST_Prims(gr,a)
