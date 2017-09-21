from selenium import webdriver
from PIL import Image


class ScreenShot(object):
    def __init__(self, url, js, filename):
        self.url = url
        self.js = js
        self.filename = filename

    def shot(self):
        browser = webdriver.PhantomJS()
        browser.get(self.url)
        browser.execute_script(self.js)
        browser.set_window_size(1680, 1080)
        browser.save_screenshot(self.filename)

    def crop(self):
        img = Image.open(self.filename)
        x = img.size[0]
        y = 1000
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
        print('Getting screen shot...')
        self.shot()
        print('Cropping the screen shot...')
        self.crop()
        print('Perfecting...')
        self.fill()
        print('Perfect!')
