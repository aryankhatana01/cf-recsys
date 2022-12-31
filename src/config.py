import torch

class cfg:
    n_epochs = 10
    batch_size = 24
    lr = 1e-3
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    optimizer = torch.optim.Adam
    scheduler = torch.optim.lr_scheduler.OneCycleLR
