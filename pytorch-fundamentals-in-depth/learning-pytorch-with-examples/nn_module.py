# nn module
# For large neural networks, raw autograd can be a bit too low-level
# Use of the nn package that defines a set of Modules

import torch

N, D_in, H, D_out = 64, 1000, 100, 10

x = torch.randn(N, D_in)
y = torch.randn(N, D_out)

model = torch.nn.Sequential(
        torch.nn.Linear(D_in, H),
        torch.nn.ReLU(),
        torch.nn.Linear(H, D_out),
)

loss_fn = torch.nn.MSELoss(reduction='sum')

learning_rate = 1e-4
for t in range(500):
  y_pred = model(x)

  loss = loss_fn(y_pred, y)
  print(t, loss.item())

  model.zero_grad()

  loss.backward()

  with torch.no_grad():
    for param in model.parameters():
      param -= learning_rate * param.grad

# To use more sophisticated optimizers, we can use the optim package
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
for t in range(500):
  y_pred = model(x)

  loss = loss_fn(y_pred, y)
  print(t, loss.item())

  optimizer.zero_grad()

  loss.backward()

  optimizer.step()

# We can define our own Modules by subclassing nn.Module and defining a forward function

class TwoLayerNet(torch.nn.Module):
  def __init__(self, D_in, H, D_out):
    super(TwoLayerNet, self).__init__()
    self.linear1 = torch.nn.Linear(D_in, H)
    self.linear2 = torch.nn.Linear(H, D_out)

  def forward(self, x):
    h_relu = self.linear1(x).clamp(min=0)
    y_pred = self.linear2(h_relu)
    return y_pred
