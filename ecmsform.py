from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from IPython import embed

from secret import vivian, edison


ECMS_URL = 'http://ecmsglobal.com/cn/'
return_code = input('请输入退运单号：').upper()

person_num = input('1-vivian, 2-edison: ')
if person_num == '1' or not person_num:
    person = vivian
else:
    person = edison

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
b.find_element_by_id('returnPhone').send_keys(person.phone)
print('Input the Return Phone.')

captcha_text = input('Enter CAPTCHA: ')
print('Verify code: %s' % captcha_text)

window_cnt = len(b.window_handles)  # window_cnt = 1, 未弹出新页面时的页面数目。
b.find_element_by_id('returnVerifyCode').send_keys(captcha_text)  # 输入验证码。
b.find_element_by_id('returnPostBtn').click()  # 点击确认
print('Jumping to the detail form...')
new_window = b.window_handles[window_cnt]  # 弹出新页面。
b.switch_to.window(new_window)  # 跳转到新页面。

# title = '易客满-客户验证'
title = '易客满-退货人信息'
sec = 3
try:
    WebDriverWait(b, sec).until(
        ec.title_is(title)
    )
except Exception as e:
    print(e)

print('Get page of {}.'.format(b.title))

# 填写表单
# 姓（中文）
b.find_element_by_id('consigneeFirstNameCn').send_keys(person.surname)

# 名（中文）
b.find_element_by_id('consigneeLasterNameCn').send_keys(person.givenname)

# 联系电话
b.find_element_by_id('consigneePhone').send_keys(person.phone)

# 街道地址
b.find_element_by_id('consigneeAddress').send_keys(person.address)

# 邮编
b.find_element_by_id('consigneeZipCode').send_keys(person.zipcode)

# 身份证号码
b.find_element_by_id('cnsigneeIdCard').send_keys(person.id)

# 上传身份证照片
b.find_element_by_id('IDCardCopy1').send_keys(person.idcard_fr)
b.find_element_by_id('IDCardCopy2').send_keys(person.idcard_bk)

# 选择省市县
b.find_element_by_id('pcc-select').click()  # 点开选择界面
b.find_element_by_xpath('//a[@skuid=440000]').click()  # 省
b.find_element_by_xpath('//a[@skuid=440100]').click()  # 市
b.find_element_by_xpath('//a[@skuid=440105]').click()  # 区/县

# 勾选负责声明
b.find_element_by_id('checky').click()

# 验证码
captcha_text = input('Enter CAPTCHA: ')
b.find_element_by_id('verifyCode').send_keys(captcha_text)

# 提交
b.find_element_by_id('postme').click()

# 验证是否成功。
try:
    success_icon = b.find_element_by_xpath('//img[@src="/brige/static/imgs/success.png"]')
except NoSuchElementException:
    pass
else:
    if success_icon.is_displayed():
        print('Success!')
        b.close()


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