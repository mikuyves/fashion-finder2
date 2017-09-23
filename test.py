import asyncio
import time

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


now = lambda: time.time()

from types import coroutine

@coroutine
def y_sleep():
    yield time.sleep(1)
''' Result:
```bash
Start 1  -- 1 sec
Start 2  -- 1 sec
Start 3  -- 1 sec
End 1  \
End 2  ----- almost the same time
End 3  /
Time: 3.009171962738037 sec.
```
'''

@asyncio.coroutine
def yf_sleep():
    yield from time.sleep(1)

async def o_sleep():
    await time.sleep(1)
''' Result:
```bash
Start 1  -- 1 sec
Start 2  -- 1 sec
Start 3  -- 1 sec
Time: 3.006171941757202 sec.
         -- BUT no ends.
```
'''


async def a_sleep():
    await asyncio.sleep(1)
''' Result:
```bash
Start 1  \
Start 2  ----- almost the same time
Start 3  /
End 1  \
End 2  ----- almost the same time
End 3  /
Time: 1.0080575942993164 sec.
```
'''

async def sleep():
    time.sleep(1)
''' Result:
```bash
Start 1
End 1
Start 2
End 2
Start 3
End 3
Time: 3.008172035217285 sec.
```
'''


async def get_sleep(n):
    print('Start {}'.format(n))
    # await y_sleep()
    await yf_sleep()
    # await o_sleep()
    # await a_sleep()
    # await sleep()
    print('End {}'.format(n))


start = now()

# coro1 = get_sleep(1)
# coro2 = get_sleep(2)
# coro3 = get_sleep(3)
#
# tasks = [
#     asyncio.ensure_future(coro1),
#     asyncio.ensure_future(coro2),
#     asyncio.ensure_future(coro3)
# ]

tasks = [asyncio.ensure_future(get_sleep(i)) for i in range(1,4)]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

print('Time: {} sec.'.format(now() - start))
