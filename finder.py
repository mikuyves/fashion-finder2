from gevent import monkey; monkey.patch_all()
import gevent
import time
import random
import re
import  os
from urllib.parse import urlparse

import requests
from lxml import html
from gmail import GMail, Message

from data.rules import website_rules
from data.useragent import USER_AGENTS
from screenshot import ScreenShot
from utils import hack_zh
# Define your own BASEPATH which is a ABS-PATH for saving the data.
from secret import BASEPATH
import send_gmail


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
            if self.url_zh:
                print('正在分析 %s 中文网站...' % self.domain)
                self.response_zh, self.doc_zh = get_html_doc(self.url_zh)
            self.is_parsed = True

    @property
    def url_zh(self):
        en2zh = self.rule.get('en2zh')
        return en2zh(self.url) if en2zh else None

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

    @property
    def fullname(self):
        return ' - '.join([self.brand, self.title])

    @property
    def filename_base(self):
        return '.'.join(' '.join([self.brand, self.title]).split())

    @property
    def folder_path(self):
        return os.path.join(BASEPATH, self.filename_base)

    @property
    def has_zh_maybe(self):
        return self.rule.get('has_zh_maybe')

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
        '''Returns ::list:: Raw results of css selector.'''
        # Handle NoneType.
        if not full_css:
            return []
        # Handle `or` condition.
        f_css_list = full_css.split(', ')
        for f_css in f_css_list:
            css, prop = f_css.split('::')

            # Handle language.
            if not lang or lang == 'en':
                results = self.doc.cssselect(css)
            elif lang == 'zh':
                results = self.doc_zh.cssselect(css)

            # Skip no result condition.
            if results == []:
                continue

            if prop == 'text':
                return [r.text for r in results]
            elif 'attr' in prop:
                prop_value = prop[5:-1]
                return [r.attrib.get(prop_value) for r in results]

    def parse_raw(self, results, output='text'):
        if results == []:
            return ''

        if output == 'text':
            return ' '.join(''.join(results).split()) if results else ''
        elif output == 'paragraph':
            return '\n'.join([i.strip() for i in results if i and i.strip()]) if results else ''
        elif output == 'list':
            return [i.strip() for i in results if i and i.strip()] if results else []

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

    def download(self):
        urls = self.photo_urls
        if urls:
            print('\nDownloading photos of %s from %s' % (self.fullname, self.domain))
            print('\nTotal: %d' % len(urls))
            # Some website such as matchesfashion.com should be requested with
            # User-Agent to download photos.
            for num, url in enumerate(urls):
                try:
                    photo = get_html_doc(url)[0]
                except Exception as e:
                    print(e)
                finally:
                    gevent.sleep(1)
                    if photo.ok:
                        filename = '%s_%d.jpg' % (self.filename_base, num)
                        abs_filename = os.path.join(self.folder_path, filename)
                        with open(abs_filename, 'wb') as f:
                            f.write(photo.content)
        else:
            print('No photo in this item.')

    def save_file(self):
        filename = os.path.join(self.folder_path, '%s.txt' % self.filename_base)
        with open(filename, 'w') as f:
            f.write(self.fullname)
            f.write('\n\n')
            f.write(self.desc)
            f.write('\n\n')
            f.write(self.details)
            f.write('\n\n')
            f.write(self.url)
            if self.has_zh_maybe:
                f.write('\n\n')
                try:
                    f.write(self.title_zh)
                    f.write('\n\n')
                    f.write(self.desc_zh)
                    f.write('\n\n')
                    f.write(self.details_zh)
                except UnicodeEncodeError:
                    f.write(hack_zh(self.title_zh))
                    f.write('\n\n')
                    f.write(hack_zh(self.desc_zh))
                    f.write('\n\n')
                    f.write(hack_zh(self.details_zh))
                f.write('\n\n')
                f.write(self.url_zh)

    def make_tag_file(self):
        # Make a file for Gmail.
        filename = os.path.join(self.folder_path, 'ready_to_send.gml')
        with open(filename, 'w') as f:
            f.write(self.fullname)

    def get_screenshot(self):
        js = self.rule.get('screenshot_js')
        filename = self.filename_base + '_shot.png'
        abs_filename = os.path.join(self.folder_path, filename)
        shot = ScreenShot(self.url, abs_filename, js)
        shot.run()
        return abs_filename

    def save(self):
        os.mkdir(self.folder_path)
        gevent.joinall([
            gevent.spawn(self.download),
            gevent.spawn(self.get_screenshot),
            gevent.spawn(self.save_file),
            gevent.spawn(self.make_tag_file)
        ], timeout=10)

    def run(self):
        self.parse()
        self.save()


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


if __name__ == '__main__':
    url = input('Enter URL:')
    f = Fashion(url)
    f.run()
