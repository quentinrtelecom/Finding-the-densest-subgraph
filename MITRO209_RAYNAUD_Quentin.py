import timeit
import matplotlib.pyplot as plt

## Links to graphs
graph_to_test1 = 'D:\\Documents\\Télécom\\MITRO\\mitro209\\data_to_test\\bons\\facebook_combined.txt'
graph_to_test2 = 'D:\\Documents\\Télécom\\MITRO\\mitro209\\data_to_test\\bons\\deezer_europe_edges.csv'
graph_to_test3 = 'D:\\Documents\\Télécom\\MITRO\\mitro209\\data_to_test\\bons\\lastfm_asia_edges.csv'
graph_to_test4 = 'D:\\Documents\\Télécom\\MITRO\\mitro209\\data_to_test\\bons\\musae_git_edges.csv'
graph_to_test5 = 'D:\\Documents\\Télécom\\MITRO\\mitro209\\data_to_test\\bons\\RO_edges.csv'

## Main function

def densest_subgraph(adress_graph):
    if adress_graph[-1]=='t':  # The codes to read .txt files and .csv file are slightly different. Using bool will help the program to choose the way it has read the lines. The t correspond to the last t of .txt
        bool = True
    else:
        bool = False
    with open(adress_graph) as f:
        lines = f.readlines()
        E = len(lines)
    
    #print(E)
    nodes_by_degree = {i:dict() for i in range(E)} #dictionnary where the key i is a dictionnary of the nodes of degree i. If the degree of a node is i, it is a key associated to the value 1 in the i-th dictionnary
    degree_of_nodes = {i:{} for i in range(E)} #dictionnary where the key i represents a node, and the value represents the degree of this node
    neighbours = {i:{} for i in range(E)}# dictionnary where the key i represent a node, and the value is a dictionnary of all the neighbours of the node i. If a node is a neighbour of i, it is a key associated to the value 1 in the i-th dictionnary
    

    N=0    #N will be the number of nodes in the entry graph
    max_node = 0  #max_node will be the useful number of nodes. In some graphs, there are nodes of degree zeros. We will never consider them as they are not useful. In the end, we always have that max_node <= N 
    M = E
    with open(adress_graph) as f:
        for line in f:
            
            if bool:    #Use when .txt files
                node1,node2 = line.strip().split()
            if not bool: #Use when .csv files
                node1,node2 = line.split(',')  
            curr_node = int(node1)
            linked_node = int(node2)
            if curr_node >=N:               # computing N the max number of nodes of the entry graph.
                N = curr_node
            if linked_node>=N:
                N = linked_node
            if degree_of_nodes[curr_node]:
                degree_of_nodes[curr_node]+=1
                nodes_by_degree[degree_of_nodes[curr_node]][curr_node] = 1
                del nodes_by_degree[degree_of_nodes[curr_node]-1][curr_node]
                neighbours[curr_node][linked_node] = 1
                if linked_node!=curr_node:
                    if degree_of_nodes[linked_node]:
                        degree_of_nodes[linked_node]+=1
                        nodes_by_degree[degree_of_nodes[linked_node]][linked_node] = 1
                        del nodes_by_degree[degree_of_nodes[linked_node]-1][linked_node]
                        neighbours[linked_node][curr_node] = 1
                        
                    else:
                        degree_of_nodes[linked_node] = 1
                        nodes_by_degree[1][linked_node] = 1
                        neighbours[linked_node][curr_node] = 1
                        max_node+=1
                
            else:
                
                degree_of_nodes[curr_node] = 1
                nodes_by_degree[1][curr_node] = 1
                max_node+=1
                if linked_node!=curr_node:
                    if degree_of_nodes[linked_node]:
                        degree_of_nodes[linked_node]+=1
                        nodes_by_degree[degree_of_nodes[linked_node]][linked_node] = 1
                        del nodes_by_degree[degree_of_nodes[linked_node]-1][linked_node]
                        neighbours[linked_node][curr_node] = 1
                        
                    else:
                        degree_of_nodes[linked_node] = 1
                        nodes_by_degree[1][linked_node] = 1
                        neighbours[linked_node][curr_node] = 1
                        max_node+=1
                    neighbours[curr_node][linked_node] = 1
    
    best_density = 0
    removed = []
    min_deg = 0
    while not nodes_by_degree[min_deg]:
        min_deg +=1
    for i in range(max_node-1):    #the number of iteration is equal to the number of nodes in the entry graph
        density = E/max_node
        if best_density <= density:
            best_density = density
            best_iter = i
        
        min_deg_node = next(iter(nodes_by_degree[min_deg]))
        removed.append(min_deg_node)

        del nodes_by_degree[min_deg][min_deg_node]
        
        E-=min_deg
        max_node-=1
        for neighbour in neighbours[min_deg_node]:  #modifying the degree, and the place in nodes_by_degree, of every neighbours of min_deg_node
            del nodes_by_degree[degree_of_nodes[neighbour]][neighbour]
            degree_of_nodes[neighbour] -= 1
            nodes_by_degree[degree_of_nodes[neighbour]][neighbour] = 1
            del neighbours[neighbour][min_deg_node]
        #print(nodes_by_degree)
        if min_deg > 0 and nodes_by_degree[min_deg-1]:
            min_deg-=1
        else:
            while not nodes_by_degree[min_deg]:
                min_deg+=1
    
    return [N,M,best_density,best_iter]

## Tests

R1 = densest_subgraph(graph_to_test1)
R2 = densest_subgraph(graph_to_test2)
R3 = densest_subgraph(graph_to_test3)
R4 = densest_subgraph(graph_to_test4)
R5 = densest_subgraph(graph_to_test5)

print(R1)
print(R2)
print(R3)
print(R4)
print(R5)

##Time computing

elapsed_time1 = timeit.timeit(lambda: densest_subgraph(graph_to_test1), number = 10)/10
elapsed_time2 = timeit.timeit(lambda: densest_subgraph(graph_to_test2), number = 10)/10
elapsed_time3 = timeit.timeit(lambda: densest_subgraph(graph_to_test3), number = 10)/10
elapsed_time4 = timeit.timeit(lambda: densest_subgraph(graph_to_test4), number = 10)/10
elapsed_time5 = timeit.timeit(lambda: densest_subgraph(graph_to_test5), number = 10)/10

L_time = [elapsed_time1, elapsed_time2,elapsed_time3, elapsed_time4, elapsed_time5]
L_lenghts = [R1[0]+R1[1], R2[0]+R2[1], R3[0]+R3[1], R4[0]+R4[1], R5[0]+R5[1] ]

## Ploting

plt.scatter(L_lenghts,L_time)

plt.show()
# print("Elapsed Time:", elapsed_time,"seconds")

