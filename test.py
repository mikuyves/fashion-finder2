from selenium import webdriver
from PIL import Image


from finder import Fashion, print_result


def test_fashion():
    url = input('Enter Url: ')
    f = Fashion(url)
    f.run()
    print_result(f)


def test_selenium():
    url = input('Enter Url: ')
    browser = webdriver.PhantomJS()
    browser.get(url)
    # css = input('Enter CSS selector: ')
    # tag = browser.find_element_by_css_selector('')
    # print(tag.text)1920
    browser.execute_script(website_rules[website]['screenshot_js'])

    browser.set_window_size(1680, 1080)
    browser.save_screenshot('screenshot.png')


def crop_screenshot(filename):
    img = Image.open(filename)
    x = img.size
    y = 1000
    points = (0, 0, x, y)
    img = img.crop(points)
    img.save(filename)


def fill_white(filename):
    img = Image.open(filename)
    x, y = img.size
    points = (0, 0, x, y)
    p = Image.new('RGBA', img.size, (255, 255, 255))
    p.paste(img, points, img)
    p.save('%s_white.png' % filename.split('.')[0])


