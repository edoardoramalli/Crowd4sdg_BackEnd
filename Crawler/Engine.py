import tweepy
import time
import datetime
import pandas as pd


def authenticate(consumer_key, consumer_secret):
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def crawl(api, query, count):
    '''
    q –
    he search query string of 500 characters maximum, including operators.
    Queries may additionally be limited by complexity

    geocode -
    Returns tweets by users located within a given radius of the given latitude/longitude.
    The location is preferentially taking from the Geotagging API, but will fall back to their Twitter profile. The parameter value is specified by “latitide,longitude,radius”, where radius units must be specified as either “mi” (miles) or “km” (kilometers). Note that you cannot use the near operator via the API to geocode arbitrary locations; however you can use this geocode parameter to search near geocodes directly.
    A maximum of 1,000 distinct “sub-regions” will be considered when using the radius modifier.

    lang -
    Restricts tweets to the given language, given by an ISO 639-1 code. Language detection is best-effort.

    locale -
    Specify the language of the query you are sending (only ja is currently effective).
    This is intended for language-specific consumers and the default should work in the majority of cases.

    result_type -
    Specifies what type of search results you would prefer to receive.
    The current default is “mixed.” Valid values include:
        mixed : include both popular and real time results in the response
        recent : return only the most recent results in the response
        popular : return only the most popular results in the response

    count -
    The number of results to try and retrieve per page.

    until -
    Returns tweets created before the given date. Date should be formatted as YYYY-MM-DD.
    Keep in mind that the search index has a 7-day limit.
    In other words, no tweets will be found for a date older than one week.

    since_id -
    Returns only statuses with an ID greater than (that is, more recent than) the specified ID.
    There are limits to the number of Tweets which can be accessed through the API.
    If the limit of Tweets has occurred since the since_id, the since_id will be forced to the oldest ID available.

    max_id -
    Returns only statuses with an ID less than (that is, older than) or equal to the specified ID.

    include_entities -
    The entities node will not be included when set to false. Defaults to true.


    :param api:
    :param query:
    :param count:
    :return:
    '''

    # modify query to filter retweets and require images
    searchQuery = query
    searchQuery += ' -filter:retweets'  # don't retrieve retweets
    searchQuery += ' filter:images'  # only retrieve tweets containing images
    # print("Query: ", searchQuery)

    # settings:
    maxTweets = count
    tweetsPerQry = min(100, count)  # Number of tweets retrieved each request (100 is maximum)

    # variables:
    twts = []  # tweets recovered thus far
    max_id = -1  # smallest tweet id amongst recovered set
    ids = set()  # tweet ids already seen
    urls = set()  # image urls already seen

    # print("Downloading max {0} tweets".format(maxTweets))

    while len(twts) < maxTweets:
        try:

            if (max_id <= 0):  # start from the most recent tweet
                new_tweets = api.search(q=searchQuery,
                                        count=tweetsPerQry,
                                        tweet_mode='extended')
            else:  # start from tweet with id = max_id - 1
                new_tweets = api.search(q=searchQuery,
                                        count=tweetsPerQry,
                                        max_id=str(max_id - 1),
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