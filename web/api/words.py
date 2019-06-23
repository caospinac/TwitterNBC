import json

from web.api import API
from web.core import app


class WordsAPI(API):

    async def get(self, request, word=None):
        per_page = request.raw_args.get("per_page", 10)
        page = request.raw_args.get("page", 1)
        try:
            per_page = int(per_page)
            page = int(page)
        except ValueError:
            per_page = 10
            page = 1

        if word:
            return self.json(self.words_collection.find_one({'value': word}))

        query_param = request.raw_args.get("q", "")
        query = {}
        try:
            query = json.loads(query_param)
            if not isinstance(query, dict):
                query = {}
        except json.decoder.JSONDecodeError:
            pass

        cursor = self.words_collection.find({'value': {'$ne': "_"}, **query})
        cursor.skip(per_page * (page - 1))
        cursor.limit(per_page)
        return self.json(list(cursor), count=cursor.count())


app.add_route(WordsAPI.as_view(), "/v1/words")
app.add_route(WordsAPI.as_view(), "/v1/words/<word:[^\\d\\W_]+>")
