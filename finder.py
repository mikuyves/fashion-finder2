import time
import random
import re
from urllib.parse import urlparse

import requests
from lxml import html

from data.rules import website_rules
from data.useragent import USER_AGENTS


user_agent = USER_AGENTS[random.randint(0, 10)]


class Fashion(object):
    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(url)
        self.domain = self.parsed_url.netloc
        self.rule = website_rules.get(self.domain)
        self.is_parsed = False

    def parse(self):
        if self.is_parsed:
            return
        else:
            print('Parsing %s' % self.domain)
            self.response, self.doc = get_html_doc(self.url)
            en2zh = self.rule.get('en2zh')
            if en2zh:
                print('正在分析 %s 中文网站...' % self.domain)
                self.url_zh = en2zh(self.url)
                self.response_zh, self.doc_zh = get_html_doc(self.url_zh)
            self.is_parsed = True

    @property
    def brand(self):
        if not self.is_parsed:
            return
        if self.rule.get('type') == 'Official':
            return self.rule.get('brand')
        return self.parse_field('brand')

    @property
    def title(self):
        if not self.is_parsed:
            return
        return self.parse_field('text_css.title')

    @property
    def desc(self):
        if not self.is_parsed:
            return
        return self.parse_field('text_css.desc')

    @property
    def details(self):
        if not self.is_parsed:
            return
        return self.parse_field('text_css.details', output='paragraph')

    @property
    def photo_urls(self):
        if not self.is_parsed:
            return
        urls = self.parse_field('photo_urls_css', output='list')
        urls = self.process_photo_with_re(urls)
        urls = self.process_photo_with_handler(urls)
        urls = self.validate_urls(urls)
        return urls

    # 中文属性。
    @property
    def title_zh(self):
        if not self.is_parsed:
            return
        return self.parse_field('text_css.title', lang='zh')

    # 中文属性。
    @property
    def desc_zh(self):
        if not self.is_parsed:
            return
        return self.parse_field('text_css.desc', lang='zh')

    # 中文属性。
    @property
    def details_zh(self):
        if not self.is_parsed:
            return
        return self.parse_field('text_css.details', output='paragraph', lang='zh')

    def parse_css(self, full_css, lang):
        css, prop = full_css.split('::')
        if not lang or lang == 'en':
            results = self.doc.cssselect(css)
        elif lang == 'zh':
            results = self.doc_zh.cssselect(css)

        if prop == 'text':
            return [r.text for r in results]
        elif 'attr' in prop:
            prop_value = prop[5:-1]
            return [r.attrib.get(prop_value) for r in results]

    def parse_raw(self, results, output='text'):
        if results == []:
            return None

        if output == 'text':
            return ' '.join(''.join(results).split()) if results else None
        elif output == 'paragraph':
            return '\n'.join([i.strip() for i in results if i.strip()]) if results else None
        elif output == 'list':
            return [i.strip() for i in results if i.strip()] if results else None

    def parse_field(self, key, output='text', lang='en'):
        if '.' in key:
            k1, k2 = key.split('.')
            full_css = self.rule.get(k1).get(k2)
        else:
            full_css = self.rule.get(key)
        raw_results = self.parse_css(full_css, lang=lang)
        result = self.parse_raw(raw_results, output=output)
        return result

    def process_photo_with_re(self, urls):
        url_pattern = self.rule.get('photo_urls_re')
        if not url_pattern:
            return urls
        else:
            url_re = re.compile(url_pattern)
            return [url_re.match(url).group(1) for url in urls]

    def process_photo_with_handler(self, urls):
        handle = self.rule.get('handle_photo_urls')
        if not handle:
            return urls
        else:
            return handle(urls)

    def validate_urls(self, urls):
        scheme = self.parsed_url.scheme
        netloc = self.domain

        valid_urls = []
        for url in urls:
            parsed_url = urlparse(url)
            if parsed_url.scheme and parsed_url.netloc:
                pass
            elif not parsed_url.scheme and not parsed_url.netloc:
                url = parsed_url._replace(**{'scheme': scheme, 'netloc': netloc}).geturl()
            elif not parsed_url.scheme:
                url = parsed_url._replace(**{'scheme': scheme}).geturl()
            valid_urls.append(url)

        return valid_urls


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


def print_result(res):

    print('Brand: %s' % res.brand)
    print('Title: %s' % res.title)
    print('Desc: %s' % res.desc)
    print('Details: %s' % res.details)
    print('Photo URLs: %s' % res.photo_urls)

    print('中文翻译：')
    print('Title: %s' % res.title_zh)
    print('Desc: %s' % res.desc_zh)
    print('Details: %s' % res.details_zh)
