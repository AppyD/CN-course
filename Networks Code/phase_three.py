''' Note: It 'runs' for now but I am not entirely if sure the results are correct and there
were one or two workarounds in the code....What I tried is included here nevertheless.'''

import networks_project as n
import random
import matplotlib.pyplot as plt
import time

start = time.time()

N_initial = 100
m = 6
assert m < N_initial
r = int(m/2)
propagation_time = 10000
assert propagation_time > N_initial

edge_list = n.initialise_graph(N_initial)
degree_list = [n.degree(i, edge_list) for i in xrange(N_initial)]
weights = [i[0] for i in edge_list] + [i[1] for i in edge_list]    
            
for i in xrange(N_initial, propagation_time):
    new_node_counter = 0
    existing_node_counter = 0
    
    ### attach r edges to already existing vertices
    while existing_node_counter < r:
        existing_node = random.choice([w for w in weights if w != i])
        connecting_node = random.choice(n.possible_connections_3(existing_node, edge_list, xrange(i)))
        
        if sorted([existing_node, connecting_node]) in edge_list:
            continue
        
        else:
            n.add_edge(existing_node, connecting_node, edge_list)
            existing_node_counter += 1
            degree_list[existing_node] += 1
            degree_list[connecting_node] += 1
	    weights.append(existing_node)
	    weights.append(connecting_node)
    
    ### attach r edges to the new vertex
    while new_node_counter < r:
        connecting_node = random.choice(weights)
        
        if [connecting_node, i] in edge_list:       # sorted list so won't be in [i, connecting_node] form
            continue
        
        else:
            n.add_edge(i, connecting_node, edge_list)
            new_node_counter += 1
            if len(degree_list) == i:
                degree_list.append(1)
            else:
                degree_list[i] += 1
            degree_list[connecting_node] += 1
            weights.append(connecting_node)
            weights.append(i)
    


kmax = max(degree_list)
probs = n.numerical_degree_distribution(degree_list, kmax, propagation_time, edge_list)
#theo_probs = n.theoretical_degree_distribution(N_total, m, kmax)


plt.figure()
plt.loglog(xrange(kmax+1), probs, 'rx', label='N='+str(propagation_time))
#plt.loglog(xrange(kmax+1), theo_probs, 'b-', label='theoretical degree distribution')

plt.legend()
plt.xlabel('Degree, k', fontsize='large')
plt.ylabel(r'Degree distribution, $p_\infty(k)$', fontsize='large')
plt.show()

edge_list[:] = []    # clear lists/variables to avoid any trouble when looping...
degree_list[:] = []
probs[:] = []
#theo_probs[:] = []


end = time.time()

#print "Theoretical probabilities sum to ", np.sum(theo_probs)
#print "Chi-Square = ", n.chi_square(theo_probs, probs)

print "\nRuntime was ", end-start, " seconds."