import tweepy
import yaml
import telegram
from telegram.error import NetworkError, Unauthorized

# Load cfg
with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)
access_token = cfg["twitter"]["access_token"]
access_token_secret = cfg["twitter"]["access_token_secret"]
consumer_key = cfg["twitter"]["api_key"]
consumer_secret = cfg["twitter"]["api_secret"]
bot_token = cfg["telegram"]["bot_token"]
chat_id = cfg["telegram"]["chat_id"]
queries = cfg["queries"]
max_results = cfg["twitter"]["max_results"]



bot = telegram.Bot(bot_token)


# Init Tweepy
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)


# Search and notify new tweets to Telegram

for query in queries:
    q = queries[query]["query"]
    since_id = queries[query]["since_id"]
    tweets = api.search(q, maxResults=max_results, since_id=since_id)[::-1]
    
    if tweets:
        for tweet in tweets:
            link = "https://twitter.com/sad/status/{}".format(tweet.id_str)
            bot.send_message(chat_id=chat_id, parse_mode=telegram.ParseMode.MARKDOWN, text='New tweet from query: "_{}_":\n\n```\t{}```\n\n\n[Link]({})'.format(q, tweet.text, link))

        cfg["queries"][query]["since_id"] = tweets[-1].id_str

if queries:
    with open("config.yml", 'w') as yaml_file:
        yaml_file.write( yaml.dump(cfg, default_flow_style=False))
        yaml_file.close()
