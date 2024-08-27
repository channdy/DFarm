import unittest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService

# Import Appium UiAutomator2 driver for Android platforms (AppiumOptions)
from appium.options.android import UiAutomator2Options

APPIUM_PORT = 4723
APPIUM_HOST = '127.0.0.1'


def appium_service():
    service = AppiumService()
    service.start(
        # Check the output of `appium server --help` for the complete list of
        # server command line arguments
        args=['--address', APPIUM_HOST, '-p', str(APPIUM_PORT)],
        timeout_ms=20000,
    )
    yield service
    service.stop()
    
def create_android_driver(custom_opts = None):
    options = UiAutomator2Options()
    options.platformVersion = '10'
    options.platformName = 'Android'
    options.automationName = 'uiautomator2'
    options.appPackage = 'com.facebook.katanb'
    # options.udid = '123456789ABC'
    options.deviceName = 'emulator-5606'
    if custom_opts is not None:
        options.load_capabilities(custom_opts)
    # Appium1 points to http://127.0.0.1:4723/wd/hub by default
    return webdriver.Remote(f'http://{APPIUM_HOST}:{APPIUM_PORT}', options=options)

# def android_driver_factory():
#     return create_android_driver

# def test_android_click(appium_service, android_driver_factory):
#     # Usage of the context manager ensures the driver session is closed properly
#     # after the test completes. Otherwise, make sure to call `driver.quit()` on teardown.
#     with android_driver_factory({
#         'appium:app': '/path/to/app/test-app.apk',
#         'appium:udid': '567890',
#     }) as driver:
#         el = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='item')
#         el.click()
        
driver = create_android_driver
el = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='item')


# capabilities = dict(
#     platformName='Android',
#     automationName='uiautomator2',
#     deviceName='emulator-5606',
#     appPackage='com.android.settings',
#     appActivity='.Settings',
#     language='en',
#     locale='US'
# )

# appium_server_url = 'http://localhost:4723/wd/hub'

# # Converts capabilities to AppiumOptions instance
# capabilities_options = UiAutomator2Options().load_capabilities(capabilities)

# class Devices(unittest.TestCase):
#     def setUp(self) -> None:
#         self.driver = webdriver.Remote(command_executor=appium_server_url,options=capabilities_options)

#     def tearDown(self) -> None:
#         if self.driver:
#             self.driver.quit()

#     def test_find_battery(self) -> None:
#         el = self.driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Battery"]')
#         el.click()

# if __name__ == '__main__':
#     unittest.main()