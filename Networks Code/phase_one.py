import networks_project as n
import log_bin_CN_2016 as lbcn
import numpy as np
import random
import time
import matplotlib.pyplot as plt


start = time.time()

N_initial = 10
m = 1
propagation_time = 100000

assert m < N_initial
assert propagation_time > N_initial

edge_list = n.initialise_graph(N_initial)
degree_list = [n.degree(i, edge_list) for i in xrange(N_initial)]
weights = [i[0] for i in edge_list] + [i[1] for i in edge_list]
#k1_list = []

for i in xrange(N_initial, propagation_time):
    counter = 0
    
    while counter < m:
        connecting_node = random.choice(weights)
        
        if [connecting_node, i] in edge_list:       # sorted list so won't be in [i, connecting_node] form
            continue
        
        else:
            n.add_edge(i, connecting_node, edge_list)
        
            weights.append(i)
            weights.append(connecting_node)
            
            counter += 1
            
            if len(degree_list) == i:
                degree_list.append(1)
            
            else:
                degree_list[i] += 1
            
            degree_list[connecting_node] += 1


kmax = max(degree_list)
#k1_list.append(kmax)
#k1_list.append(heapq.nlargest(5,degree_list))      # used for checking spread of k1 to k5

probs = n.numerical_degree_distribution(degree_list, kmax, propagation_time, edge_list)
theo_probs = n.preferential_attachment_theory(propagation_time, m, kmax)

#b,c = lbcn.log_bin(degree_list, 1.0, 1.5, 2.0)    # log-binned values

plt.figure(1)
plt.loglog(xrange(kmax+1), probs, 'o', color='green', label = r'N='+str(propagation_time))
plt.loglog(xrange(kmax+1), theo_probs, '-r')
#plt.loglog(b,c,'--', color='r', label = r'N = '+str(propagation_time))

plt.legend()
plt.xlabel(r'Degree, $k$', fontsize='large')
plt.ylabel(r'Degree distribution, $p_\infty(k)$', fontsize='large')
plt.show()

print "Theoretical probabilities sum to ", np.sum(theo_probs)     # not quite 1 because of initial network but close enough in large N limit

#edge_list[:] = []    # remember to clear lists/variables to avoid any trouble if looping...
#degree_list[:] = []
#probs[:] = []
#theo_probs[:] = []
#b[:] = []
#del c
#kmax = 0

end = time.time()

print "\nRuntime was ", end-start, " seconds."