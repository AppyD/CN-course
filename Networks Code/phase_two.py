import networks_project as n
import numpy as np
import random
import matplotlib.pyplot as plt
import time

start = time.time()

N_initial = 10
m = 1
propagation_time = 10000
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
probs = n.numerical_degree_distribution(degree_list, kmax, N_total, edge_list)
theo_probs = n.random_attachment_theory(m, kmax)

plt.figure(2)
plt.loglog(xrange(kmax+1), probs, 'yo', label='m= '+str(m))
plt.loglog(xrange(kmax+1), theo_probs, 'y--')

plt.legend()
plt.xlabel('Degree, k', fontsize='large')
plt.ylabel(r'Degree distribution, $p_\infty(k)$', fontsize='large')
plt.show()

print "Theoretical probabilities sum to ", np.sum(theo_probs)
print "Chi-Square = ", n.chi_square(theo_probs, probs)

#edge_list[:] = []    # clear lists/variables to avoid any trouble when looping...
#degree_list[:] = []
#probs[:] = []
#theo_probs[:] = []

end = time.time()
print "\nRuntime was ", end-start, " seconds."