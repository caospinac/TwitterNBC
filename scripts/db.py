import pymongo

from configparser import ConfigParser


_config = ConfigParser()
_config.read("config.ini")
config = _config._sections
for sec_name, sec_content in config.items():
    config[sec_name] = dict(
        (k, eval(v)) for k, v in sec_content.items()
    )

client = pymongo.MongoClient(
    config['DB']['host'], config['DB']['port']
)

db = client[config['DB']['name']]


if __name__ == "__main__":
    print("DB:", db.name)
