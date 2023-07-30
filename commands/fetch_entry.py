import requests


def _get_json_from_url(url: str):
    with requests.get(url) as r:
        return r.json()[-1]


if __name__ == "__main__":
    print(_get_json_from_url("https://placetw.com/locales/en/art-pieces.json"))
