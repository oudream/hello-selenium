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
        self.driver.implicitly_wait(30)
        self.base_url = "http://192.168.5.29/web"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_app_dynamics_job(self):
        driver = self.driver

        def _login():
            driver.get("http://192.168.5.29/web/login")

            locator = (By.ID, "codeimage")
            img_base64 = None
            try:
                WebDriverWait(driver, 30).until(EC.visibility_of_element_located(locator))
                # WebDriverWait(driver, 30).until(EC.presence_of_element_located(locator))
                # driver.execute_script("document.getElementById('codeimage').decoding = 'sync';")
                time.sleep(1)
                driver.find_element_by_id("codeimage").screenshot('codeimage.png')
                # img_base64 = driver.find_element_by_id("codeimage").screenshot_as_base64
                # img_base64 = driver.find_element_by_id("codeimage").get_property('complete')
            except:
                print("ele can't find")

            driver.find_element_by_id("loginName").clear()
            driver.find_element_by_id("loginName").send_keys('69000000')
            driver.find_element_by_id("memberPwd").clear()
            driver.find_element_by_id("memberPwd").send_keys('qwer1234')
            # ERROR: Caught exception [ERROR: Unsupported command [doubleClick | id=loginName | ]]
            # driver.find_element_by_id("captcha").clear()

            # code = baidu_word_ocr.ocr_b64content(img_base64)
            code = baidu_word_ocr.ocr_file(r"codeimage.png")

            driver.find_element_by_id("captcha").clear()
            driver.find_element_by_id("captcha").send_keys(str(code).strip())
            # driver.find_element_by_id("captcha").send_keys(code)
            driver.find_element_by_id("loginSubmit").click()

            locator = (By.CSS_SELECTOR, ".user-info")
            ele = None
            try:
                driver.implicitly_wait(0)
                WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))
                ele = driver.find_element(*locator)
                driver.implicitly_wait(30)
                # time.sleep(1)  # 为了看效果
            except:
                print("ele can't find")

            return ele is not None

        for i in range(0, 5):
            if not _login():
                driver.execute_script("location.reload(true);")
            else:
                break

        # finally:

        # try:
        #     adc_bn = WebDriverWait(driver, 30, 0.5).until(
        #         EC.presence_of_element_located(("#popupAdCloseBtn",By.CSS_SELECTOR)),
        #         '页面元素加载超时！')
        #     if adc_bn.size() > 0:
        #         adc_bn.click()
        #     #
        #     # driver.implicitly_wait(30)
        #     # adc_bn = driver.find_element_by_id("popupAdCloseBtn")
        #     # driver.implicitly_wait(0)
        #     # if adc_bn.size() > 0:
        #     #     adc_bn.click()
        # except Exception:
        #     print('popupAdCloseBtn do not exist!')
        # driver.get("http://localhost:8080/web/login/logout")
        # driver.find_element_by_xpath("//dl[@class='top-menu login']")
        # driver.find_element_by_link_text(u"退出").click()
        # menu = driver.find_element_by_xpath("//dl[@class='top-menu login']")
        locator = (By.CSS_SELECTOR, "dl.top-menu.login")
        ele = None
        try:
            driver.implicitly_wait(0)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))
            ele = driver.find_element_by_css_selector("dl.top-menu.login")
            driver.implicitly_wait(30)
            # time.sleep(1)  # 为了看效果
        except:
            print("ele can't find")

        ActionChains(driver).move_to_element_with_offset(ele, 10, 10).perform()
        hidden_submenu = driver.find_element_by_link_text(u"離開城市")
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
