from http import HTTPStatus

from sanic import Sanic
from sanic.exceptions import NotFound, FileNotFound
from sanic.views import HTTPMethodView
from sanic import response as sr

from web.core import app, db


@app.exception(NotFound, FileNotFound)
def error_404(request, exception):
    status = dict(vars(HTTPStatus))['_value2member_map_'][404]
    return sr.json({
        'status': status.phrase,
        'description': status.description,
        'code': status.value,
        'data': None
    }, status=status.value)


class APIUtils(HTTPMethodView):
    def __init__(self):
        self.words_collection = db.words

    def _parsed_data(self, data):
        def parse_id(data):
            return {
                **data,
                **({'_id': str(data['_id'])} if data.get('_id') else {}),
            }

        if isinstance(data, list):
            return list(map(parse_id, data))

        if isinstance(data, dict):
            return parse_id(data)

        return None


class API(APIUtils):

    def get(self, request, arg=None):
        return self.response(405)

    def post(self, request, arg=None):
        return self.response(405)

    def put(self, request, arg=None):
        return self.response(405)

    def patch(self, request, arg=None):
        return self.response(405)

    def delete(self, request, arg=None):
        return self.response(405)

    def _json(self, body, status=200, headers=None):
        return sr.json(body, status, headers)

    def json(self, data={}, **kwargs):
        data = self._parsed_data(data)
        return self.response(200, data, kwargs)

    def response(self, code=None, data=None, additionals={}):
        try:
            status = dict(vars(HTTPStatus))['_value2member_map_'][code]
            return sr.json({
                'status': status.phrase,
                'description': status.description,
                'code': status.value,
                **additionals,
                'data': data
            }, status=status.value)
        except KeyError as e:
            print("\033[91m")
            print(e)
            print("\033[0m")
            return sr.json({
                'status': "Unknown error",
                'description': "",
                'code': 500,
                'data': data
            }, 500)
