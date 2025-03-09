import torch

a = torch.full(size=(3, 3), fill_value=12, dtype=torch.float16, device='cpu', requires_grad=False)
print(a)
print(type(a))