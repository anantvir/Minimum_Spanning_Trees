"""Author - Anantvir Singh, concept reference:= Data Structures and Algorithms in Python by Michael T. Goodrich et al"""


# --------------------------- Adjaceny Map Representation of a Graph ----------------------------------------

class Vertex:
    def __init__(self,x):
        self._element = x
    
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
    
    def edges(self):
        edges = set()
        for eachDict in self._outgoing.values():
            for eachValue in eachDict.values():
                edges.add(eachValue)
        return edges
    
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

    def get_adjacency_map(self):
        return self._outgoing


set_dict = {}               # Make it global to make the program simpler. Disjoint sets are stored here with key = representative of a set(i.e first element of linked list)
class DisjointSet:
    class Node:
        def __init__(self,info,FORWARD_LINK = None, BACKWARD_LINK = None):
            self.info = info
            self.FORWARD_LINK = FORWARD_LINK
            self.BACKWARD_LINK = BACKWARD_LINK

    class SetObject:
        def __init__(self,set_object_name = None,head = None,tail = None):
            self.set_object_name = set_object_name
            self.head = None
            self.tail = None
        
        def __hash__(self):
            return hash(self.set_object_name)  
    
    def Make_Set(self,item):            # Creates a new linked list, whose only object is 'item'
        setObject = self.SetObject()
        newNode= self.Node(item)
        newNode.BACKWARD_LINK = setObject
        setObject.head = newNode
        setObject.tail = newNode
        set_dict[item] = setObject 
        return setObject
    
    def Find_Set(self,item):
        if set_dict.get(item) is not None:
            return set_dict[item].head
        else:
            for value in set_dict.values():
                node = value.head
                while node is not None:
                    if node.info == item:
                        return node.BACKWARD_LINK
                    node = node.FORWARD_LINK
                   
                raise ValueError('Cannot find this item in any Disjoint Set') 
                 # Representative of Set

    def Union(self,x,y):                # Implementation as per page 565 CLRS    
        x.tail.FORWARD_LINK = y.head
        x.tail = y.tail
        node = y.head
        while node is not None:
            node.BACKWARD_LINK = x
            node = node.FORWARD_LINK
        value = x.head.info
        set_dict[value] = x             # Create new disjoint set in set_dict
        del set_dict[y.head.info]       # Remove old set 'y' as y has been merged with 'x' now
        y.head = None                   # head and tail of 'y' are now None
        y.tail = None
        return x                        # Return new Disjoint set x


gr = Graph(directed=False)
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
gr.insert_edge(b,c,8)
gr.insert_edge(a,h,8)
gr.insert_edge(b,h,11)
gr.insert_edge(h,i,7)
gr.insert_edge(i,g,6)
gr.insert_edge(h,g,1)    
gr.insert_edge(i,c,2)
gr.insert_edge(c,f,4)
gr.insert_edge(g,f,2)
gr.insert_edge(d,f,14)
gr.insert_edge(f,e,10)
gr.insert_edge(d,e,9)
gr.insert_edge(c,d,7)



def MST_Kruskal(G):
    A = []
    ds= DisjointSet()
    for vertex in G.vertices():
        ds.Make_Set(vertex)
    edges = list(G.edges())
    sorted_edges = sorted(edges,key = lambda x: x._element)
    for edge in sorted_edges:
        u = edge._origin
        v = edge._destination
        if ds.Find_Set(u) != ds.Find_Set(v):
            A.append(edge)
            ds.Union(u,v)
    return A   

MST_Kruskal(gr)


