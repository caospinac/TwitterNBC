from web.api import API
from web.core import app
from classifiers.nbc import NaiveBayesClassifier


class NaiveBayesClassifierAPI(API):
    def __init__(self):
        self.nbc = NaiveBayesClassifier()

    def get(self, request):
        text = request.raw_args.get("t", None)
        if text == "":
            return self.response(400)

        if text is None:
            return self._json("You can send a text through 't' argument in "
                              "the URL. E.g., '/api/nbc?t=I have a problem'")

        r = self.nbc.classify_naive_bayes_text(text)
        return self.json(data=r)


app.add_route(NaiveBayesClassifierAPI.as_view(), "/api/nbc")
