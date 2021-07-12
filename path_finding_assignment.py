"""
Python file for FIT2004 assignment 4
Author : Neo Shao Hong
Student ID : 31276520
"""

#%% graph class
class Graph:
    """
    Constructor

    Arguments:
        n -> size of graph
    
    Time : O(n)
    Aux. space : O(n)
    """
    def __init__(self, n):
        self.vertices = []
        for i in range(n):
            self.vertices.append(Vertex(i))

    """
    Add edge to graph

    Arguments:
        u -> id of starting vertex
        v -> id of ending vertex
        w -> weight of edge
        argv_directed -> whether the edge is directed or not
    
    Time: O(1)
    Aux. space: O(1)
    """
    def add_edge(self, u, v, w, argv_directed = True):
        edge = Edge(self.vertices[u],self.vertices[v],w)
        self.vertices[u].add_edge(edge)
        if not argv_directed:
            self.vertices[v].add_edge(edge)

    """
    Use djikstra algorithm to find a path from start to end.
    Returns (length of the path, the path)

    Arguments:
        start -> id of starting vertex
        end -> id of ending vertex
        search_id -> identifier for this search

    Time : O(E log V) 
        where E is the number of edges in the graph
            V is the number of vertices in the graph
    
    Aux.space : O(V) where V is the number of vertices in the graph
    """
    def djikstra(self, start, end, search_id = 1):
        index_array = [i for i in range(len(self.vertices))]
        heap = [None]* len(self.vertices)
        heap[0] = self.vertices[start]
        heap[0].payload = (0, None)
        size = 1
        
        def swap(i,j):
            heap[i], heap[j] = heap[j], heap[i]
            index_array[heap[i].id], index_array[heap[j].id] = (
                index_array[heap[j].id], index_array[heap[i].id])
            
        # store (volume, predecessor) at vertex
        while size>0:
            #serve
            current = heap[0]
            if current == self.vertices[end]:
                break;
            size-=1
            current.visited = search_id
            #sink
            if size>0:
                k = 0
                swap(k, size)
                while 2*k+1<size:
                    min_child, child_pos = (
                        min((heap[2*k+1], 2*k+1), (heap[2*k+2], 2*k+2), key = (lambda x: x[0]))
                        if 2*k+2<size else (heap[2*k+1], 2*k+1))
                    if min_child<heap[k]:
                        swap(child_pos, k)
                    else:
                        break;
            # edge relaxation
            for edge in current.edges:
                destination = edge.v if edge.v!=current else edge.u
                changed = False
                if destination.visited != search_id:
                    if destination.discovered != search_id:
                        changed = True
                        destination.discovered = search_id
                        index_array[destination.id] = size
                        heap[index_array[destination.id]] = destination
                        size+=1
                    elif destination.payload[0]>current.payload[0] + edge.w:
                        changed = True
                #rise (update)
                if changed: 
                    destination.payload = (current.payload[0] + edge.w, current)
                    index = index_array[destination.id]
                    while index>0 and heap[(index-1)//2]>heap[index]:
                        swap(index, (index-1)//2)
                        index = (index-1)//2

        return self.vertices[end].payload[0], self.reconstruct(start,end)

    """
    Reconstruct path from start to end. Returns the reconstructed path

    Argument:
        start -> id of starting vertex
        end -> id of ending vertex

    Time : O(n) where n is the length of the reconstructed path
    Aux. space : O(n) where n is the length of the reconstructed path
    """
    def reconstruct(self, start, end):
        path = []
        current = self.vertices[end]
        loop = start == end and current.payload[1]!=None
        while current.id!=start or loop:
            loop = False
            path.append(current.id)
            current = current.payload[1]
        path.append(start)
        return path[::-1]

class Vertex:
    """
    Constructor

    Arguments:
        id -> identifier of this vertex
        payload -> data to store at vertex

    Time : O(1)
    Aux. space : O(1)
    """
    def __init__(self, id, payload = None):
        self.edges = []
        self.id = id
        self.payload = payload
        self.visited = 0
        self.discovered = 0

    """
    Add an edge to the vertex's adjacency list

    Arguments:
        edge -> edge to add

    Time : O(1)
    Aux. space : O(1)
    """
    def add_edge(self, edge):
        self.edges.append(edge)

    """
    Comparism method for vertex

    Arguments:
        other -> another vertex to compare to

    Time: O(1)
    Aux. space: O(1)
    """
    def __lt__(self, other):
        return self.payload[0]<other.payload[0]
    
class Edge:
    """
    Constructor

    Arguments:
        u -> id of starting vertex
        v -> id of ending vertex
        w -> weight of edge

    Time: O(1)
    Aux. space: O(1)
    """
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

# %% Question 1
from math import inf

"""
Find the maximum value that can be obtained after performing at most
max_trades trades. Returns the maximum value.

Arguments:
    prices -> an array of length n, where prices[i] is the value of 
                1L of the liquid with ID i.
    starting_liquid -> ID of the liquid you arrive with. You always 
                start with 1L of this liquid.
    max_trades -> maximum number of trades you can conduct
    townspeople -> a list of lists. Each interior list corresponds 
                to the trades offered by a particular person. The interior 
                lists contain 3 element tuples, (give, receive, ratio).
                Each tuple indicates that this person is willing to be given 
                liquid with ID give in exchange for liquid with ID receive 
                at the given ratio.

Time : O(T*M) 
    where T is the total number of trades available
        M is max_trades

Aux.space : O(T + L) 
    where T is the total number of trades available
        L is the length of starting_liquid
"""
def best_trades(prices, starting_liquid, max_trades, townspeople):
    max_price = 1*prices[starting_liquid]
    graph = Graph(len(prices))

    for people in townspeople:
        for (u,v,w) in people:
            graph.add_edge(u, v, w)
    
    volume = [[-inf, -inf] for _ in range(len(prices))]
    volume[starting_liquid] = [1,1]
    
    trades = 1
    edges = graph.vertices[starting_liquid].edges
    while trades<=max_trades:
        changes = False
        edges2 = []
        for e in edges:
            if volume[e.u.id][(trades-1)%2]*e.w > volume[e.v.id][trades%2]:
                volume[e.v.id][trades%2] = volume[e.u.id][(trades-1)%2]*e.w
                changes = True
                if volume[e.v.id][trades%2]*prices[e.v.id]>max_price:
                    max_price = volume[e.v.id][trades%2]*prices[e.v.id]
            if e.v.visited!=trades:
                for e2 in e.v.edges:
                    edges2.append(e2)
                e.v.visited = trades
        if not changes:
            break;
        edges = edges2
        trades+=1
    return max_price
                    
# %% Question 2
"""
Calculate the most optimal way to travel from one city to another,
with the option of making a delivery from one city to another.
Returns the minimum cost of traveling from the start to end city.

Arguments:
    n -> the number of cities. The cities are numbered [0..n-1].

    roads -> list of tuples. Each tuple is of the form (u,v,w). 
    Each tuple represents an road between cities u and v. w is 
    the cost of traveling along that road, which is always 
    non-negative. Note that roads can be traveled in either direction, 
    and the cost is the same. 

    start -> id of starting city
    end -> id of ending city

    delivery -> tuple containing 3 values. The first value is the city 
    where we can pick up the item. The second value is the city where 
    we can deliver the item. The third value is the amount of money we
    can make if we deliver the item from the pickup city to the delivery city.

Time : O(R log(N)) 
    where R is the total number of roads
        N is the total number of cities

Aux. space : O(N + R) 
    where R is the total number of roads
        N is the total number of cities
"""
def opt_delivery(n, roads, start, end, delivery):
    graph = Graph(n)
    for (u,v,w) in roads:
        graph.add_edge(u, v, w, False)

    # no detour
    (normal, normal_path) = graph.djikstra(start, end, 1)
    
    # start to pickup
    (detour, detour_path) = graph.djikstra(start, delivery[0], 2) 

    # pickup to delivery point
    temp = graph.djikstra(delivery[0], delivery[1], 3)
    detour += temp[0]
    for i in range(1, len(temp[1])):
        detour_path.append(temp[1][i])

    # pickup to end
    temp = graph.djikstra(delivery[1], end, 4)
    detour += temp[0]
    for i in range(1, len(temp[1])):
        detour_path.append(temp[1][i])

    if detour-delivery[2]<normal:
        return (detour-delivery[2], detour_path)
    else:
        return (normal, normal_path)
    

 # %%
