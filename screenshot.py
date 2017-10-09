import re
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PIL import Image


class GoogleResult(object):
    def __init__(self, title=None, url=None, size=None):
        self.title = title
        self.url = url
        self.size = size

    def to_dict(self):
        return {'title': self.title,
                'url': self.url,
                'size': self.size}


class ScreenShot(object):
    def __init__(self, url=None, filename='screenshot.png', js=None):
        self.url = url
        self.js = js
        self.filename = filename

    def browse(self):
        self.browser = webdriver.PhantomJS()
        self.browser.get(self.url)

    def shot(self):
        self.browser.set_window_size(1280, 1080)
        # if self.js:
        #     print('Running JS script...')
        #     browser.execute_script(self.js)
        self.browser.save_screenshot(self.filename)

    def crop(self):
        img = Image.open(self.filename)
        x = img.size[0]
        y = 900
        points = (0, 0, x, y)
        img = img.crop(points)
        img.save(self.filename)

    def fill(self):
        img = Image.open(self.filename)
        x, y = img.size
        points = (0, 0, x, y)
        p = Image.new('RGBA', img.size, (255, 255, 255))
        p.paste(img, points, img)
        p.save(self.filename)

    def run(self):
        self.browse()
        print('Getting screen shot...')
        self.shot()
        print('Cropping the screen shot...')
        self.crop()
        print('Perfecting...')
        self.fill()
        print('Perfect!')

base_tag_xpath = '//g-img[@class="_ygd"]'
img_tag_xpath = '//g-img[@class="_ygd"]/img'
cite_tag_xpath = '//g-img[@class="_ygd"]/../../../..//cite'
image_size_tag_xpath = '//g-img[@class="_ygd"]/../../../..//span[@class="f"]'
title_tag_xpath = '//g-img[@class="_ygd"]/../../../../..//h3'

size_re = re.compile(r'(\d*) × (\d*)')

class GoogleImage(object):


    def __init__(self, url=None):

        self.google_image = 'https://images.google.com/?gws_rd=ssl'
        self.url = url
        self.screenshot_file = 'screenshot.png'
        self.entry = None
        self.browser = webdriver.Chrome()
        self.results = []

    def get_google(self):
        # import secret
        # self.browser.add_cookie(secret.get_google_cookie())
        self.browser.get(self.google_image)

    def show_entry(self):
        self.button = self.browser.find_element_by_xpath('//input[@id="lst-ib"]/../../..//a')
        self.button.click()

    def input_entry(self):
        self.entry = self.browser.find_element_by_xpath('//input[@id="qbui"]')
        self.entry.send_keys(self.url)
        self.entry.submit()

    def change_lang(self):
        url = self.browser.current_url.replace('hl=zh-CN', 'hl=en')
        self.browser.get(url)

    def download_thumb(self):
        img_tags = self.browser.find_elements_by_xpath(img_tag_xpath)
        img_urls = [tag.get_attribute('src') for tag in img_tags]
        for num, url in enumerate(img_urls):
            image = requests.get(url)
            with open('thumb_{}.jpg'.format(num), 'wb') as f:
                f.write(image.content)

    @property
    def result_titles(self):
        title_tags = self.browser.find_elements_by_xpath(title_tag_xpath)
        titles = [tag.text.strip() for tag in title_tags]
        return titles

    @property
    def result_cites(self):
        cite_tags = self.browser.find_elements_by_xpath(cite_tag_xpath)
        cites = [tag.text.strip() for tag in cite_tags]
        return cites

    @property
    def result_img_urls(self):
        img_tags = self.browser.find_elements_by_xpath(img_tag_xpath)
        img_urls = [tag.get_attribute('src') for tag in img_tags]
        return img_urls

    @property
    def result_img_size(self):
        size_tags = self.browser.find_elements_by_xpath(image_size_tag_xpath)
        img_size_res = [size_re.match(tag.text) for tag in size_tags]
        img_width_height = [[r.group(1), r.group(2)] for r in img_size_res]
        img_sizes = [int(width) * int(height) for width, height in img_width_height]
        return img_sizes

    def shot(self):
        self.browser.set_window_size(1280, 1500)
        self.browser.save_screenshot(self.screenshot_file)

    def run(self):
        self.get_google()
        self.show_entry()
        self.input_entry()
        self.change_lang()
        self.download_thumb()


# 元素截图。
def shot_and_crop_element(browser, filename='elementshot.jpg'):
    browser.save_screenshot('elementshot.jpg')
    img_location = captcha_tag.location
    img_size = captcha_tag.size
    img_rangle = (
        int(img_location['x']),
        int(img_location['y']),
        int(img_location['x']) + img_size['width'],
        int(img_location['y']) + img_size['height'],
    )
    img = Image.open('elementshot.jpg')
    img = img.crop(img_rangle)
    img.save('elementshot.jpg')
    return img

