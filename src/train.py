import torch
import torch.nn as nn
import pandas as pd
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from sklearn import model_selection, preprocessing
from dataset import MovieDataset
from model import RecSysModel

def train_one_epoch(epoch, model, optimizer, scheduler, data_loader, device):
    model.train()
    final_loss = 0
    for data in data_loader:
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
        df, test_size=0.1, 
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
    model.fit(
        train_ds, 
        test_ds, 
        epochs=10, 
        train_bs=1024, 
        valid_bs=1024, 
        fp16=True,
        pin_memory=False
    )

    # # Creating DataLoader
    # train_loader = DataLoader(
    #     train_ds,
    #     batch_size=1024,
    #     num_workers=2,
    #     shuffle=True,
    #     pin_memory=True
    # )

    # valid_loader = DataLoader(
    #     test_ds,
    #     batch_size=1024,
    #     num_workers=2,
    #     pin_memory=True
    # )

    # # Defining the device
    # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # model.to(device)

    # # Defining the optimizer
    # optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    # # Defining the scheduler
    # scheduler = torch.optim.lr_scheduler.OneCycleLR(
    #     optimizer=optimizer,
    #     max_lr=1e-3,
    #     steps_per_epoch=len(train_loader),
    #     epochs=10
    # )

    # # Training the model
    # for epoch in range(10):
    #     train_one_epoch(epoch, model, optimizer, scheduler, train_loader, device)

if __name__ == "__main__":
    train()
