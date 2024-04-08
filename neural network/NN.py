import numpy as np 
import matplotlib.pyplot as plt
import torch

F = np.fromfile("dataQuadReg1D.txt", float, -1,' ',)

D = np.zeros((100,2))

for i in range (F.size):
    
        D[int(i/2)][i%2] = F[i]

T = np.zeros(100)
I = -3
for i in range (T.size):
    T[i] = I 
    I += 7/100


X = torch.from_numpy(D[:,0]).float().unsqueeze(1).requires_grad_(True)
Y = torch.from_numpy(D[:,1]).float().unsqueeze(1).requires_grad_(True)
w = torch.randn(1,16,requires_grad=True)
w2 = torch.randn(16,1,requires_grad=True)
b = torch.randn(16,requires_grad=True)
b2 = torch.randn(1,requires_grad=True)
alpha = 0.01
for i in range (1000):
    if(i%1000) == 0:
      new_X = torch.from_numpy(T).float().unsqueeze(1)
      Z1 = torch.matmul(new_X,w)+b
      New_X1 =torch.nn.functional.relu(Z1)
      Z2 = torch.matmul(New_X1,w2)+b2
      B = new_X.detach().numpy()
      C = Z2.detach().numpy()
      ay = plt.subplot()
      ay.plot(B,C)
      ax = plt.subplot()
      ax.scatter(D[:,0],D[:,1])
      plt.show()

    X1 = torch.matmul(X,w)+b
    X2 = torch.nn.functional.relu(X1)
    YPred = torch.matmul(X2,w2)+b2
    loss = (YPred - Y).square().mean()
    loss.backward()
    with torch.no_grad():   
            w.add_(w.grad.mul(-alpha))
            b .add_(b.grad.mul(-alpha))
            w2.add_(w2.grad.mul(-alpha))
            b2.add_(b2.grad.mul(-alpha)) 
            w.grad.zero_()
            b.grad.zero_()
            w2.grad.zero_()
            b.grad.zero_()



new_X = torch.from_numpy(T).float().unsqueeze(1)
Z1 = torch.matmul(new_X,w)+b
New_X1 =torch.nn.functional.relu(Z1)
Z2 = torch.matmul(New_X1,w2)+b2
B = new_X.detach().numpy()
C = Z2.detach().numpy()
ay = plt.subplot()
ay.plot(B,C)
ax = plt.subplot()
ax.scatter(D[:,0],D[:,1])
plt.show()