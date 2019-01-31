import tweepy
from newsapi.newsapi_client import NewsApiClient
from secrets import *
import requests
import json


def search(api, query_string):
    search = api.search(q=query_string)
    for result in search:
        print(result.text)

def get_followers_last_tweet(api):
    followers = api.followers_ids()
    for f in followers:
        try:
            user_timeline = api.user_timeline(f)
            if user_timeline.__len__() > 0:
                status_id = user_timeline[0].id
                print(api.get_status(status_id))
        except tweepy.error.TweepError:
            continue

def get_top_articles(newsapi):
    top_headlines = newsapi.get_top_headlines(language='en', country='us')
    return top_headlines


def tweet_top_articles(twitter_api, articles_dict):
    for article in articles_dict['articles']:
        try:
            title = article['title'].rsplit('-',1)[0]
            url = get_short_url(article['url'])
            name = article['source']['name'].rsplit('.com',1)[0]
            tweet_string = title + "\n" +  url + " \nSource: "+ name
            print(tweet_string)
            print(len(tweet_string))
            #twitter_api.update_status(tweet_string)
        except (KeyError, TypeError) as e:
            continue

def get_short_url(url):
    try:
        api_url = 'https://api.rebrandly.com/v1/links?apikey='+rebrandly_key
        headers = {'Content-type': 'application/json'}
        data = {"destination": url}
        response = requests.post(api_url, data=json.dumps(data), headers=headers)
        url_dict = json.loads(response.text)
        return url_dict['shortUrl']
    except KeyError:
        return KeyError

def main():
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)
    twitter_api = tweepy.API(auth)


    newsapi = NewsApiClient(api_key=news_api_key)


    articles = get_top_articles(newsapi)
    tweet_top_articles(twitter_api, articles)



if __name__ == '__main__':
    main()