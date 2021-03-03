
# https://stackoverflow.com/questions/52273722/selenium-mobile-emulation-how-do-i-add-user-agent-to-chrome-options-while-au
# https://stackoverflow.com/questions/51417440/emulate-devices-with-headless-chrome
# https://www.rubydoc.info/gems/selenium-webdriver/Selenium/WebDriver/Chrome/Options#add_emulation-instance_method
# https://peter.sh/experiments/chromium-command-line-switches/

'''
browser_options = ::Selenium::WebDriver::Chrome::Options.new
browser_options.args << '--headless'
browser_options.add_emulation(device_name: 'iPhone 8')

Capybara::Selenium::Driver.new(app, browser: :chrome, options: browser_options)
'''

from selenium import webdriver
from time import sleep


mobileEmulation = {'deviceName': 'Apple iPhone 4'}
options = webdriver.ChromeOptions()
options.add_experimental_option('mobileEmulation', mobileEmulation)

driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)

driver.get('http://m.baidu.com')

sleep(3)
driver.close()


from selenium import webdriver
from time import sleep

WIDTH = 320
HEIGHT = 640
PIXEL_RATIO = 3.0
UA = 'Mozilla/5.0 (Linux; Android 4.1.1; GT-N7100 Build/JRO03C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3'

mobileEmulation = {"deviceMetrics": {"width": WIDTH, "height": HEIGHT, "pixelRatio": PIXEL_RATIO}, "userAgent": UA}
options = webdriver.ChromeOptions()
options.add_experimental_option('mobileEmulation', mobileEmulation)

driver = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
driver.get('http://m.baidu.com')

sleep(3)
driver.close()