"""
This file contains the configuration for the inference process.
"""

import torch

class cfg:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model_dir = 'model.pth'