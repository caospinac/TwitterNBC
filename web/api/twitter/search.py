from web.api import API
from web.api.twitter.util import TwitterAPI
from web.core import app
from classifiers.nbc import NaiveBayesClassifier


class TwitterSearch(API):
    def __init__(self):
        self.twitter = TwitterAPI()

    def get(self, request):
        q = request.raw_args.get("q", "")
        count = request.raw_args.get("count", 12)
        lang = request.raw_args.get("lang", "en")
        if q == "":
            return self.response(400)

        r = self.twitter.search(
            q=q,
            lang=lang,
            count=count
        )
        return self.json(data=r, count=count)


app.add_route(TwitterSearch.as_view(), "/v1/twitter/search")
