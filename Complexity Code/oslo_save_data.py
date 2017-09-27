import complexity_project as cp
import cPickle as pickle

d1 = cp.oslo(8,1000000)
print "d1 done!"
d2 = cp.oslo(16,1000000)
print "d2 done!"
d3 = cp.oslo(32,1000000)
print "d3 done!"
d4 = cp.oslo(64,1000000)
print "d4 done!"
d5 = cp.oslo(128,1000000)
print "d5 done!"
d6 = cp.oslo(256,1000000)
print "d6 done!"

oslo_data = [d1, d2, d3, d4, d5, d6]

pickle.dump(oslo_data, open( "oslo_data_2.p", "wb"))
print "Dump successful!"