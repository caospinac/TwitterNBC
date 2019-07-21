from web.api import API
from web.api.twitter.util import TwitterAPI
from web.core import app
from classifiers.nbc import NaiveBayesClassifier


class TwitterSearch(API):
    def __init__(self):
        self.twitter = TwitterAPI()
        self.nbc = NaiveBayesClassifier()

    def get(self, request):
        q = request.raw_args.get('q', "")
        try:
            count = int(request.raw_args.get('count'))
        except ValueError:
            count = 12

        lang = request.raw_args.get('lang', "en")
        classify = request.raw_args.get('classify', "false")
        class_field = request.raw_args.get('class_field', "text")

        if q == "":
            return self.response(400)

        r = self.twitter.search(
            q=q,
            lang=lang,
            count=count
        )
        if classify == "true":
            for tweet in r:
                text = tweet.get(class_field)
                if not text:
                    continue

                tweet['nbc'] = self.nbc.classify_naive_bayes_text(text)

        return self.json(data=r, count=count)


app.add_route(TwitterSearch.as_view(), "/v1/twitter/search")
