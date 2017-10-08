from pathlib import Path

import requests
from selenium import webdriver
from PIL import Image
import matplotlib.pyplot as plt

from secret import RETURN_PHONE


ECMS_URL = 'http://ecmsglobal.com/cn/'
return_code = 'ECM015047583'


# 打开浏览器，进入网址。
b = webdriver.Chrome()
b.get(ECMS_URL)

# 点击“清关资料”按钮。
info_tag = b.find_elements_by_xpath('//ul[@id="subNav"]/li/a')[1].click()
# 点击”退运“按钮。
b.find_element_by_id('btnReturn').click()

# 填写“退运运单号”和“手机号码”
b.find_element_by_id('returnCode').send_keys(return_code)
b.find_element_by_id('returnPhone').send_keys(RETURN_PHONE)

# 获取验证码图片
captcha_tag = b.find_element_by_id('returnCaptcha')
captcha_tag = b.find_element_by_id('returnCaptcha')

# 不能请求这个captcha_url，每请求一次变一次。
# captcha_url = captcha_tag.get_attribute('src')

# 保存图片，并截图。
b.save_screenshot('captcha.jpg')
img_location = captcha_tag.location
img_size = captcha_tag.size
img_rangle = (
    int(img_location['x']),
    int(img_location['y']),
    int(img_location['x']) + img_size['width'],
    int(img_location['y']) + img_size['height'],
)
img = Image.open('captcha.jpg')
img = img.crop(img_rangle)
img.save('captcha.jpg')

# import matplotlib.image as mpimg
# imgplot = plt.imshow(mpimg.imread('animal.png'))

img = Image.open('captcha.jpg')
plt.imshow(img)
plt.ion()
plt.show()
captcha_text = input('Enter what you see: ')
plt.close()
print('Verify code: %s' % captcha_text)

b.find_element_by_id('returnVerifyCode').send_keys(captcha_text)
b.find_element_by_id('returnPostBtn').click()

print('Jump to the detail form.')

