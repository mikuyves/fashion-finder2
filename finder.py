import time
import random

import requests
from lxml import html

from data.useragent import USER_AGENTS


user_agent = USER_AGENTS[random.randint(0, 10)]


# 发送请求，带 cookie。
def get_html_doc(url):
    time.sleep(0.9)
    headers = {
        'User-Agent': user_agent,
    }
    response = requests.get(
        url,
        headers=headers)
    print('Response code: %d' % response.status_code)
    return [response, html.fromstring(response.content)]
