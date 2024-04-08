import matplotlib.pyplot as plt
import numpy as np

def regression_based_on_data(l, u, a, y):
    """
    Please modify the body of this function according to the description in exercise 2.1
    """
    Dja = [] 
    Djy = [] 
    a_est_j = []
    x_y = []
    x_mu = []
    x_sigma = []
    x_s = []
    F = 7

    for j in range(len(a)):
        Dja.append(bootstrapping(a,j))
        Djy.append(bootstrapping(y,j))

    for j in range(len(Dja)):
        a_est_j.append(a_est(Dja[j],Djy[j],F))

    x = l 

    for j in range(1):

        while x <= u:
            x_s.append(x)
            y_mu = 0
            y_sigma = 0
            x_y = []
            for i in range(len(a_est_j)):
                x_y.append(f_est_c(F,x,a_est_j[i]))
                y_mu += f_est_c(F,x,a_est_j[i])

            y_mu = y_mu / len(a_est_j)
            x_mu.append(y_mu)

            for i in range(len(x_y)):
                y_sigma += ((x_y[i] + y_mu)**2)

            y_sigma = np.sqrt(y_sigma / (len(x_y)-1))
            x_sigma.append(y_sigma)
            x += 0.1 * (u-l) 
    
        max = x_mu[0] + 2 * x_sigma[0]
        for i in range(len(x_mu)):
            if (x_mu[i] + 2 * x_sigma[i] > max):
               max = x_mu[i] + 2 * x_sigma[i]
               x = x_s[i]

    return x
   


def phi(k,a):
    return a**k

def f_est_c(F, a, a_est):
    f = 0.0
    for k in range(F):
        f += a_est[k]*phi(k,a)
    return f

def bootstrapping(a,j):
    b_a = np.zeros(len(a)-1)
    hit = False
    for i in range(len(a)):
        if( hit == False):
            if(i != j):
                b_a[i] = a[i]
            else:
                hit = True
        else:
            b_a[i-1] = a[i]

    return b_a


def a_est(a, y, F):
    A = np.zeros((len(a),F))
    f_est = np.zeros((len(a)))

    for i in range(len(a)):
        for j in range(F):
            A[i][j] = phi(j,a[i])

    AT = np.transpose(A)

    AI = np.matmul(AT,A)

    AI = np.linalg.inv(AI)

    A = np.matmul(AI,AT)

    a_est = np.dot(A,y)

    return a_est