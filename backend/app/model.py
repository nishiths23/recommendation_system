
import pickle
from typing import List
import pandas as pd
from fastapi import APIRouter
from fastapi import Query
from pydantic import BaseModel
import collections
from fastapi.responses import JSONResponse

#APIRouter creates path operations for predict module
router = APIRouter(
    prefix="/predict",
    responses={404: {"description": "Not found"}},
)

class Item(BaseModel):
    username: str

def flatten(x):
    if isinstance(x, collections.Iterable):
        return [a for i in x for a in flatten(i)]
    else:
        return [x]

@router.get('/product/')
async def predict(username: str):
    '''
    Predicting the top recommended products using best ML models
    '''
    list_data: List = []
    
    # load all input files
    review_df_file = open('./data/product_review.pkl', 'rb')
    review_df = pickle.load(review_df_file)

    sentiment_clean_df_file = open('./data/sentiment_df.pkl', 'rb')
    sentiment_clean_df = pickle.load(sentiment_clean_df_file)

    user_reco_file = open('./pickle/user_recommendation.pkl', 'rb')
    user_reco_table = pickle.load(user_reco_file)

    sentiment_model_file = open('./pickle/Sentiment_model.pkl', 'rb')
    sentiment_model = pickle.load(sentiment_model_file)

    tfidf_file = open('./pickle/tfidf_vectorizer.pkl', 'rb')
    tfidf_vector = pickle.load(tfidf_file)

    # check for valid username
    if username in user_reco_table.index:

        top20_product_ids = user_reco_table.loc[username].sort_values(ascending=False)[:20]
        product_map = pd.DataFrame(review_df[['id','name']]).drop_duplicates()
        top20_products = pd.merge(top20_product_ids, product_map, on='id')

        # Mapping product with product reviews
        product_mapping_review = pd.DataFrame(sentiment_clean_df[['id','text_data','user_sentiment']]).drop_duplicates()
        product_review_data =pd.merge(top20_products, product_mapping_review, on='id')

        # get features using tfidf vectorizer
        test_features= tfidf_vector.transform(product_review_data['text_data'])

        # Predict Sentiment Score on the above Product Reviews using the finally selected ML model
        product_review_data['predicted_sentiment'] = sentiment_model.predict(test_features)
        product_review_data['predicted_sentiment_score'] = product_review_data['predicted_sentiment'].replace(['negative','positive'],[0,1])

        # Find positive sentiment percentage for every product
        product_pivot = product_review_data.reset_index().pivot_table(values='predicted_sentiment_score', index='name', aggfunc='mean')
        product_pivot.sort_values(by='predicted_sentiment_score',inplace= True, ascending= False)
        
        # Get top 5 products
        # list_data = [{ 'index': index, 'name': out} for index, out in enumerate (product_pivot.head(5).index, 1)]
        list_data = [{'score': row, 'name': index } for index, row in product_pivot.head(5).itertuples()]


    return JSONResponse(content= list_data if len(list_data) > 0 else [],
    headers={
        "Access-Control-Allow-Origin": "*", 
        "Access-Control-Allow-Credentials": "true",
        "content-type":"application/json"
    }) 
