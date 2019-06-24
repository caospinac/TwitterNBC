import tweepy

from web.core import config


class TwitterAPI(object):

    def __init__(self):
        auth = tweepy.OAuthHandler(
            config['TWITTER']['consumer_key'],
            config['TWITTER']['consumer_secret']
        )
        auth.set_access_token(
            config['TWITTER']['access_token'],
            config['TWITTER']['access_token_secret']
        )
        self.api = tweepy.API(auth)

    def parse_fields(self, data):
        if not data:
            return None

        text = data['full_text']
        if data.get('retweeted_status'):
            text = data['retweeted_status']['full_text']

        return {
            'created_at': data['created_at'],
            '_id': data['id_str'],
            'text': text,
            'lang': data['lang'],
            'metadata': data['metadata'],
        }

    def search(self, q, lang="en", result_type="mixed", count=12,
               include_entities=False):
        cursor = tweepy.Cursor(
            self.api.search,
            q=q,
            lang=lang,
            result_type=result_type,
            include_entities=include_entities,
            tweet_mode="extended"
        )
        iter_result = (status._json for status in cursor.items(count))

        return list(map(self.parse_fields, iter_result))
