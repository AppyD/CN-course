''' Contains the functions used to simulate the 1D Oslo Model and perform
statistical analyses on the data. See 'plotting' module for the code to create
the graphs used in the Complexity Project Report.'''


import numpy as np
import random as rndm
from collections import Counter
import log_bin_CN_2016 as lbcn
import cPickle as pickle


def load_oslo_data():
    ''' Load the pre-made data for the Oslo Model with 1000000 iterations for
    L = 8,16,32,64,128,256 and also for L=256 with 10000 and 100000 iterations.
    Can use example command:
        d8,d16,d32,d64,d128,d256,d256ten,d62hundred = cp.load_oslo_data()
        to load the data into these variables.'''
    
    dat = pickle.load(open("oslo_data_2.p", "rb"))
    return dat[0], dat[1], dat[2], dat[3], dat[4], dat[5]
   
    
#Task 1

def initialise_lattice(L):
    ''' Creates an empty 1D lattice of size L with threshold slopes of either 1
    or 2 for each site. Each element of the lattice array is contained in the
    form [slope z, threshold slope zth]. '''
    
    lattice = [[0, rndm.randint(1,2)] for i in range(0,L)]
#    lattice = [[0, 1] for i in range(0,L)]        # for testing only
    return lattice

###############################################################################

def oslo(L, num_it):
    ''' Implementation of the Oslo Model in 1D. Set smooth to a different value
    to get a moving average of the height instead.'''
    
    lattice = initialise_lattice(L)

    s = []    # list of avalanche sizes
    h = []    # list of avalance heights
    t = []    # list of times
    
    for n in range(1,num_it+1):
        lattice[0][0] += 1
        size = 0
        count = 0
        while count < L:

            count = 0
            for i in range(0,L):
                
                if lattice[i][0] > lattice[i][1]:
                
                    size += 1

                    if i == 0:
                        lattice[0][0] -= 2
                        lattice[1][0] += 1
                
                    elif i == L-1:
                        lattice[L-1][0] -= 1
                        lattice[L-2][0] += 1
                
                    else:
                        lattice[i][0] -= 2
                        lattice[i+1][0] += 1
                        lattice[i-1][0] += 1
            
                    lattice[i][1] = rndm.randint(1,2)
                
                else:
                    count += 1
                    
        t.append(float(n))
        h.append(float(np.sum(lattice, 0)[0]))
        s.append(float(size))
    
    return lattice, s, t, h
    
###############################################################################

# Task 2b    

def moving_average(h, W):
    ''' Returns a moving average of the data h using a window of size 2W+1.'''
    window = np.ones(int(W))/float(W)
    return np.convolve(h, window, 'same')
    

def data_collapse(t, h, L):
    ''' Performs a data collapse for a given system size of the processed height.'''
    
    t_coll = [float(i)/(L**2) for i in t]
    h_coll = [i/L for i in h]
    
    return t_coll, h_coll

###############################################################################

# Task 2c

def crop(t,h,L):
    ''' Keep recurrent configurations and crop out transient configurations.'''
    
    rec = next(j for j in t if j > (L**2 + 100))    # '+100' to be certain we are in recurrent stage
    i = t.index(rec)     
    tlist, hlist = t[i:], h[i:]
    
    return tlist, hlist


def height_av(t,h,L):
    ''' Find the average height of a given list of times and heights.'''
    
    tlist, hlist = crop(t,h,L)
    avh = np.sum(hlist)/len(hlist)
    
    return avh
    
    
def stdev(t,h,L):
    ''' Find the standard deviation of the height in the recurrent stage.'''
    
    tlist, hlist = crop(t,h,L)
    
    av_hsqr = np.sum([i**2 for i in hlist], dtype=long)/float(len(hlist))
    sqr_avh = float((height_av(tlist, hlist, L))**2)
    
    stdev = float((av_hsqr - sqr_avh)**0.5)
    return stdev
    
###############################################################################    
    
# Task 2d 
 
def height_prob(heights):
    ''' Calculate the height probability.'''
    
    h_dict = Counter(heights)
    h_list, prob_list = [], []
    
    for  key, value in h_dict.iteritems():   # turn dictionary into the lists of heights and probabilties
        h_list.append(key)
        prob_list.append(value)
        
    probs = [float(i)/len(heights) for i in prob_list]
    
    return h_list, probs

###############################################################################

# Task 3a

def avalanche_prob(s,t,L):
    ''' Calculate the avalanche size probability.'''
    
    times, sizes = crop(t,s,L)
    
    s_dict = Counter(sizes)
    s_list, prob_list = [], []
    
    for  key, value in s_dict.iteritems():
        s_list.append(key)
        prob_list.append(value)
    
    probs = [float(i)/len(sizes) for i in prob_list]
    
    return s_list, probs, prob_list
    

# adapted function from 'log_bin_CN_2016' module
def log_binning(s, a):
    ''' Log bin the avalance sizes.'''
    
    b, c = lbcn.log_bin(s, 1.0, 1.5, a, 'integer', drop_zeros=True)
    return b,c

###############################################################################    
    
# Task 3c

def FSSA(s,P,tau,D,L):
    ''' Data collapse for testing the finite-size scaling ansatz (FSSA).'''
    
    scaled_s = [i/(L**D) for i in s]
    scaled_P = [(s[i]**tau)*P[i] for i in range(0, len(s))]
    return scaled_s, scaled_P

###############################################################################

# Task 3d    

def moment_k(s, k):
    ''' Calculate the k'th mooment of the avalanche size.'''
    
    sk = [i**k for i in s]
    kmom = np.sum(sk)/float(len(s))
    return kmom