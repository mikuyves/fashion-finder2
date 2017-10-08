from selenium import webdriver

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

captcha_text = input('Enter CAPTCHA: ')
print('Verify code: %s' % captcha_text)

b.find_element_by_id('returnVerifyCode').send_keys(captcha_text)
b.find_element_by_id('returnPostBtn').click()

print('Jump to the detail form.')

# TODO: Waiting for another Return Code to test.