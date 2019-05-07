import os

from sanic import Sanic

from configparser import ConfigParser


_config = ConfigParser()
_config.read("config.ini")
config = _config._sections
for sec_name, sec_content in config.items():
    config[sec_name] = dict(
        (k, eval(v)) for k, v in sec_content.items()
    )

app = Sanic(__name__)
