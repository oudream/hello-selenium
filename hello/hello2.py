# -*- coding: utf-8 -*-
from enum import Enum, unique

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


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
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8080/web"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get("http://localhost:8080/web/login")
        driver.find_element_by_id("loginName").clear()
        driver.find_element_by_id("loginName").send_keys('user001')
        driver.find_element_by_id("memberPwd").clear()
        driver.find_element_by_id("memberPwd").send_keys('123456')
        # ERROR: Caught exception [ERROR: Unsupported command [doubleClick | id=loginName | ]]
        driver.find_element_by_id("captcha").clear()
        driver.find_element_by_id("captcha").send_keys("1234")
        driver.find_element_by_id("loginSubmit").click()
        # time.sleep(5)
        # driver.get("http://localhost:8080/web/login/logout")
        # driver.find_element_by_xpath("//dl[@class='top-menu login']")
        # driver.find_element_by_link_text(u"退出").click()
        # menu = driver.find_element_by_xpath("//dl[@class='top-menu login']")
        menu = driver.find_element_by_css_selector("dl.top-menu.login")
        # print(menu)
        ActionChains(driver).move_to_element_with_offset(menu, 10, 10).perform()
        hidden_submenu = driver.find_element_by_link_text(u"退出")
        hidden_submenu.click()
        # driver.find_element_by_link_text(u"退出").click()



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
