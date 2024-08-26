import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService

APPIUM_PORT = 4723
APPIUM_HOST = '127.0.0.1'

appium_service = AppiumService()
appium_service.start(
    # Check the output of `appium server --help` for the complete list of
    # server command line arguments
    args=['--address', APPIUM_HOST, '-p', str(APPIUM_PORT), '--base-path', '/wd/hub'], 
    timeout_ms=20000,
)
appium_service.start()

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['automationName'] = 'UiAutomator2'
desired_caps['platformVersion'] = '9'
desired_caps['deviceName'] = 'emulator-5606'
desired_caps['appPackage'] = 'com.facebook.katana'
desired_caps['appActivity'] = 'com.facebook.katana.activity.FbMainTabActivity'

capabilities_options = UiAutomator2Options().load_capabilities(desired_caps)

appium_server_url = 'http://localhost:4723/wd/hub'

# driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
time.sleep(10)

driver = webdriver.Remote(command_executor=appium_server_url,options=capabilities_options)

# ele_id = driver.find_element(AppiumBy.ID,"com.skill2lead.appiumdemo:id/EnterValue")
time.sleep(30)

elem = driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.FrameLayout[@resource-id="com.facebook.katana:id/(name removed)"])[2]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup').click()
time.sleep(1)
driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.FrameLayout[@resource-id="com.facebook.katana:id/(name removed)"])[2]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText').send_keys("Hello")
# elem.send_keys("Hello")

time.sleep(60)

driver.quit()

appium_service.stop()