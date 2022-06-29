import pytest
from selenium import webdriver
from common import get_config
import sys

driver = None
# 取得 config
config = get_config()

'''
url = sys.argv[1]
config.set("config","urllist",str(url))

username = sys.argv[2]
config.set("config","username",str(username))

password = sys.argv[3]
config.set("config","password",str(password))

file = open("Config/config.ini", 'w')
config.write(file) 
file.close()
'''

class NoTestException(Exception):
    pass

import winreg , os , requests , zipfile
from Logger import create_logger
log = create_logger(r"\AutoTest", 'test')


def get_Chrome_version():#取得local Chrome version
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
    version, types = winreg.QueryValueEx(key, 'version')
    local_version = version.split('.')[0]
    log.info('local Chrome version : %s'%local_version)
    return local_version

def get_Driver_version():
    '''查询系统内的Chromedriver版本'''
    local_driver_version = os.popen('chromedriver --version').read().split(' ')[1].split('.')[0]
    log.info('local driver version : %s'%local_driver_version)
    return local_driver_version


def get_server_chrome_versions(version):#version 需帶 數字,去抓去 網站上有的 chromedriver
    '''return all versions list'''

    #down_ver_list = []# 存放 有mapping 到的 chromedriver version
    url="https://registry.npmmirror.com/-/binary/chromedriver/"
    rep = requests.get(url).json()# list 裡麵包字典
    for dict_ in rep:
        split_version = dict_['name'].split('.')[0]# # 抓取 name 並把 他取出 70.0.3538.97/ > 70
        if version == split_version:
            down_url = dict_['url']
            log.info('抓到 對應的 driver 版本 : %s'%dict_['name'])
            return down_url+ 'chromedriver_win32.zip'

def download_driver(download_url):
    '''下载文件'''
    file = requests.get(download_url)
    with open("chromedriver.zip", 'wb') as zip_file:        # 保存文件到脚本所在目录
        zip_file.write(file.content)
    new_driver = get_Chrome_version()
    log.info('新driver: %s 下载成功'%new_driver)


def unzip_driver():
    '''解压Chromedriver压缩包到指定目录'''
    f = zipfile.ZipFile("chromedriver.zip",'r')
    for file in f.namelist():
        f.extract(file, '.')
    log.info('解壓縮成功')


local_chrome = get_Chrome_version()
local_driver = get_Driver_version()
if local_chrome == local_driver:
    log.info('local chrome version 和 driver version 一致 , 無須 下載')
else:
    down_url = get_server_chrome_versions(local_chrome)
    download_driver(down_url)
    unzip_driver()


@pytest.fixture(scope='session', autouse=True)
def browser(request):
    global driver
    if driver is None:
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
    def fin():
        driver.quit()
    request.addfinalizer(fin)        
    return driver
