

import sys


col0 = [-1, 3, 2, -1]
col1 = [-1, -1, 5, 2]
col2 = [-1, -1, -1, 3]
col3 = [-1, -1, -1, -1]


graph = [col0, col1, col2, col3]


t_col0 = [-1, 10, 10, -1, -1, -1]
t_col1 = [-1, -1, 2, 4, 8, -1]
t_col2 = [-1, -1, -1, -1, 9, -1]
t_col3 = [-1, -1, -1, -1, -1, 10]
t_col4 = [-1, -1, -1, 6, -1, 10]
t_col5 = [-1, -1, -1, -1, -1, -1]


test_graph = [t_col0, t_col1, t_col2, t_col3, t_col4, t_col5]


paths = []


class FlowObject:
    flow = 0
    capacity = 1


def build_networkflow_from(graph):
    size = len(graph)
    networkflow = [[FlowObject() for j in range(size)] for i in range(size)]
    for i in range(size):
        for j in range(size):
            networkflow[i][j].flow = 0
            networkflow[i][j].capacity = graph[i][j]
    return networkflow


def printnetworkflow(networkflow):
    size = len(networkflow)
    for i in range(size):
        for j in range(size):
            print(networkflow[i][j].flow, '/', networkflow[i][j].capacity, end=' | ')
        print()


def print_networkflow(networkflow):
    size = len(networkflow)
    for i in range(size):
        for j in range(size):
            print(networkflow[i][j].flow, '/', networkflow[i][j].capacity, end=' | ')
        print()


def find_minimal_capacity(residualgraph, networkflow, path):
    size = len(path)
    minimalcapacity = sys.maxsize
    for i in range(0, size-1):
        if residualgraph[path[i]][path[i+1]] <= minimalcapacity:
            minimalcapacity = networkflow[path[i]][path[i+1]].capacity - networkflow[path[i]][path[i+1]].flow
    return minimalcapacity


def update_networkflow(networkflow, graph, path, mincapacity):
    size = len(path)
    for i in range(0, size-1):
        if graph[path[i]][path[i+1]] > -1:                                                          # if forward edge
            networkflow[path[i]][path[i+1]].flow += mincapacity
        else:
            networkflow[path[i]][path[i+1]].flow -= mincapacity
    return networkflow


def update_routine(networkflow, residualgraph, path):
    minimalcapacity = find_minimal_capacity(residualgraph, networkflow, path)
    return update_networkflow(networkflow, residualgraph, path, minimalcapacity)


def build_residual_graph_from(networkflow):
    size = len(networkflow)
    residualgraph = [[-1 for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            if networkflow[i][j].capacity == -1:
                residualgraph[i][j] = residualgraph[i][j]
            elif networkflow[i][j].capacity > -1:
                residualgraph[i][j] = networkflow[i][j].capacity - networkflow[i][j].flow
                residualgraph[j][i] = networkflow[i][j].flow
    return residualgraph


def compare_paths(path1, path2):
    pathlen1 = len(path1)
    pathlen2 = len(path2)
    if pathlen1 != pathlen2:
        return False
    else:
        for i in range(0, pathlen1):
            if path1[i] != path2[i]:
                return False
    return True


def is_node_in_path(path, node):
    for i in range(0, len(path)):
        if path[i] == node:
            return True
    return False


def get_paths_bfs(graph, start, end):
    nodes = len(graph)
    queue = []
    queue.append([start])
    visited = [-1] * nodes
    while queue:
        path = queue.pop(0)
        currentnode = path[-1]
        visited[currentnode] = 1
        if currentnode == end:
            # paths.append(path)                                            # search of all paths
            return path
        for neighbor in range(len(graph)):
            if graph[currentnode][neighbor] > 0:
                if visited[currentnode] == 1 and visited[neighbor] == -1:   # check neighbor important to avoid loops
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
    return [-1, -1]
    # return paths                                                          # return all paths as list


def edmonds_karp_algorithm(graph, startnode, targetnode):
    networkflow = build_networkflow_from(graph)
    while 1:
        residualgraph = build_residual_graph_from(networkflow)
        shortestpath = get_paths_bfs(residualgraph, startnode, targetnode)
        if shortestpath[0] == -1:
            return networkflow
        else:
            networkflow = update_routine(networkflow, residualgraph, shortestpath)
    return networkflow


valid_solution = edmonds_karp_algorithm(test_graph, 0, 5)
invalid_solution = edmonds_karp_algorithm(graph, 0, 78)


print()
print()
printnetworkflow(valid_solution)
#build_maxflow_from(valid_solution)
print()
print()
printnetworkflow(invalid_solution)