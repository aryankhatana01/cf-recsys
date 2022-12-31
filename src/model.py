import torch
import torch.nn as nn
import torch.nn.functional as F

class RecSysModel(nn.Module):
    def __init__(self, n_users, n_movies, n_factors=50):
        super(RecSysModel, self).__init__()
        self.user_factors = nn.Embedding(n_users, n_factors) # n_users = 610, n_factors = 50
        self.movie_factors = nn.Embedding(n_movies, n_factors) # n_movies = 9724, n_factors = 50
        self.output = nn.Linear(n_factors, 1) # n_factors = 50, 1
        
    def forward(self, user_id, movie_id):
        user_factors = self.user_factors(user_id)
        movie_factors = self.movie_factors(movie_id)
        out = torch.cat([user_factors, movie_factors], dim=1)
        out = self.output(out)
        # if rating is not None:
        #     loss = F.mse_loss(out, rating.view(-1, 1))
        #     return loss
        return out