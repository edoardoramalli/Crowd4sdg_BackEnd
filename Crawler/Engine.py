import tweepy
import time
import datetime
import pandas as pd

## CONNECT TO TWITTER API:

# consumer_key = 'BIIA4eAxf6UkpSNtxAEZLciUn'
# consumer_secret = 'gaXrea9UecJ61XXgvIhDHstjE6QhfNhgMoiFeD2S7LTWjnkKBJ'


def authenticate(consumer_key, consumer_secret):
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


# if (not api):
#     print("CANNOT authenticate with Twitter API")
# else:
#     print("Twitter API authentication successful!")


## crawl() function returns a Pandas DataFrame

def crawl(api, query, count):
    # modify query to filter retweets and require images
    searchQuery = query
    searchQuery += ' -filter:retweets'  # don't retrieve retweets
    searchQuery += ' filter:images'  # only retrieve tweets containing images
    # print("Query: ", searchQuery)

    # settings:
    maxTweets = count
    tweetsPerQry = 100  # Number of tweets retrieved each request (100 is maximum)

    # variables:
    twts = []  # tweets recovered thus far
    max_id = -1  # smallest tweet id amongst recovered set
    ids = set()  # tweet ids already seen
    urls = set()  # image urls already seen

    # print("Downloading max {0} tweets".format(maxTweets))

    while len(twts) < maxTweets:
        try:

            if (max_id <= 0):  # start from the most recent tweet
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry, tweet_mode='extended')
            else:  # start from tweet with id = max_id - 1
                new_tweets = api.search(q=searchQuery, count=tweetsPerQry, max_id=str(max_id - 1),
                                        tweet_mode='extended')

            # stop if no more tweets are found
            if not new_tweets:
                # print("No more tweets found")
                break

            # extract information from tweets
            for tweet in new_tweets:

                # retrieve tweet info
                tweetInfo = {}
                tweetInfo['id'] = tweet.id
                tweetInfo['id_str'] = tweet.id_str
                tweetInfo['created_at'] = tweet.created_at
                tweetInfo['language_code'] = tweet.metadata['iso_language_code']
                tweetInfo['full_text'] = tweet.full_text

                # check if tweet id is new (possibly not necessary)
                if tweetInfo['id'] in ids:
                    continue
                ids.add(tweetInfo['id'])

                # check if image is present
                if 'media' in tweet.entities:
                    tweetInfo['media_url'] = tweet.entities['media'][0]['media_url']
                    tweetInfo['type'] = tweet.entities['media'][0]['type']

                    # check if image url is new (possibly not necessary)
                    if tweetInfo['media_url'] in urls:
                        continue
                    urls.add(tweetInfo['media_url'])

                # check if tweet location is available
                if tweet.place != None:
                    tweetInfo['country'] = tweet.place.country
                    tweetInfo['country_code'] = tweet.place.country_code
                    tweetInfo['bounding_box'] = tweet.place.bounding_box.coordinates[0]
                else:
                    tweetInfo['country'] = 'None'
                    tweetInfo['country_code'] = 'None'
                    tweetInfo['bounding_box'] = 'None'

                # check if user location is available
                if tweet.user.location != None:
                    tweetInfo['user_loc'] = tweet.user.location
                else:
                    tweetInfo['user_loc'] = 'None'

                twts.append(tweetInfo)

            # print("Downloaded {0} tweets (completed: {1:.2f}%)".format(len(twts), len(twts) / maxTweets * 100))

            # update max_id with the last retrieved tweet
            max_id = new_tweets[-1].id

        except tweepy.TweepError as e:
            return e

    # print("downloaded {0} tweets".format(len(twts)))

    return pd.DataFrame(twts)


def crawl_CSV(api, query, count):
    return crawl(api, query, count).to_csv(None, index=False)