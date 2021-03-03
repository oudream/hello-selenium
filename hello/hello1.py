"""
http://localhost:8080/web/login
user001
123456
http://localhost:8080/web/goods/3?goodsId=11
http://localhost:8080/web/goods/3?goodsId=13


http://localhost:8080/seller/login
sell001
123456


http://localhost:8080/admin/login
admin
111111


"""
import os

from enum import Enum, unique

from selenium import webdriver


@unique
class DriverType(Enum):
    Chrome = 1
    Edge = 2
    Firefox = 3


c_driver_type = DriverType.Chrome

driver_filepath = {
    DriverType.Chrome: r"D:\tools\webdriver\chromedriver.exe",
    DriverType.Edge: r"D:\tools\webdriver\msedgedriver.exe",
    DriverType.Firefox: r"D:\tools\webdriver\geckodriver.exe"
}


def get_driver_filepath(dt):
    return driver_filepath[dt]


try:
    os.system("taskkill /f /im {} /t".format(os.path.basename(driver_filepath[c_driver_type])))
except:
    pass

if c_driver_type == DriverType.Chrome:
    browser = webdriver.Chrome(r"D:\tools\webdriver\chromedriver.exe")
elif c_driver_type == DriverType.Edge:
    browser = webdriver.Edge(r"D:\tools\webdriver\msedgedriver.exe")
else:
    browser = webdriver.Firefox(r"D:\tools\webdriver\geckodriver.exe")
browser.get('http://seleniumhq.org/')
