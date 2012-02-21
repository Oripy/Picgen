# -*- coding: utf-8 -*-
"""
Create functions that output pseudo-random numbers
"""

# Range of the random numbers
m = 2**25
# a-1 is divisible by all prime factors of m,
# a-1 is a multiple of 4 if m is a multiple of 4
a = 184513*4+1
# c and m are relatively prime (pgcd(c, m) = 1)
c = 1640393*2+1

# Linear congruential generator
def next_rand_LCG(prev):
    """ Returns the next random number. """       
    return (a * prev + c) % m

def rand_LCG(n):
    """ Returns the nth random number. """
    return (a**n - 1)/(a - 1) * c % m

if __name__ == "__main__":
    def pgcd(a, b):
        if a < b:
            a, b = b, a
        while True:
            r = a%b
            if r != 0:
                a = b
                b = r
            else:
                break
        return b
    print "- Parameters -"
    print "a: {}".format(a)
    print "c: {}".format(c)
    print "m: {}".format(m)
    print ""
    
    print "- Tests of the parameters -"
    good_a = True
    # a-1 is a multiple of 4 if m is a multiple of 4
    if (m % 4) == 0:
        if ((a-1) % 4) != 0:
            print "Error, a-1 must be a multiple of 4 if m is a multiple of 4"
            good_a = False
    
    # a-1 is divisible by all prime factors of m
    prime_factors = [2]
    for p in prime_factors:
        if ((a-1) % p) != 0:
            print "a-1 not divisible by {}".format(p)
            print "Error, a-1 must be divisible by all prime factors of m"
            good_a = False
    
    if good_a:
        print "a: Ok"
    
    # c and m are relatively prime (pgcd(c, m) = 1)
    if pgcd(c, m) != 1:
        print "b"
        print "Error, c and m must be relatively prime (pgcd(c, m) = 1)"
    else:
        print "c: Ok"
    
    # Potential "s"
    s = 0
    while True:
        s += 1
        if (a-1)**s % m == 0:
            break
    # If "s" < 5, generator is not random enough
    print "potential s = {}".format(s)
    if s < 5:
        print "Warning, generator not random enough"
    else:
        print "s: Ok (generator can be random enough, other tests needed)"
        
    print ""
    print "- Tests next_rand_LCG -"
    X0 = 0 # Seed
    print "Seed: {}".format(X0)
    Xi = X0
    for i in xrange(10):
        print "{}: {}".format(i, Xi)    
        Xi = next_rand_LCG(Xi)
    print ""
    print "- Tests rand_LCG -"
    for i in xrange(10):
        print "{}: {}".format(i, rand_LCG(i))
    
