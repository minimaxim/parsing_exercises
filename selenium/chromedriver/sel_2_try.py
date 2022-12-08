from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from auth_data import vk_pass, vk_login


options = Options()
options.add_argument("window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get('https://vk.com/')
    time.sleep(2)
    email_input = driver.find_element(By.ID, "index_email")
    email_input.clear()
    email_input.send_keys(vk_login)
    time.sleep(2)
    login_button = driver.find_element(By.CLASS_NAME, 'VkIdForm__signInButton').click()
    time.sleep(2)
    pass_input = driver.find_element(By.NAME, 'password')
    pass_input.clear()
    pass_input.send_keys(vk_pass)
    time.sleep(2)
    in_button = driver.find_element(By.CLASS_NAME, "vkuiButton__in").click()
    time.sleep(10)

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()