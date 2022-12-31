import torch
import torch.nn as nn
import pandas as pd
import torch.nn.functional as F
from torch.utils.data import DataLoader
from sklearn import model_selection, preprocessing
from dataset import MovieDataset
from model import RecSysModel
from config import cfg
from tqdm import tqdm

def train_one_epoch(epoch, model, optimizer, scheduler, data_loader, device):
    model.train()
    final_loss = 0

    for data in tqdm(data_loader, total=len(data_loader)):
        user_id = data['user_id'].to(device)
        movie_id = data['movie_id'].to(device)
        rating = data['rating'].to(device)
        optimizer.zero_grad()
        output = model(user_id, movie_id)
        loss = F.mse_loss(output, rating.view(-1, 1))
        loss.backward()
        optimizer.step()
        scheduler.step()
        final_loss += loss.item()
    print(f'Epoch={epoch}, Loss={final_loss/len(data_loader)}')

def train():
    df = pd.read_csv('../input/ratingsCleaned.csv') # UserId, MovieId, Rating

    # Preprocess the data
    lbl_users = preprocessing.LabelEncoder() # Encode the user ids
    lbl_movies = preprocessing.LabelEncoder() # Encode the movie ids

    df['userId'] = lbl_users.fit_transform(df['userId'].values)
    df['movieId'] = lbl_movies.fit_transform(df['movieId'].values)

    # Split the data into train and test
    df_train, df_test = model_selection.train_test_split(
        df, 
        test_size=0.1, 
        random_state=42, 
        stratify=df['rating'].values
    )

    # Create the train dataset
    train_ds = MovieDataset(
        movieId=df_train['movieId'].values,
        userId=df_train['userId'].values,
        rating=df_train['rating'].values
    )

    # Create the test dataset
    test_ds = MovieDataset(
        movieId=df_test['movieId'].values,
        userId=df_test['userId'].values,
        rating=df_test['rating'].values
    )

    # Intitailizing the model
    model = RecSysModel(
        n_users=len(lbl_users.classes_),
        n_movies=len(lbl_movies.classes_)
    )

    # print(model)

    # Creating train DataLoader
    train_loader = DataLoader(
        train_ds,
        batch_size=cfg.batch_size,
        shuffle=True,
        pin_memory=False
    )

    # Creating validation DataLoader
    valid_loader = DataLoader(
        test_ds,
        batch_size=cfg.batch_size,
        pin_memory=False
    )

    ###### Testing Our Model for one batch ######
    # for data in train_loader:
    #     user_id = data['user_id']
    #     movie_id = data['movie_id']
    #     _ = model(user_id, movie_id)
    #     break
    #############################################

    # Defining the device
    device = cfg.device
    model.to(device)

    # Defining the optimizer
    optimizer = cfg.optimizer(model.parameters(), lr=cfg.lr)

    # Defining the scheduler
    scheduler = cfg.scheduler(
        optimizer,
        max_lr=cfg.lr,
        steps_per_epoch=len(train_loader),
        epochs=cfg.n_epochs
    )

    # Training the model
    for epoch in range(cfg.n_epochs):
        train_one_epoch(epoch, model, optimizer, scheduler, train_loader, device)

if __name__ == "__main__":
    train()
