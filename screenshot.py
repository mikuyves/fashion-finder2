import re
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PIL import Image


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


# 元素截图。
# def shot_and_crop_element(browser, filename='elementshot.jpg'):
#     browser.save_screenshot('elementshot.jpg')
#     img_location = captcha_tag.location
#     img_size = captcha_tag.size
#     img_rangle = (
#         int(img_location['x']),
#         int(img_location['y']),
#         int(img_location['x']) + img_size['width'],
#         int(img_location['y']) + img_size['height'],
#     )
#     img = Image.open('elementshot.jpg')
#     img = img.crop(img_rangle)
#     img.save('elementshot.jpg')
#     return img

