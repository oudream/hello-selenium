# -*- coding: utf-8 -*-
import datetime
from enum import Enum, unique
from textwrap import dedent

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
        self.base_url = "http://192.168.5.29/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def wait_until_images_loaded(self, driver, timeout=30):
        """Waits for all images & background images to load."""
        driver.set_script_timeout(timeout)
        return driver.execute_async_script(dedent('''
            function extractCSSURL(text) {
                var url_str = text.replace(/.*url\((.*)\).*/, '$1');
                if (url_str[0] === '"') {
                    return JSON.parse(url_str);
                }
                if (url_str[0] === "'") {
                    return JSON.parse(
                        url_str
                            .replace(/'/g, '__DOUBLE__QUOTE__HERE__')
                            .replace(/"/g, "'")
                            .replace(/__DOUBLE__QUOTE__HERE__/g, '"')
                    );
                }
                return url_str;
            }
            function imageResolved(url) {
                return new $.Deferred(function (d) {
                    var img = new Image();
                    img.onload = img.onload = function () {
                        d.resolve(url);
                    };
                    img.src = url;
                    if (img.complete) {
                        d.resolve(url);
                    }
                }).promise();
            }
            var callback = arguments[arguments.length - 1];
            $.when.apply($, [].concat(
                $('img[src]')
                    .map(function (elem) { return $(this).attr('src'); })
                    .toArray(),
                $('[style*="url("]')
                    .map(function () { return extractCSSURL($(this).attr('style')); })
                    .toArray()
            ).map(function (url) { return imageResolved(url); })).then(function () { callback(arguments); });
        '''))

    def test_app_dynamics_job(self):
        driver = self.driver
        # driver.get("http://192.168.5.29/")
        # driver.get("https://taobao.com/")
        # driver.get("https://www.jd.com/")
        # driver.get("https://gz.meituan.com/")
        driver.get("https://www.twant.com/web/")
        # driver.execute_script("location.reload(true);")
        # driver.execute_script("""
        # var script = document.createElement( 'script' );
        # script.type = 'text/javascript';
        # script.src = 'https://code.jquery.com/jquery-3.5.1.slim.min.js';
        # script.integrity = 'sha256-4+XzXVhsDmqanXGHaHvgh1gMQKX40OUvDEBTu8JcmNs=';
        # script.crossorigin = 'anonymous';
        # document.head.appendChild(script);
        # """)
        now = time.perf_counter_ns()
        print('-------------------- begin : ' + str(datetime.datetime.now()))
        r = self.wait_until_images_loaded(driver)
        print('-------------------- cost : ' + str(r) + ' --- ' + str((time.perf_counter_ns()-now) // 1000000))


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
