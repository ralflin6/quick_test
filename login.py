from selenium.webdriver import ActionChains

from common import get_config,is_exist_element_css

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from datetime import datetime

import allure
import time,re
from Logger import create_logger

logger = create_logger("./Log/", "login")
config = get_config()

def login(browser):
    # 爽哥登入區塊
    with allure.step("爽哥登入區塊"):
        try:

            WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))

            with allure.step("輸入帳號 " + config["KX_DEV_frontend"]["acc"]):
                logger.info("輸入帳號 " + config["KX_DEV_frontend"]["acc"])
                # 輸入帳號
                browser.find_element_by_css_selector("input[name='username']").clear()
                browser.find_element_by_css_selector("input[name='username']").send_keys(config["KX_DEV_frontend"]["acc"])

            with allure.step("輸入密碼 " + config["KX_DEV_frontend"]["pwd"]):
                logger.info("輸入密碼 " + config["KX_DEV_frontend"]["pwd"])
                # 輸入密碼
                browser.find_element_by_css_selector("input[type='password']").clear()
                browser.find_element_by_css_selector("input[type='password']").send_keys(config["KX_DEV_frontend"]["pwd"])

            # 點擊 Login 按鈕
            browser.find_element_by_css_selector(".btn.mt-3").click()

            # 確認爽哥登入成功
            try:
                WebDriverWait(browser, 0.5).until(ec.presence_of_element_located((By.ID, "menuId")))
                allure.dynamic.title("登入資訊輸入正確測試 Pass!")
                logger.info("登入資訊輸入正確測試 Pass!")
                with allure.step("截圖"):
                    allure.attach(browser.get_screenshot_as_png(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), allure.attachment_type.PNG)
                assert True
            except Exception:
                with allure.step("截圖"):
                    allure.attach(browser.get_screenshot_as_png(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), allure.attachment_type.PNG)
                    allure.dynamic.title("登入資訊輸入正確測試 Fail!")
                    logger.info("登入資訊輸入正確測試 Fail!")
                    assert False
                

        except Exception as e:
            with allure.step("截圖"):
                allure.attach(browser.get_screenshot_as_png(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), allure.attachment_type.PNG)
            allure.dynamic.title("登入資訊輸入正確測試 Fail! : %s"%str(e))
            assert False