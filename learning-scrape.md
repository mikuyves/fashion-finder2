Web scraping using Python: requests and lxml
===

[https://data-lessons.github.io/library-webscraping/04-lxml/]

### Traversing elements in a page with lxml
The following illustrates loads the response HTML into a tree of elements, and illustrates the `xpath` and `cssselect` methods provided on an ElementTree (and each Element thereof), as well as other tree traversal. Running the following code:

```python
import requests
import lxml.html

response = requests.get('http://www.un.org/en/sc/documents/resolutions/2016.shtml')
tree = lxml.html.HTML(response.text)
title_elem = tree.xpath('//title')[0]
title_elem = tree.cssselect('title')[0]  # equivalent to previous XPath
print("title tag:", title_elem.tag)
print("title text:", title_elem.text_content())
print("title text:", title_elem.text)
print("title html:", lxml.html.tostring(title_elem))
print("title tag:", title_elem.tag)
print("title's parent's tag:", title_elem.getparent().tag)
```

produces this output:

```bash
title tag: title
title text: Resolutions adopted by the United Nations Security Council in 2016
title text: Resolutions adopted by the United Nations Security Council in 2016
title html: b'<title>Resolutions adopted by the United Nations Security Council in 2016</title>&#13;\n'
title tag: title
title's parent's tag: head
```


This code begins by building a tree of Elements from the HTML using `lxml.html.fromstring(some_html)`. It then illustrates some operations on the elements. With some element, `elem`, or the tree:

* `elem.xpath(some_path)` and elem.cssselect(some_selector) find a list of nodes relative to elem matching the given XPath or CSS selector expression, respectively.
* `elem.getparent()` gets the parent element of elem. Similarly, elem.getprevious() and elem.getnext() may return a single element, or None.
* `elem.getchildren()` gets a list of the children of elem, while elem.getiterator() allows for iterating over all the descendants of elem. (Not illustrated above.)
* `elem.tag` is elem’s tag name.
* `elem.text_content()` gets the text of an element and all of its children
* `elem.text` is the text of an element and all of its children
    - `elem.text_content() == elem.text  # True`
* `elem.attrib` is a dict of the attributes of elem.
* `lxml.html.tostring(elem)` translates the element back into HTML/XML.

In the above example, we extract the first (and only) <title> element from the page, show its text, etc., and do the same for its parent, the <head> node. When we print the text of that parent node, we see that it consists of two blank lines. Why?

Apart from basic features of Python, these are all the tools we should need.


### PhantomJS 截图
```python
import base64
import sys
import pyocr
from StringIO import StringIO
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from PIL import Image

driver = webdriver.Remote(
    command_executor='http://10.10.10.140:8910',
    desired_capabilities=DesiredCapabilities.PHANTOMJS)

driver.get('目标网址')


# 获取元素位置
element = driver.find_element_by_class_name('conttxt')
location = element.location
size = element.size

# 计算出元素位置图像坐标
img = Image.open(StringIO(base64.decodestring(driver.get_screenshot_as_base64())))
driver.quit()
left = location['x']
top = location['y']
right = location['x'] + size['width']
bottom = location['y'] + size['height']
img = img.crop((int(left), int(top), int(right), int(bottom)))
# img.save('screenshot.png') 是否保存图像


# 利用pyocr库 推荐引擎tesseract进行图像识别
tools = pyocr.get_available_tools()[:]
print tools[0].image_to_string(img,lang='chi_sim')

# from: https://www.cplusplus.me/2624.html
```


