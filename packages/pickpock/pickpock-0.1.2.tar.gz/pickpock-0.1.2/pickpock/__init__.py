"""
A re-implementation of Deen Freelon's pyktok

json dsl from https://skeptric.com/json-extraction-dsl/
"""
import re
import csv
import json
import datetime
import functools
import time
import random
from pathlib import Path
from operator import itemgetter
from typing import Union, Callable, Any

import requests
import selectolax
import browser_cookie3

from requests.adapters import HTTPAdapter, Retry

# ****************************************************************************
# *                                   setup                                  *
# ****************************************************************************


headers = {'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'en-US,en;q=0.8',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive'}
url_regex = '(?<=\.com/)(.+?)(?=\?|$)'

DEFAULT_COLS = [
    'id',
    'createTime',
    'video.duration',
    'locationCreated',
    'desc',
    'isAd',

    'stats.diggCount',
    'stats.shareCount',
    'stats.commentCount',
    'stats.playCount',

    'author',
    'nickname',
    'author.nickname',
    'author.verified',
    'authorStats.followerCount',
    'authorStats.followingCount',
    'authorStats.heartCount',
    'authorStats.videoCount',
    'authorStats.diggCount',
]

session = None
sleep = 5

# ****************************************************************************
# *                                 json dsl                                 *
# ****************************************************************************


def is_integer(s: str) -> bool:
    return re.match('^-?[0-9]+$', s) is not None


def convert_integers(s: str) -> Union[str, int]:
    if is_integer(s):
        return int(s)
    else:
        return s


def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions)


def extractor(path: str, sep: str='.') -> Callable[[Any], Any]:
    steps = [convert_integers(x) for x in path.split(sep)]
    return compose(*map(itemgetter, reversed(steps)))


def extract(obj: Any, path: str, sep: str='.', default=None) -> Any:
    try:
        return extractor(path, sep)(obj)
    except (KeyError, IndexError, TypeError):
        return default

# ****************************************************************************
# *                               data storage                               *
# ****************************************************************************


def write_json(data, filename="tiktok.jsonl"):
    with open(filename, "a") as datafile:
        datafile.write(json.dumps(data) + "\n")


def write_csv(data,
              filename="tiktok.csv",
              cols=DEFAULT_COLS):
    header = Path(filename).exists()
    with open(filename, "a") as csvf:
        writer = csv.writer(csvf)
        # add header if the file didn't exist
        if not header:
            writer.writerow([*cols, "date_captured"])
        row = []
        for element in cols:
            val = extract(obj=data, path=element, sep=".", default='')
            if "createTime" in element:
                val = datetime.datetime.fromtimestamp(int(val)).isoformat()
            print(f'{element}: {val}')
            row.append(val)
        row.append(datetime.datetime.utcnow().isoformat())
        writer.writerow(row)


# ****************************************************************************
# *                                   core                                   *
# ****************************************************************************

def init(browser="firefox", cookie_file=None, throttle=5):
    if not cookie_file:
        if Path("cookies.sqlite").exists:
            cookie_file = "cookies.sqlite"
        else:
            raise "No cookie file found, provide cookies.sqlite or path via parameter"
    cookies = getattr(browser_cookie3, browser)(cookie_file=cookie_file, domain_name='www.tiktok.com')

    global sleep
    sleep = throttle

    global session
    session = requests.Session()

    retries = Retry(total=3,
                    backoff_factor=2,
                    status_forcelist=[500, 502, 503, 504])

    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.headers.update(headers)
    session.cookies.update(cookies)


def fetch_json(url):
    tt = session.get(url, timeout=30)
    t = selectolax.parser.HTMLParser(tt.content)
    script = t.css_first("script#SIGI_STATE")
    tt_json = json.loads(script.text())
    time.sleep(random.randint(1, sleep))
    return tt_json


def fetch_video(url):
    pass


def fetch_multi(url):
    tt_json = fetch_json(url)
    data_loc = tt_json['ItemModule']
    for v in data_loc:
        data_slot = data_loc[v]
        yield data_slot


def fetch_post(url):
    tt_json = fetch_json(url)
    video_id = list(tt_json['ItemModule'].keys())[0]
    data_slot = tt_json['ItemModule'][video_id]
    yield data_slot


def fetch(url):
    """
    Dispatch download to specific method
    """
    if not session:
        init()
    if "/tag/" in url:
        yield from fetch_multi(url)
    elif "/video/" in url:
        yield from fetch_post(url)
    elif re.findall("@[a-zA-Z0-9_-]*", url) and "video" not in url:
        yield from fetch_multi(url)


def store(url):
    regex_url = re.findall(url_regex, url)[0]
    metadata_fn = regex_url.replace('/', '_') + '.csv'
    for item in fetch(url):
        write_json(item)
        write_csv(item, filename=metadata_fn)
