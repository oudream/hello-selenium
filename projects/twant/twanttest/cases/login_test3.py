import math
from enum import Enum, unique
import unittest, time, re
import logging
import logging.handlers
import datetime
from PIL import Image

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from twanttest.base import baidu_word_ocr


logger = logging.getLogger(__name__)


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


class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.driver = webdriver.Chrome(driver_filepath[c_driver_type])
        self.driver.maximize_window()
        # self.driver.implicitly_wait(30)
        self.base_url = "http://192.168.5.29/web"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get("https://192.168.5.29/web/goods/3983?goodsId=6368")
        driver.execute_script("location.reload(true);")

        ele = datetime.datetime.now()
        try:
            ele = driver.find_element_by_css_selector(
                '#main-nav-holder > div.ncs-sidebar-container.goods-detall.share-container > div.right-side > div > div.ncs-meta.pr.nolmar-price')
            ele = driver.find_element_by_css_selector(
                '#main-nav-holder > div.ncs-sidebar-container.goods-detall.share-container > div.right-side > div > div.ncs-logistics')
            print(ele)
            print('-------------------------------1--- : '+str(math.floor(datetime.datetime.now().timestamp()*1000)))
            displayed = ele.get_property('offsetParent')
            print('-------------------------------2--- : '+str(math.floor(datetime.datetime.now().timestamp()*1000)))
            displayed = ele.is_displayed()
            print('-------------------------------3--- : '+str(math.floor(datetime.datetime.now().timestamp()*1000)))
            print(displayed)
        except Exception as e:
            print(e)
        print(ele)

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to.alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to.alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
