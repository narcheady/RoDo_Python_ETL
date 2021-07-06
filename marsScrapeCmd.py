import pandas as pd
# from twitter import Twitter
# from twitter import OAuth
import re
import matplotlib.pyplot as plt


# accesstoken = '1306383817473699840-7lOFPXnXan5KjfF2JGlepqalGq2EaX'
# accesstokensecret= 'z0wokk3M7z7A7mHJll1UAX7QlYiPUAVv1Fx62W92awpHi'
# apikey = 'LMcVqFvyJSyBSJIiusvuv2qwz'
# apisecretkey = 'ten59LiLXRwRUVbnwwBBef52GJfifUGfAxe4mpGMoiu4cMfdIN'

# oauth=OAuth(accesstoken,accesstokensecret,apikey,apisecretkey)
# api = Twitter(auth=oauth,retry=True)

# tweetList = api.search.tweets(q="marswxreport lang:en -filter:retweets",tweetmode='extended',count=100)
# tweetTable=pd.json_normalize(tweetList['statuses'])
# tweetTable = tweetTable[['text']]

import requests
from bs4 import BeautifulSoup

contents = requests.get(
    "https://twitter.com/MarsWxReport",
    headers={"User-Agent": "UCWEB/2.0 (compatible; Googlebot/2.1; +google.com/bot.html)"}
)
soup = BeautifulSoup(contents.text, "html.parser")

tweetTable = pd.DataFrame(columns=['text'])

tweets_list = list()
tweets = soup.find_all("div", {"class": "js-tweet-text-container"})

for tweet in tweets:
    tweet_text = tweet.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"}).text.replace("\n", " ").strip()
    tweetTable = tweetTable.append({'text':tweet_text}, ignore_index = True)

tweetTable['Date']=tweetTable['text'].str.extract('\(([^\)]+)\)')
tweetTable = tweetTable.dropna()
tweetTable = tweetTable.reset_index(drop=True)

for i in tweetTable.index:
    tweetTable.at[i, 'Temperature High'] = tweetTable.at[i, 'text'].split(',')[2].split('/')[0].split(' ')[-1].split('ºC')[0]
    tweetTable.at[i, 'Temperature Low'] = tweetTable.at[i, 'text'].split(',')[3].split('/')[0].split(' ')[-1].split('ºC')[0]
    tweetTable.at[i, 'Pressure'] = tweetTable.at[i, 'text'].split(',')[4].split(' ')[3]


marsExtract = tweetTable[['Date','Temperature High','Temperature Low','Pressure']]
marsExtract.to_csv('mars_weather.csv', index=False)

marsExtract.plot(kind='scatter',x='Temperature High',y='Pressure',color='red')
plt.savefig('mars_scatter_plot.png')
plt.show()