# Sentiment Based Product Recommendation System

Upgrad assigned capstone project

## Abstract

Given a dataset containing from an E-Commerse business about the reviews given by the users to the products, create a recommendation system that would use this data to recommend products to its users.

## Synpopsis

Reviews and ratings given by the users for the products play a vital role in purchase decisions. Suppose you want to buy a particular product from any e-commerce website. You check the reviews of that product, and if people are giving positive responses or higher ratings, then the product is considered good to buy, and if there are more negative responses or lower ratings, then it is not considered a good buy. 

 But, the recommendation system works upon how you can automate this process and then recommend the products to other users based on the previously existing reviews and ratings.

 ## Progress summary

 After basic Exploratory Data Analysis and some basic preprocessing of the given data we start creating the recommendation system

 - The first step is the NLP step where the existing reviews are analysed and a machine learning model is created to predict the user sentiment of the review (Negative or Positive)
   - For this 3 models are evaluated:
     - Logistic regression
     - Random forest
     - Naive Bayes
       - MultinomialNB
       - SGDClassifier
       - GaussianNB
       - BernoulliNB
   - Out of these models Logistic regression gives the best performance so it is selected as the user prediction model
 - Second step is to create a product recommendation model. For this 2 models are evaluates
   - User-User based
   - Item-Item based
   - Out of these User-User based model gives the best performance so it is selected
 - The third step is to use User-User based recommendation model and Logistic regression to recommend 5 products to the given users
   - For this we start by creating a list of products recommended to the user by the User-User based recommendation model
   - Then we use the Logistic regression model to predict sentiments of the user from the reviews given to those products and give a positive sentiment score
   - Third and final step is to recommend top 5 products with the best positive sentiment score
 - The last step is to present the project as a cmplete app.
   - For this a project is created that uses 
     - Python's FastAPI framework as backend
       - It contains bundled up all the models and data that was used to make the predictions
       - This backend uses REST APIs t provide a list of random users for whome the product recommendations can be made
       - 5 Product recommendations to the selected user
     - React as the frontend
       - The frontend shows a list of 5 random users for whome recommendations can be seen
       - It also takes input a username
       - After providing a user either from the list or in the field it shows a list of 5 recommended products and their positive sentiment score

## Conclusion

This repository contains the Backend, Frontend code and the Jupyter notebook associated with the project

To run the project locally execute the ```execute.sh``` file in terminal

```bash
sh execute.sh
```
