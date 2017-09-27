import numpy as np
import bisect
from collections import Counter
import random

###############################################################################
################ Initialisation of graph ######################################
###############################################################################

def possible_connections(node, edge_list, node_list):
    ''' Returns a list of nodes that a given node could add a new edge with, for
    the initial random graph of N nodes.'''
   
    available_nodes = [i for i in node_list]
    neighbours = [i[1] for i in edge_list if i[0] == node] + [i[0] for i in
                edge_list if i[1] == node] + [node]
        
    for i in neighbours:
        available_nodes.pop(available_nodes.index(i))
    
    return available_nodes

def initialise_graph(N):
    ''' Create a random initial graph with N nodes of degree 1, stored in an
    adjacency list. Note: self-edges are not allowed and each node has at least 
    one edge so that preferential attachment may later occur.'''
    
    node_list = [i for i in xrange(N)]
    edge_list = []
    
    for x in node_list:      
        available_nodes = possible_connections(x, edge_list, node_list)
        connecting_node = random.choice(available_nodes)
        edge_list.append(sorted([x, connecting_node]))
    
    sorted_edges = sorted(edge_list, key = lambda x: x[0])
    
    return sorted_edges

################################################################################
################################################################################
##################### GENERAL FUNCTIONS FOR ALL PHASES #########################    

def degree(node, edge_list):
    ''' Returns the degree of a given node in the network.'''
    
    degree = 0
    
    for i in edge_list:
        if i[0] == node or i[1] == node:
            degree += 1
        if i[0] > node:
            break
    
    return degree
    

def add_edge(node, second_node, edge_list):
    ''' Create an edge between two nodes with probability k/2E.'''
    
    bisect.insort_left(edge_list, sorted([node, second_node]))
    print "Edge added between ", node, " and ", second_node
    
    
def numerical_degree_distribution(degree_list, kmax, N, edge_list):
    ''' Calculate the numerical degree distribution for a given network.'''
    
    degree_counts = Counter(degree_list)
    probabilities = []
    
    for i in xrange(kmax+1):
        num_k = degree_counts[i]
        probabilities.append(float(num_k)/N)
    
    return probabilities

###############################################################################
########################### PHASE ONE ########################################

def preferential_p_infinity(k,m):
    ''' Returns the value of the degree distribution p_infinity at a particular
    value of the degree k and m.'''
    
    if k < m:     # validity of theoretical distribution
        return 0
    else:
        return (2.*m*(m+1))/(k*(k+1)*(k+2))
        
      
def preferential_attachment_theory(N, m, kmax):
    ''' Calculate the theoretical degree distribution for a given network that
    follows a preferential attachment scheme.'''
    
    return [preferential_p_infinity(i,m) for i in xrange(kmax+1)]
     
    
def preferential_attachment_k1(m):
    ''' Calculate the theoretical value of k1 for various N for a particular m, 
    in a preferential attachment scheme.'''
    
    return [ (-1 + np.sqrt(1 + 4*i*m*(m+1)) )/2. for i in xrange(100,10100,100)]

###############################################################################
###############################################################################
############################# PHASE TWO #######################################

def random_p_infinity(k,m):
    ''' Returns the value of the degree distribution for a network with random
    attachment.'''
    
    if k < m:
        return 0
    else:
        return (float(m)**(k-m))/((1+m)**(k-m+1))


def random_attachment_theory(m,kmax):
    ''' Calculate the theoretical degree distribution for a network following a
    random attachment scheme when picking new nodes.'''
    
    return [random_p_infinity(i,m) for i in xrange(kmax+1)]


def random_attachment_k1(m):
    ''' Calculate the theoretical value of k1 for various N for a particular m,
    in a random attachment scheme.'''
    
    return [m - (np.log(i))/(np.log(m)-np.log(m+1)) for i in xrange(100,10100,100)]


################################################################################
################################################################################
############################## PHASE THREE #####################################

def existing_p_infinity(k,m):
    ''' Returns the value of the degree distribution for a network with edges being
    added between existing vertices as well.'''
    
    if k < m:
        return 0
    else:
        return (m**(k-m))/((1+m)**(k-m+1))


def existing_nodes_theory(m,kmax):
    ''' Calculate the theoretical degree distribution for a network with edges being
    added between existing vertices as well.'''
    
    return [random_p_infinity(i,m) for i in xrange(1,kmax+1)]


def possible_connections_3(node, edge_list, node_list):
    ''' Returns a list of nodes that a given node could add a new edge with, for
    the initial random graph of N nodes.'''
   
    available_nodes = [i for i in node_list]
    neighbours = [i[1] for i in edge_list if i[0] == node] + [i[0] for i in
                edge_list if i[1] == node]
        
    for n in neighbours:
        try:                # i am not sure having a try statement here is a good solution...
            available_nodes.pop(available_nodes.index(n))    
        except:
            print "could not remove from list"
    
    return available_nodes



################################################################################

def chi_square(expected_list, data_list):
    ''' Returns the chi-squared value for the distribution.'''
    
    chi = 0
    for i in xrange(len(expected_list)):
        try:
            chi_i = ((data_list[i] - expected_list[i])**2)/data_list[i]
            chi += chi_i
        except: #ZeroDivisionError:
            continue
            
    return chi