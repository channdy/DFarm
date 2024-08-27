import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import os
import subprocess
from selenium.webdriver.support.ui import WebDriverWait


try:
    # os.system("start /B start cmd.exe @cmd /k appium -a 127.0.0.1 -p 4723 --base-path /wd/hub")
    subprocess.Popen("""start appium -a 127.0.0.1 -p 4723 --base-path /wd/hub""", shell=True)
except Exception as err:
    print(err)

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['automationName'] = 'UiAutomator2'
desired_caps['platformVersion'] = '9'
desired_caps['deviceName'] = 'emulator-5554'
desired_caps['appPackage'] = 'com.facebook.katana'
desired_caps['appActivity'] = 'com.facebook.katana.activity.FbMainTabActivity'

capabilities_options = UiAutomator2Options().load_capabilities(desired_caps)

appium_server_url = 'http://localhost:4723/wd/hub'

# driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
time.sleep(10)

driver = webdriver.Remote(command_executor=appium_server_url,options=capabilities_options)

try:
    username_input = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.FrameLayout[@resource-id="com.facebook.katana:id/(name removed)"])[2]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup')))
    username_input.click()
    driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.FrameLayout[@resource-id="com.facebook.katana:id/(name removed)"])[2]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText').send_keys("Username")
    time.sleep(1)
    pwd_input = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.FrameLayout[@resource-id="com.facebook.katana:id/(name removed)"])[2]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup')))
    pwd_input.click()
    driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.FrameLayout[@resource-id="com.facebook.katana:id/(name removed)"])[2]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.widget.EditText').send_keys("Password")
    time.sleep(1)
    login_btn = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@content-desc="Log in"]/android.view.ViewGroup')))
    login_btn.click()
    time.sleep(60)
except TimeoutException as ex:
    print("Exception has been thrown. " + str(ex))

# time.sleep(60)

driver.quit()
# appium_service.stop()