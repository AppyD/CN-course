''' Plotting functions for use alongside the complexity_project module. Used to
produce basic figures given in the report. Note that, to save time in running the
oslo model repeatedly, pre-created data from a pickle file can be loaded for use 
in the plotting functions, if the user so wishes.'''


import complexity_project as cp
import matplotlib.pyplot as plt
import numpy as np


print "Do you want to load from 'oslo_data_2.p'? [y/n]"
choice = str(raw_input())

if choice == 'y':
    print "You have chosen to load from oslo_data.p"
    d8, d16, d32, d64, d128, d256 = cp.load_oslo_data()
    data_set = [d8, d16, d32, d64, d128, d256]
    load = 1
    
elif choice == 'n':
    print "You have chosen to generate the data yourself. Warning - some of the larger system sizes may take longer to produce results."
    load = 0

else:
    raise Exception("Please write either y or n!")
    
    
###############################################################################
############# PLOTTING FUNCTIONS FOR TASKS IN COMPLEXITY PROJECT ##############
###############################################################################   
    
    
def timeplot(num_it=100000):
    ''' Plots the height of the pile against time..'''
    
    plt.figure()
    
    if load == 0:
        model = cp.oslo(16, num_it)
        plt.plot(model[2], model[3], label='L=16')
        
        model = cp.oslo(32, num_it)
        plt.plot(model[2], model[3], label='L=32')
        
        model = cp.oslo(64, num_it)
        plt.plot(model[2], model[3], label='L=64')
        
        model = cp.oslo(128, num_it)
        plt.plot(model[2], model[3], label='L=128')
        
        model = cp.oslo(256, num_it)
        plt.plot(model[2], model[3], label='L=256')
    
    
    else:
        plt.plot(d16[2],  d16[3], label='L=16')
        plt.plot(d32[2],  d32[3], label='L=32')
        plt.plot(d64[2],  d64[3], label='L=64')
        plt.plot(d128[2], d128[3], label='L=128')
        plt.plot(d256[2], d256[3], label='L=256')
        plt.axis([-2540,100000,0,455])
    
    
    plt.xlabel('Time (units of number of grains added)')
    plt.ylabel('Height of pile (number of grains)')
    plt.title('h(t;L) vs t for various system sizes')
    plt.legend(bbox_to_anchor=(0.26,1))

##############################################################################

def smooth_data_collapse(num_it=100000):
    ''' Plots the data collapse of the processed height for the different 
    system sizes.'''
    
    plt.figure()   
    
    if load == 0:
        m = cp.oslo(16, num_it)
        h_smooth = cp.moving_average(m[3],25)
        t,h = cp.data_collapse(m[2],h_smooth,16)
        plt.plot(t, h, label='L=16')

        m = cp.oslo(32, num_it)
        h_smooth = cp.moving_average(m[3],25)
        t,h = cp.data_collapse(m[2],h_smooth,32)
        plt.plot(t, h, label='L=32')
        
        m = cp.oslo(64, num_it)
        h_smooth = cp.moving_average(m[3],25)
        t,h = cp.data_collapse(m[2],h_smooth,64)
        plt.plot(t, h, label='L=64')
        
        m = cp.oslo(128, num_it)
        h_smooth = cp.moving_average(m[3],25)
        t,h = cp.data_collapse(m[2],h_smooth,128)
        plt.plot(t, h, label='L=128')
        
        m = cp.oslo(256, num_it)
        h_smooth = cp.moving_average(m[3],25)
        t,h = cp.data_collapse(m[2],h_smooth,256)
        plt.plot(t, h, label='L=256')        
        
    else:
        h_smooth = cp.moving_average(d16[3],25)
        t,h = cp.data_collapse(d16[2],h_smooth,16)
        plt.plot(t, h, label='L=16')

        h_smooth = cp.moving_average(d32[3],25)
        t,h = cp.data_collapse(d32[2],h_smooth,32)
        plt.plot(t, h, label='L=32')
        
        h_smooth = cp.moving_average(d64[3],25)
        t,h = cp.data_collapse(d64[2],h_smooth,64)
        plt.plot(t, h, label='L=64')
        
        h_smooth = cp.moving_average(d128[3],25)
        t,h = cp.data_collapse(d128[2],h_smooth,128)
        plt.plot(t, h, label='L=128')
        
        h_smooth = cp.moving_average(d256[3],25)
        t,h = cp.data_collapse(d256[2],h_smooth,256)
        plt.plot(t, h, label='L=256')  
    
    
    plt.xlabel(r't/$L^2$', fontsize='large')
    plt.ylabel(r'$\tilde{h}$/L', fontsize='large')
    plt.title(r'Data Collapse of $\tilde{h}$')
    plt.axis([-1, 1.3, 0.3, 1.9])
    plt.legend(bbox_to_anchor=(0.25,1))
    
###############################################################################

def plot_avh(num_it=100000):
    ''' Plots the average height of the pile against system size.'''
    
    lengths = [8, 16, 32, 64, 128, 256]
    hlist = []
    
    if load == 0:
        for L in lengths:
            m = cp.oslo(L, num_it)
            hlist.append(cp.height_av(m[2],m[3],L))
            
    else:
        hlist.append(cp.height_av(d8[2],d8[3],lengths[0]))
        hlist.append(cp.height_av(d16[2],d16[3],lengths[1]))
        hlist.append(cp.height_av(d32[2],d32[3],lengths[2]))
        hlist.append(cp.height_av(d64[2],d64[3],lengths[3]))
        hlist.append(cp.height_av(d128[2],d128[3],lengths[4]))
        hlist.append(cp.height_av(d256[2],d256[3],lengths[5]))

    plt.figure()
    plt.plot(lengths, hlist, 'x-')
    plt.title('Average height vs system size')
    plt.xlabel('System size, L')
    plt.ylabel('Time-averaged height, <h>')

###############################################################################

def plot_stdev(num_it=100000):
    ''' Plots the standard deviation of the system height in the recurrent stage
    against the system size.'''

    lengths = [8, 16, 32, 64, 128, 256]
    dev_list = []
    
    if load == 0:
        for L in lengths:
            m = cp.oslo(L, num_it)
            dev_list.append(cp.stdev(m[2],m[3],L))
    
    else:
        for d in data_set:
            dev_list.append(cp.stdev(d[2],d[3],lengths[data_set.index(d)]))
    
    
    plt.figure()
    print dev_list
    plt.plot(lengths, dev_list, 'x-')
    plt.title('Standard Deviation against system size')
    plt.xlabel('System size, L')
    plt.ylabel('Standard Deviation')

###############################################################################    
    
def plot_height_probs(num_it=70000):
    '''Plots the height probability against height for each system size.'''
    plt.figure()
    
    if load == 0:    
                
        m = cp.oslo(8, num_it)
        x,y = cp.height_prob(m[3])
        plt.plot(x, y, label='L=8')
        
        m = cp.oslo(16, num_it)
        x,y = cp.height_prob(m[3])
        plt.plot(x, y, label='L=16')
        
        m = cp.oslo(32, num_it)
        x,y = cp.height_prob(m[3])
        plt.plot(x, y, label='L=32')
        
        m = cp.oslo(64, num_it)
        x,y = cp.height_prob(m[3])
        plt.plot(x, y, label='L=64')
        
        m = cp.oslo(128, num_it)
        x,y = cp.height_prob(m[3])
        plt.plot(x, y, label='L=128')
        
        m = cp.oslo(256, num_it)
        x,y = cp.height_prob(m[3])
        plt.plot(x, y, label='L=256')
        
    else:
        
        x,y = cp.height_prob(d8[3])
        plt.plot(x, y, label='L=8')
        
        x,y = cp.height_prob(d16[3])
        plt.plot(x, y, label='L=16')
        
        x,y = cp.height_prob(d32[3])
        plt.plot(x, y, label='L=32')
        
        x,y = cp.height_prob(d64[3])
        plt.plot(x, y, label='L=64')
        
        x,y = cp.height_prob(d128[3])
        plt.plot(x, y, label='L=128')
        
        x,y = cp.height_prob(d256[3])
        plt.plot(x, y, label='L=256')        
    
    
    plt.legend()
    plt.title('Height Probability P(h;L) against height', fontsize='large')
    plt.xlabel('Height, h', fontsize='large')
    plt.ylabel('P(h;L)', fontsize='large')

###############################################################################

def plot_avalanches():
    ''' Plots the avalanche size probability against s.'''
    
    model = cp.oslo(256,2000000)
    x,y,z = cp.avalanche_prob(model[1],model[2],256)
    
    plt.subplot(311)    
    plt.loglog(x[:10000], y[:10000], 'x', label=r'N=$10^4$')
    plt.title('Avalanche Size Probability P(s;L) against s for L = 256')
    plt.legend()
    
    plt.subplot(312)
    plt.loglog(x[:100000], y[:100000], 'x', label=r'N=$10^5$')
    plt.ylabel('P(s;L)')
    plt.legend()
    
    plt.subplot(313)
    plt.loglog(x[:1000000], y[:1000000], 'x', label=r'N=$10^6$')
    plt.xlabel('Avalanche sizes, s')            
    plt.legend()
    

###############################################################################

def plot_log_bins():
    ''' Plots the log-binned avalanche size probabilities for each system size.'''
    
    plt.figure()
    
    x,y = cp.log_binning(d8[1], 1.5)
    plt.loglog(x, y, label='L=8')
            
    x,y = cp.log_binning(d16[1], 1.5)
    plt.loglog(x, y, label='L=16')

    x,y = cp.log_binning(d32[1], 1.5)
    plt.loglog(x, y, label='L=32')
    
    x,y = cp.log_binning(d64[1], 1.5)
    plt.loglog(x, y, label='L=64')
    
    x,y = cp.log_binning(d128[1], 1.5)
    plt.loglog(x, y, label='L=128')
    
    x,y = cp.log_binning(d256[1], 1.5)
    plt.loglog(x, y, label='L=256')
    
    plt.legend()
    plt.title('Binned Avalanche Probability P(s;L) against s')
    plt.xlabel('Avalanche sizes, s')
    plt.ylabel('Binned P(s;L)')

###############################################################################    
    
def FSS(tau, D):
    ''' Data collapse of the binned avalanche size probabilities to confirm the
    finite-size scaling (FSS) ansatz.'''
    
    plt.figure()
    
    x,y = cp.log_binning(d8[1], 1.5)
    x1,y1 = cp.FSSA(x,y,tau,D,8)
    plt.loglog(x1,y1, label='L=8')
            
    x,y = cp.log_binning(d16[1], 1.5)
    x1,y1 = cp.FSSA(x,y,tau,D,16)
    plt.loglog(x1,y1, label='L=16')

    x,y = cp.log_binning(d32[1], 1.5)
    x1,y1 = cp.FSSA(x,y,tau,D,32)
    plt.loglog(x1,y1, label='L=32')
    
    x,y = cp.log_binning(d64[1], 1.5)
    x1,y1 = cp.FSSA(x,y,tau,D,64)
    plt.loglog(x1,y1, label='L=64')
    
    x,y = cp.log_binning(d128[1], 1.5)
    x1,y1 = cp.FSSA(x,y,tau,D,128)
    plt.loglog(x1,y1, label='L=128')
    
    x,y = cp.log_binning(d256[1], 1.5)
    x1,y1 = cp.FSSA(x,y,tau,D,256)
    plt.loglog(x1,y1, label='L=256')
    
    plt.legend(bbox_to_anchor=(0.25,0.41))
    plt.title('Binned Avalanche Probability P(h;L) against s')
    plt.xlabel('Avalanche sizes, s')
    plt.ylabel('Binned P(h;L)')
    
###############################################################################

def plot_moments():
    ''' Moment analysis of the avalanche size probability to estimate D and tau.'''
    
    lengths = [8,16,32,64,128,256]
    k = [1,2,3,4,5]
    slopes = []
    
    plt.figure()
    
    moments = [cp.moment_k(d[1],1) for d in data_set]
    slope, intercept = np.polyfit(np.log(lengths), np.log(moments), 1)
    slopes.append(slope)
    plt.loglog(lengths,moments, 'x-', label='k=1')

    moments = [cp.moment_k(d[1],2) for d in data_set]
    slope, intercept = np.polyfit(np.log(lengths), np.log(moments), 1)
    slopes.append(slope)
    plt.loglog(lengths,moments, 'x-', label='k=2')

    moments = [cp.moment_k(d[1],3) for d in data_set]
    slope, intercept = np.polyfit(np.log(lengths), np.log(moments), 1)
    slopes.append(slope)
    plt.loglog(lengths,moments, 'x-', label='k=3')

    moments = [cp.moment_k(d[1],4) for d in data_set]
    slope, intercept = np.polyfit(np.log(lengths), np.log(moments), 1)
    slopes.append(slope)
    plt.loglog(lengths,moments, 'x-', label='k=4')

    moments = [cp.moment_k(d[1],5) for d in data_set]
    slope, intercept = np.polyfit(np.log(lengths), np.log(moments), 1)
    slopes.append(slope)
    plt.loglog(lengths,moments, 'x-', label='k=5')
    
    plt.legend()
    plt.title(r'log($<s^k>$) vs log(L)')
    plt.xlabel('Lengths, L')
    plt.ylabel(r'$<s^k>$')
    
    plt.figure()
    plt.plot(k,slopes,'o-')
    plt.title(r'D(1+k-$\tau_s$) vs k')
    plt.xlabel('k',fontsize='large')
    plt.ylabel(r'D(1+k-$\tau_s$)',fontsize='large')
