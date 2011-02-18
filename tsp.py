#!/usr/bin/env python

import sys


def load(filename):
    """Load a TSP input.

    Read a TSP input file and construct a data structure containing the
    specified edges. Yield a tuple of the number of nodes in the graph
    and the edges that connect them.

    An adjacency matrix should not be constructed because for n -> 20K,
    the memory usage of such a structure will quickly become excessive.
    """
    adj = None
    Nnodes = -1

    with open(filename, 'r') as f:
        # calculate the number of nodes in the graph.
        line1 = f.readline()
        nnodes_offset = line1.find('#') + 1
        Nnodes = int(line1[nnodes_offset:])

        # create an adjacency list.
        # list multiplication is faster, but in this case it creates
        # a list of pointers to the same dict. a comprehension must
        # be used.
        adj = [{} for i in range(Nnodes)]

        # retrieve, parse, and store all edges.
        # to retrieve an edge weight, use (adj[src][dest]).
        # to search, use (dest in adj[src]).
        for line in f:
            edge_src_str, edge_dest_str, edge_wt_str = line.split()
            edge_src = int(edge_src_str)
            edge_dest = int(edge_dest_str)
            edge_wt = float(edge_wt_str)
            adj[edge_src][edge_dest] = edge_wt
            adj[edge_dest][edge_src] = edge_wt

    return adj


def greedy_tsp(adj):
    """Nearest-neighbor solution to TSP.

    Not the optimal or fastest solution, but Good Enough
    for what we're doing (for now).
    """
    current_vertex = 1
    total_cost = 0
    visited = []
    path = []

    def lesser(x, y):
        return x if x < y else y

    def binary_insert(sorted_list, entry):
        def bsplice(start, end):
            if start == end:
                sorted_list[start:end] = [entry, ]
                return
            mid = start + (end - start) / 2
            if entry > sorted_list[mid]:
                bsplice(mid, end)
            else:
                bsplice(start, mid)
        bsplice(0, len(sorted_list))

    def binary_search(sorted_list, entry):
        if len(sorted_list) == 1:
            return entry == sorted_list[0]
        L = len(sorted_list) / 2
        if entry > sorted_list[L]:
            lower = sorted_list[:L]
            return binary_search(lower, entry)
        else:
            upper = sorted_list[L + 1:]
            return binary_search(upper, entry)

    def been_to(vertex):
        return binary_search(visited, vertex) != -1

    def lightest_from(graph, vertex):
        outbound_edges = graph[vertex]
        def lesser_weight(x, y):
            return (x if outbound_edges[x] < outbound_edges[y] \
                    else y)
        lightest_dest = reduce(lesser_weight, outbound_edges)
        return (lightest_dest, outbound_edges[lightest_dest])

    while len(visited) != len(adj):
        destination, cost = lightest_from(adj, current_vertex)
        total_cost += cost
        path.append(destination)
        current_vertex = destination
        binary_insert(visited, current_vertex)

    return (path, total_cost)


def main(argv):
    pass


if __name__ == '__main__':
    sys.exit(main(sys.argv))
