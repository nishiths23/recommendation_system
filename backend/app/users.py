from fastapi import APIRouter
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
import random
import pickle


#APIRouter creates path operations for predict module
router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)

@router.get('/randomusers')
async def getRandomUsers():
    review_df_file = open('./data/product_review.pkl', 'rb')
    review_df = pickle.load(review_df_file)
    review_df['reviews_username'] = review_df.reviews_username.astype('str')

    user_reco_file = open('./pickle/user_recommendation.pkl', 'rb')
    user_reco_table = pickle.load(user_reco_file)

    new_df = pd.merge(review_df, user_reco_table, on='reviews_username')
    new_df.head()

    ids = new_df["categories"].unique()
    ids = np.random.choice(ids, size=5, replace=False)
    ids

    new_df = new_df.loc[new_df["categories"].isin(ids)]
    
    user_df = new_df.groupby('categories').apply(lambda x: x.sample(1)).reset_index(drop=True).head(5)['reviews_username']
    users = [user for user in user_df]

    # users = [item for item in review_df['reviews_username']]
    return JSONResponse(content= random.sample(users, 5), 
    headers={
        "Access-Control-Allow-Origin": "*", 
        "Access-Control-Allow-Credentials": "true",
        "content-type":"application/json"
    })