import sys
import os
import re
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from PIL import Image
# Run on server. Should install Xvfb on system before use it.
# from pyvirtualdisplay import Display

# Import other folders model.
path = Path().parent.parent  # Project path.
sys.path.append(str(path.absolute()))
from flickr.console import MyFlickr
from utils import hack_zh

# Work path.
WORKPATH = Path('J:/') / 'google.image.result'


base_tag_xpath = '//g-img[@class="_ygd"]'
img_tag_xpath = '//g-img[@class="_ygd"]/img'
cite_tag_xpath = '//g-img[@class="_ygd"]/../../../..//cite'
image_size_tag_xpath = '//g-img[@class="_ygd"]/../../../..//span[@class="f"]'
title_tag_xpath = '//g-img[@class="_ygd"]/../../../../..//h3'
url_tag_xpath = '//g-img[@class="_ygd"]/../../../../..//h3' + '/a'
page2_tag_xpath = '//a[@aria-label="Page 2"]'

size_re = re.compile(r'(\d*) × (\d*)')

class GoogleResult:
    def __init__(self, title=None, url=None, cite=None, img_url=None, img_size=None, path:Path=None, sample_url=None):
        self.title = str(title)
        self.url = url
        self.cite = cite
        self.img_url = img_url
        self.img_size = img_size
        self.path = path
        self.sample_url = sample_url
        if not self.path.parent.exists():
            self.path.parent.mkdir()
        self.path.mkdir()

    def __repr__(self):
        return '''Title: {title}
URL: {url}
WEBSITE: {cite}
URL IMAGE: {img_url}
Size: {img_size}'''.format(**self.__dict__)

    @property
    def filename(self):
        title = '.'.join(self.title.split())
        return re.sub(r'''[/\ ()@*$%#?{}\[\];><!^~`.,'"+|]''', '_', title)

    @property
    def txt_path(self):
        return self.path / (self.filename + '.txt')

    @property
    def img_path(self):
        return self.path / (self.filename + '.jpg')

    @property
    def sample_path(self):
        return self.path.parent / 'sample.jpg'

    def save_txt_file(self):
        text = self.__repr__()
        try:
            self.txt_path.write_text(text)
        except UnicodeEncodeError:
            self.txt_path.write_text(hack_zh(text))

        print('Saved TXT file.')

    def download_image(self):
        print('Downloading image...')
        img = requests.get(self.img_url)
        self.img_path.write_bytes(img.content)
        print('Done.')

    def download_sample(self):
        if not self.sample_path.exists():
            print('Downloading sample image...')
            img = requests.get(self.img_url)
            self.sample_path.write_bytes(img.content)
            print('Done.')

    def run(self):
        self.save_txt_file()
        self.download_sample()
        self.download_image()


class GoogleImage(object):
    from collections import namedtuple
    Result = namedtuple('Result', 'title url cite img_url img_size')

    def __init__(self, url=None):

        self.google_image = 'https://images.google.com/?gws_rd=ssl'
        self.url = url
        self.screenshot_file = 'screenshot.png'
        self.entry = None
        # Run on server.
        # self.display = Display(visible=0, size=(1920, 1080))
        # self.display.start()
        # Run on Windows or Mac.
        self.browser = webdriver.Chrome()
        self.results = []

    def get_google(self):
        # import secret
        # self.browser.add_cookie(secret.get_google_cookie())
        self.browser.get(self.google_image)
        print('Open browser, and go to Google Image.')

    def show_entry(self):
        self.button = self.browser.find_element_by_xpath('//input[@id="lst-ib"]/../../..//a')
        self.button.click()
        print('Show entry.')

    def input_entry(self):
        self.entry = self.browser.find_element_by_xpath('//input[@id="qbui"]')
        self.entry.send_keys(self.url)
        self.entry.submit()
        print('Enter the image url, and submit.')

    def change_lang(self):
        url = self.browser.current_url.replace('hl=zh-CN', 'hl=en')
        self.browser.get(url)

    def download_thumb(self, url, title):
        image = requests.get(url)
        with open('thumb_{}.jpg'.format(title), 'wb') as f:
            f.write(image.content)

    @property
    def result_titles(self):
        title_tags = self.browser.find_elements_by_xpath(title_tag_xpath)
        titles = [tag.text.strip() for tag in title_tags]
        return titles

    @property
    def result_urls(self):
        url_tags = self.browser.find_elements_by_xpath(url_tag_xpath)
        urls = [tag.get_attribute('href') for tag in url_tags]
        return urls

    @property
    def result_cites(self):
        # cite_tags = self.browser.find_elements_by_xpath(cite_tag_xpath)
        # cites = [urlparse(tag.text.strip()).netloc for tag in cite_tags]
        return [urlparse(url).netloc for url in self.result_urls]

    @property
    def result_img_urls(self):
        img_tags = self.browser.find_elements_by_xpath(img_tag_xpath)
        img_urls = [tag.get_attribute('src') for tag in img_tags]
        return img_urls

    @property
    def result_img_sizes(self):
        size_tags = self.browser.find_elements_by_xpath(image_size_tag_xpath)
        img_size_res = [size_re.match(tag.text) for tag in size_tags]
        img_width_height = [[r.group(1), r.group(2)] for r in img_size_res]
        img_sizes = [int(width) * int(height) for width, height in img_width_height]
        return img_sizes

    @property
    def current_page_results(self):
        return list(
            zip(
                self.result_titles,
                self.result_urls,
                self.result_cites,
                self.result_img_urls,
                self.result_img_sizes
            )
        )

    def next_page(self):
        try:
            page2_tag = self.browser.find_element_by_xpath(page2_tag_xpath)
            page2_tag.click()
            print('Going to the next page...')
        except NoSuchElementException:
            print('Only 1 page of results.')

    def _process_result(self):
        _results = list(set(self.results) | set(self.current_page_results))
        self.results = [GoogleImage.Result._make(r) for r in _results]

    def shot(self):
        self.browser.set_window_size(1280, 1500)
        self.browser.save_screenshot(self.screenshot_file)

    def run(self):
        self.get_google()
        self.show_entry()
        self.input_entry()
        self.change_lang()
        self._process_result()  # Parse page 1.
        # self.next_page()
        # self._process_result()  # Parse page 2.

        print(self.results)
        # Run on server.
        # self.display.stop()
        self.browser.close()


if __name__ == '__main__':
    f = MyFlickr()
    sample_urls = f.get_photo_urls_from_photoset()
    for url_num, sample_url in enumerate(sample_urls, start=2):
        g = GoogleImage(sample_url)
        g.run()
        results = g.results
        for result_num, result in enumerate(results, start=1):
            # filename format: {number}-{cite}-{size}
            path = WORKPATH / str(url_num) / '{0:d}-{1}-{2:d}'.format(result_num, result.cite, result.img_size)
            gr = GoogleResult(**result._asdict(), path=path, sample_url=sample_url)
            gr.run()