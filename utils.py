# 解决中文乱码问题。
def hack_zh(text):
    return text.encode('utf-8').decode('gbk', 'ignore')