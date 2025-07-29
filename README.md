# Faitelbot

Anyone that has been around Mexico's twitter football community is aware of the Faitelson phenomenon on this social network. When ever [David Faitelson](https://x.com/DavidFaitelson_), one of the most popular sports commentators on the country, tweets about anything (from a football match to what he is having for lunch), that tweet will be filled with hundred of replies reminding him about a very specific event that occurred one hot evening in the Port of Veracruz...

> This repo's goal is build a Twitter bot so we never forget what happened that day in Veracruz.

Steps followed:
1. Extract Faitelson Tweets and their replies: [Notebook](./get_tweets.ipynb)
2. Perform Exploratory data analysis on the tweets and replies: [Notebook](./EDAV.ipynb)
3. Build a training set to train a LLM: [Notebook](./create_training_set.ipynb)
4. Train a LLM to generate funny replies to Faitelson's tweets
5. Deploy a model that would:
    1. Check for Faitelson tweets in the last hour
    2. Generate funny replies to all found tweets
    3. Push those replies to Twitter