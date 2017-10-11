from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from IPython import embed

from secret import RETURN_PHONE


ECMS_URL = 'http://ecmsglobal.com/cn/'
return_code = 'ECM015047582'


# 打开浏览器，进入网址。
b = webdriver.Chrome()
b.get(ECMS_URL)
print('Getting page of {}'.format(ECMS_URL))

# 点击“清关资料”按钮。
info_tag = b.find_elements_by_xpath('//ul[@id="subNav"]/li/a')[1].click()
# 点击”退运“按钮。
b.find_element_by_id('btnReturn').click()
print('Switch to RETURN tag.')

# 填写“退运运单号”和“手机号码”
b.find_element_by_id('returnCode').send_keys(return_code)
print('Input the Return Code.')
b.find_element_by_id('returnPhone').send_keys(RETURN_PHONE)
print('Input the Return Phone.')

captcha_text = input('Enter CAPTCHA: ')
print('Verify code: %s' % captcha_text)

window_cnt = len(b.window_handles)  # window_cnt = 1, 未弹出新页面时的页面数目。
b.find_element_by_id('returnVerifyCode').send_keys(captcha_text)  # 输入验证码。
b.find_element_by_id('returnPostBtn').click()  # 点击确认
print('Jumping to the detail form...')
new_window = b.window_handles[window_cnt]  # 弹出新页面。
b.switch_to.window(new_window)  # 跳转到新页面。

title = '易客满-客户验证'
sec = 3
try:
    WebDriverWait(b, sec).until(
        ec.title_is(title)
    )
except Exception as e:
    print(e)

print('Get page of {}.'.format(b.title))

embed()
# TODO: Waiting for another Return Code to test.

# from selenium.webdriver.support.ui import Select
#
# # 将XPath为xpath的下拉框选择值为value的选项
# Select(browser.find_element_by_xpath(xpath).select_by_value(value)

# 上传文件
#
# 对于部分需要涉及到上传文件的地方，比如上传头像，其实原理就是找到对应的input元素，通过send_keys()将文件路径传递，如：
#
# 1
# browser.find_element_by_xpath(xpath).send_keys(path_of_file)