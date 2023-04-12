import subprocess

from flask import Flask, Response
from werkzeug.wrappers import Request

from . import request as r
from .detector import Detector
from .evolution import Evolution
from .request_parser import BodyParser, QueryParser


def get_directory(dir_name: str):
    from pathlib import Path

    path_to_aifw = Path(__file__).parents[0]
    return str(path_to_aifw / dir_name)


class DetectorMiddleware(object):
    """
        Middleware for detecting hacks
    """

    def __init__(self, app: Flask):
        print("Loading models")
        self.app = app
        self.evolution: Evolution = Evolution.load(
            '499', get_directory("models"))
        self.body_parser = BodyParser.load()
        self.query_parser = QueryParser.load()
        self.detector = Detector(
            self.evolution, self.body_parser, self.query_parser)

        print("Finished loading")

        # try:
        #     subprocess.run(["clear"], check = True)
        # except:
        #     subprocess.run(["cls"], check = True)

    def __call__(self, environ, start_response):
        """
            Called by middleware. Actually does the detecting.
        """

        request = Request(environ)

        data = r.Request({
            "method": request.method,
            "content_length": request.content_length,
            "protocol": request.environ.get('SERVER_PROTOCOL'),
            "is_hack": None
        })

        invalid = self.detector.predict(
            data, request.get_data(), request.query_string)

        if invalid:
            # It's a hack
            res = Response("hack detected", 403)
            return res(environ, start_response)

        return self.app(environ, start_response)
