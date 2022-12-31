import torch
import torch.nn as nn
import torch.nn.functional as F

class RecSysModel(nn.Module):
    """
    RecSysModel is a class that inherits from nn.Module

    n_users:
    Total number of unique users in the dataset.

    n_movies:
    Total number of unique movies in the dataset.

    n_factors:
    Number of latent factors or embedding space to use in the model.

    returns:
    The output of the model.
    """
    def __init__(self, n_users, n_movies, n_factors=50):
        super(RecSysModel, self).__init__()
        self.user_factors = nn.Embedding(n_users, n_factors) # n_users = 610, n_factors = 50
        self.movie_factors = nn.Embedding(n_movies, n_factors) # n_movies = 9724, n_factors = 50
        self.output = nn.Linear(n_factors*2, 1) # n_factors = 100, 1
        
    def forward(self, user_id, movie_id):
        user_factors = self.user_factors(user_id)
        # print("User Embedding Shape: ",  user_factors.shape)
        movie_factors = self.movie_factors(movie_id)
        # print("Movie Embedding Shape: ",  user_factors.shape)
        out = torch.cat([user_factors, movie_factors], dim=1)
        # print("Concat Shape: ", out.shape)
        out = self.output(out)
        # print("Output Shape: ", out.shape)
        # if rating is not None:
        #     loss = F.mse_loss(out, rating.view(-1, 1))
        #     return loss
        return out