import torch
import torch.nn as nn
import torch.nn.functional as F
import tez
import numpy as np
from sklearn.metrics import mean_squared_error

class RecSysModel(tez.Model):
    def __init__(self, n_users, n_movies, n_factors=50):
        super(RecSysModel, self).__init__()
        self.user_factors = nn.Embedding(n_users, n_factors) # n_users = 610, n_factors = 50
        self.movie_factors = nn.Embedding(n_movies, n_factors) # n_movies = 9724, n_factors = 50
        self.output = nn.Linear(n_factors*2, 1) # n_factors = 100, 1
        self.step_scheduler_after = "epoch"

    def monitor_metrics(self, out, rating):
        out = out.cpu().detach().numpy()
        rating = rating.cpu().detach().numpy()
        return {
            "rmse": np.sqrt(mean_squared_error(out, rating)),
        }

    def fetch_optimizer(self):
        opt = torch.optim.Adam(self.parameters(), lr=1e-3)
        return opt
    
    def fetch_scheduler(self):
        sch = torch.optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, mode="min", patience=5, factor=0.3, verbose=True
        )
        return sch
        
    def forward(self, user_id, movie_id, rating=None):
        user_factors = self.user_factors(user_id)
        movie_factors = self.movie_factors(movie_id)
        out = torch.cat([user_factors, movie_factors], dim=1)
        # print(out.shape)
        out = self.output(out)
        # if rating is not None:
        loss = F.mse_loss(out, rating.view(-1, 1))
        cal_met = self.monitor_metrics(out, rating)
        return out, loss, cal_met