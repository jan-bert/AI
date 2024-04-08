import numpy as np
import random

def q_learning(env):
    S = env.getNumStates()
    A = env.getNumActions()
    Q = np.zeros((S,A))
    epsilon = 0.64
    alpha = 0.06
    gamma = 0.9
    i = 0
    while i < 10_000:
        y = env.reset()
        done = False
        while (i < 10_000) & (done != True): 
            ran = random.random()
            if ( ran <= 1 - epsilon):
                a = np.argmax(Q[y])
            else:
                a = random.randint(0,A-1)

            (r, y_new , done) = env.step(a)
            i += 1
            max = np.max(Q[y_new])
            Q[y][a] = Q[y][a] + alpha * (r + gamma * max - Q[y][a])
            y = y_new
    
    return Q