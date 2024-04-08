import numpy as np
import random

def mc_random_Q(simulator):
    """
    Please modify the body of this function according to the description in exercise 3.1
    """
    Q = np.zeros(2)
    n = np.zeros(2) 
    i = 0
    while i < 10_000:
        simulator.reset() 
        R = 0
        K = simulator.getNumActions()
        a = random.randint(0,K-1)
        if a == 1 :
            (r, y, done) = simulator.step(1)
            R += r
        else:
            (r, y, done) = simulator.step(-1)
            R += r

        while (done != True) & (i < 10_000):
            K = simulator.getNumActions()
            b = random.randint(0,K-1)
            
            if (b == 1):
                (r, y, done) = simulator.step(1)
                R += r
            else:
                (r, y, done) = simulator.step(-1)
                R += r

            i += 1

        n[a] += 1
        Q[a] += R
        i += 1

    for i in range(len(Q)):
        if(n[i] != 0):
            Q[i] = Q[i]/n[i]

    return Q

class Tree:
    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None
        self.Q = 0
        self.n = 0


def mc_uct_Q(simulator):
    """
    Please modify the body of this function according to the description in exercise 3.2
    """ 
    i = 0
    beta = 2
    V0 = Tree()
    current = V0
    while i < 10_000:
        simulator.reset() 
        current = V0
        R = 0 
        done = False
        while(current.left != None) & (current.right != None) & (i < 10_000) & (done != True):
            na = 0
            Q = np.zeros(2)
            n = np.zeros(2) 
            mu = np.zeros(2)
            Q[0] = current.left.Q
            Q[1] = current.right.Q
            n[0] = current.left.n
            n[1] = current.right.n

            for j in range(len(Q)):
                if(n[j]!= 0):
                    mu[j] = Q[j]/n[j]
                    na += n[j]
            a = 0
            max = 0
            for j in range(len(Q)):
                if (n[j] != 0) & (na != 0):
                    tmp = mu[j] + beta * np.sqrt((2 * np.log(na) / n[j]) )
                    if tmp > max :
                        max = tmp
                        a = j

            if (a == 0) & (done != True) & (i < 10_000) :
                current = current.left
                (r, y, done) = simulator.step(-1)
                R += r
                i += 1
                
                
            else:
                if(done != True) & (i < 10_000):
                    current = current.right
                    (r, y, done) = simulator.step(1)
                    R += r
                    i += 1
                    

        if (current.left == None) & (done != True) & (i < 10_000):
            vl = Tree()
            vl.parent = current
            current.left = vl
            (r, y, done) = simulator.step(-1)
            R += r
            i += 1    
        else:
            if(done != True) & (i < 10_000):
                vl = Tree()
                vl.parent = current
                current.right = vl
                (r, y, done) = simulator.step(1)
                R += r
                i += 1
                
        while (done != True) & (i < 10_000):
            K = simulator.getNumActions()
            b = random.randint(0,K-1)
            
            if (b == 1):
                (r, y, done) = simulator.step(1)
                R += r
            else:
                (r, y, done) = simulator.step(-1)
                R += r

            i += 1

        if(vl != None):
            vl.n +=1
            vl.Q +=R
                
        while current != V0:
            current.n += 1
            current.Q += R
            current = current.parent

        i += 1
    Q = np.zeros(2)
    n = np.zeros(2) 
    Q[0] = V0.left.Q
    Q[1] = V0.right.Q
    n[0] = V0.left.n
    n[1] = V0.right.n
        
    for j in range(len(Q)):
        if(n[j] != 0):
            Q[j] = Q[j]/n[j]

    return Q
    
