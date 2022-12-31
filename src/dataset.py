import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader


class MovieDataset(Dataset):
    """
    Movie Dataset

    movieId:
    List of movie ids

    userId:
    List of user ids

    rating:
    List of ratings

    return:
    Dictionary of movieId, userId, rating
    """
    def __init__(self, movieId, userId, rating):
        self.movieId = movieId
        self.userId = userId
        self.rating = rating

    def __len__(self):
        return len(self.movieId)

    def __getitem__(self, idx):
        user_id = self.userId[idx]
        movie_id = self.movieId[idx]
        rating = self.rating[idx]
        return {
            'user_id': torch.tensor(user_id, dtype=torch.long),
            'movie_id': torch.tensor(movie_id, dtype=torch.long),
            'rating': torch.tensor(rating, dtype=torch.float)
        }