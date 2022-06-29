from common import get_config, is_connection_work,Create_env
from login import login
import pytest
import allure
from allure_pytest import plugin as allure_plugin
from datetime import datetime

# 取得 config
config = get_config()

url = config["KX_DEV_frontend"]["url"]
login_success = False

def Clean_Report():
    import shutil
    try:
        rm_path = './reports'
        print(rm_path)
        clean = shutil.rmtree(rm_path)
        return clean
    except FileNotFoundError:
        print('目前無reports ')

def test_login(browser): #為了分割
    global login_success
    if login_success == False:
        retry = 0
        while retry < 3:
            try:
                if is_connection_work(url): #判斷此 Url 是否可正常連線
                    browser.get(url)
                    allure.dynamic.title("登入網址是否健康測試 Pass!")
                    assert True
                else:
                    with allure.step("截圖"):
                        allure.attach(TestSelenium.browser.get_screenshot_as_png(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), allure.attachment_type.PNG)
                    allure.dynamic.title("登入網址是否健康測試 Fail!")
                    assert False
                login(browser)
                login_success = True
                break
            except:
                retry += 1
        if retry == 3:
            login_success = False
    else:
        pass

@allure.feature("Selenium Test")
class TestSelenium:
    @allure.story("Login 測試")
    @allure.title("登入網址是否健康測試")
    @allure.description("測試網址是否存活")
    def test_start(self, browser):
        # 檢查網址是否健康
        if is_connection_work(url):
            browser.get(url)
            
            allure.dynamic.title("登入網址是否健康測試 Pass!")
            assert True
        else:
            with allure.step("截圖"):
                allure.attach(TestSelenium.browser.get_screenshot_as_png(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), allure.attachment_type.PNG)
            allure.dynamic.title("登入網址是否健康測試 Fail!")
            assert False
    
    @allure.story("Login 測試")
    @allure.title("登入資訊輸入正確測試")
    @allure.description("輸入正確的登入帳號以及密碼，檢查程式是否會成功登入。")
    def test_login(self, browser):
        test_login(browser) #用於分割 Test Case 時，先確認是否已經登入過

    def Exec_Test(self,case='All'):# 執行測試案例, exe_type 為打包pyinstaller 的參數

        case_name = config["test_environment"]["case"]
        if case_name == 'False': #空是 代表  沒有 傳  指定的case 
            if case == 'All':# 預設執行全部
                pytest.main(['-s', '-v', 'main.py::TestSelenium','-q', '--alluredir', './reports'])
            
            elif '-k' in case:# 指定相關字元 testcase , Ex: case: -k Soccer
                pytest.main(['%s'%case,'main.py','-s', '-v',
                '-q', '--alluredir', './reports'])
            
            else:# 指定 一個testcase ,Ex: case: test_TopMenuLeftSportsMenu
                pytest.main(['-s', '-v',  'main.py::TestSelenium::%s'%case, '--alluredir', './reports'])
        
        else:# 這邊一定要帶 -k , 所以先自己帶
            pytest.main(['-k %s'%case_name ,'main.py','-s', '-v',
                '-q', '--alluredir', './reports'])

# pytest運行
if __name__ == "__main__":
    Clean_Report() # 清除上次的report
    Create_env(url)
    #-k test_OneSoccer or OneBasketball or OneTennis or OneBaseball or OneCricket or OneVolleyball or OneEsports
    TestSelenium().Exec_Test(case= 'All' )
