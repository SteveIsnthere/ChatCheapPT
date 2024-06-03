from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize the Chrome WebDriver
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get('https://127.0.0.1:40000/?__theme=dark')


# element xpath
_input_element = "/html/body/gradio-app/div/div/div[1]/div/div/div[7]/div[4]/div/div/div/div/div/div[1]/label/textarea"
_clear_button = "/html/body/gradio-app/div/div/div[1]/div/div/div[7]/div[5]/button[3]"

WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, _input_element)))


def get_response(prompt):
    input_element = driver.find_element(By.XPATH, _input_element)
    input_element.send_keys(prompt + Keys.RETURN)
    time.sleep(1)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "bot-row")))

    response = ""
    while response != driver.find_element(By.CLASS_NAME, "bot-row").text:
        response = driver.find_element(By.CLASS_NAME, "bot-row").text
        time.sleep(0.5)

    print(response)

    clear_button = driver.find_element(By.XPATH, _clear_button)
    clear_button.click()
    time.sleep(0.8)


get_response("write a 700 words essay about ai")
get_response("do you know who i am?")

driver.quit()