import networks_project as n
import numpy as np
import random
import matplotlib.pyplot as plt
import time


k_list = []

def phase_two_k1(num_it, N_initial=10, m=1, propagation_time=10000):
    start = time.time()
    
    for z in xrange(num_it):
        N_total = N_initial + propagation_time
        
        edge_list = n.initialise_graph(N_initial)
        degree_list = [n.degree(i, edge_list) for i in xrange(N_initial)]    
                    
        for i in xrange(N_initial, N_total):
            counter = 0
            while counter < m:
                connecting_node = random.choice(xrange(i))
                
                if [connecting_node, i] in edge_list:       # sorted list so won't be in [i, connecting_node] form
                    continue
                
                else:
                    n.add_edge(i, connecting_node, edge_list)
                    counter += 1
                    if len(degree_list) == i:
                        degree_list.append(1)
                    else:
                        degree_list[i] += 1
                    degree_list[connecting_node] += 1
        
        kmax = max(degree_list)
        k_list.append(kmax)
        
        edge_list[:] = []    # clear lists/variables to avoid any trouble when looping...
        degree_list[:] = []
    
    end = time.time()    
    print "\nRuntime was ", end-start, " seconds."
    return k_list
    