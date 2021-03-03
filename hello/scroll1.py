from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # 鼠标
from selenium.webdriver.common.action_chains import ActionChains  # 键盘
import time

driver = webdriver.Chrome()
driver.get("http://www.baidu.com")

#  2.10.1 浏览器滚动条  通过制定元素进行显示可见窗口
driver.find_element_by_link_text("新闻").click()
e=driver.find_element_by_id('change-city')
js='arguments[0].scrollIntoView();'
driver.execute_script(js,e)

# 浏览器滚动条  2.10.1 通过坐标点形式进行操作
driver.find_element_by_link_text("新闻").click()
time.sleep(2)
js = 'window.scrollTo(0,600)'
driver.execute_script(js)

# js的第二种 执行滚动条
driver.find_element_by_link_text("新闻").click()
time.sleep(2)
js = "document.documentElement.scrollTop=1000"
driver.execute_script(js)

# 滚动到底部
js = "window.scrollTo(0, document.body.scrollHeight);"
# driver.execute_script(js)
# sleep(10)
# # 滚动到顶部
js = "window.scrollTo(0, 0);"
driver.execute_script(js)

location = driver.find_element_by_link_text("新闻").location
driver.execute_script('window.scrollTo(%d,%d)' % (location['x'], location['y']))

# 让当前的元素滚动到浏览器窗口的可视区域内
'''
# https://developer.mozilla.org/zh-CN/docs/Web/API/Element/scrollIntoView
document.querySelector('li.comment-btn > a').scrollIntoView({behavior: "auto", block: "center", inline: "center"})
'''
e=driver.find_element_by_id('change-city')
js='arguments[0].scrollIntoView({behavior: "auto", block: "center", inline: "center"});'
driver.execute_script(js,e)

