import os.path
import pickle
import time

from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from configs import *

class AccauntTwiter:

    def __init__(self):
        pass

    def create_browser(self):
        self.worked = True
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        # В фоновый режим
        # chrome_options.headless = True

        caps = DesiredCapabilities().CHROME
        # caps["pageLoadStrategy"] = "normal"  # complete (полная загрузка страницы)
        # caps["pageLoadStrategy"] = "eager"  #  interactive
        caps["pageLoadStrategy"] = "none"

        # Создаём браузер
        self.brower = webdriver.Chrome(executable_path=PATCH_DRIVER, chrome_options=chrome_options, desired_capabilities=caps)


    def create_proxy_browser(self, proxy_username, proxy_password, proxy_ip, proxy_port):
        self.worked = True
        # Отключаем отображение изображений для оптимизации и так медленых прокси
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        #В фоновый режим
        # chrome_options.headless = True

        # Настраиваем прокси
        seleniumwire_options = {
            "proxy": {"http": f"http://{proxy_username}:{proxy_password}@{proxy_ip}:{proxy_port}", "verify_ssl": False}}

        caps = DesiredCapabilities().CHROME
        # caps["pageLoadStrategy"] = "normal"  # complete (полная загрузка страницы)
        # caps["pageLoadStrategy"] = "eager"  #  interactive
        caps["pageLoadStrategy"] = "none"

        # Создаём браузер
        self.brower = webdriver.Chrome(executable_path=PATCH_DRIVER, seleniumwire_options=seleniumwire_options,
                                       chrome_options=chrome_options, desired_capabilities=caps)

    def cls_broser(self):
        # При вызове этой функции закрывается текущий браузер
        try:
            self.worked = False
            self.brower.close()
            self.brower.quit()
        except Exception as ex:
            print(ex)

    def authorization_for_login (self , login, password , tag ):
        self.brower.get('https://twitter.com/i/flow/login')

        #Подождём загрузки поля ввода имени
        try:
            WebDriverWait(self.brower, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))
            )
        except:
            #Если недождались попытаемся повторить поытку
            self.brower.refresh()

    def authorization_for_cookies (self):
        pass

    def check_cookies (self):
        pass
