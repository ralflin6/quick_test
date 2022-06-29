import configparser, subprocess

import xml.etree.cElementTree as ET 
from urllib import request
from selenium.webdriver.common.by import By
from Logger import create_logger
import os

logger = create_logger("./Log/", "common")


def get_config():
    # 建立 ConfigParser
    local_config = configparser.ConfigParser()
    # 讀取 INI 設定檔
    local_config.read("Config/config.ini", encoding="utf-8")
    return local_config


# 取得 config
config = get_config()
target_url = config["KX_DEV_frontend"]["url"]

def is_connection_work(url):
    try:
        request.urlopen(url)
        return True
    except Exception as e:
        return False

def is_exist_element(driver, xpath, wtime=10):
    try:
        try:
            driver.implicitly_wait(wtime)
            driver.find_element_by_xpath(xpath)
            return True
        except:
            return False
    except Exception as e:
        return 'Except'

def is_exist_element_css(browser,web_element, css_xpath, wtime=10):
    try:
        try:
            browser.implicitly_wait(wtime)
            web_element.find_element_by_css_selector(css_xpath)
            return True
        except Exception as e:
            return False
    except Exception as e:
        return 'Except'

def Create_env(url):# 生成 env 環境 參數xml 給 報告顯示
    def get_driver_version():
        popen_path = ' chromedriver -v'
        logger.info(popen_path)
        p = subprocess.Popen(popen_path,stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
        shell=True, universal_newlines=True)
        return p.communicate()
    driver_v = get_driver_version()[0].split('(')[0]# 為tuple , 把 () 移除
    logger.info('driver - v: %s'%driver_v)    
    title = config['test_environment']['site']
    
    logger.info('Lic_URL: %s'%url)
    logger.info('title: %s'%title)

    try:
        doc = ET.fromstring("<environment><parameter><key>Browser.Version</key><value>{driver_v}</value></parameter><parameter><key>Url</key><value>{URL}</value></parameter><parameter><key>Lic</key><value>{LIC}</value></parameter></environment>".format(driver_v= driver_v
        ,URL= url, LIC= title ))

        tree = ET.ElementTree(doc)
        if not os.path.isdir('./reports/'):
            os.mkdir('./reports/')
        tree.write("./reports/environment.xml", encoding="utf-8") 
    except:
        logger.error('Create_env 寫入xml 有誤')