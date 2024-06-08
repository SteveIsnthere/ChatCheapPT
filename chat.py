from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import json

# context file path
if not os.path.exists("data"):
    os.makedirs("data")

file_path = "data/context.txt"

# usage tracking
usage_file_name = 'usage.json'
initial_data = {
    "read": 0,
    "write": 0
}
if not os.path.exists(usage_file_name):
    with open(usage_file_name, 'w') as json_file:
        json.dump(initial_data, json_file, indent=4)


def increment_counters(read_increment=0, write_increment=0):
    # Load the existing data
    with open(usage_file_name, 'r') as json_file:
        data = json.load(json_file)

    # Increment the values
    data['read'] += read_increment / 4
    data['write'] += write_increment / 4

    # Save the updated data back to the file
    with open(usage_file_name, 'w') as json_file:
        json.dump(data, json_file, indent=4)


# Initialize the Chrome WebDriver
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get('https://127.0.0.1:40000/?__theme=dark')

# element xpath
_input_element = "/html/body/gradio-app/div/div/div[1]/div/div/div[7]/div[4]/div/div/div/div/div/div[1]/label/textarea"
_submit_button = '/html/body/gradio-app/div/div/div[1]/div/div/div[7]/div[4]/div/div/button'
_clear_button = "/html/body/gradio-app/div/div/div[1]/div/div/div[7]/div[5]/button[3]"
_context_refresh_button = "/html/body/gradio-app/div/div/div[1]/div/div/div[7]/div[1]/div[2]/div/div/div[1]/button"

WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, _input_element)))


def get_chat_response(prompt):
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, _clear_button)))
    clear_button = driver.find_element(By.XPATH, _clear_button)
    clear_button.click()

    time.sleep(3)

    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "bot-row")))
    # WebDriverWait(driver, 10).until(
    #     lambda d: d.find_element(By.XPATH, _input_element) and d.find_element(By.XPATH, _input_element).is_enabled())
    # WebDriverWait(driver, 10).until(
    #     lambda d: d.find_element(By.XPATH, _submit_button) and d.find_element(By.XPATH, _submit_button).is_enabled())
    input_element = driver.find_element(By.XPATH, _input_element)
    input_element.send_keys(prompt + Keys.RETURN)
    time.sleep(1)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "bot-row")))

    response = ""
    while response != driver.find_element(By.CLASS_NAME, "bot-row").text or response == "":
        response = driver.find_element(By.CLASS_NAME, "bot-row").text
        time.sleep(0.7)

    increment_counters(len(prompt), len(response))

    return response


def get_chat_response_with_context(prompt, context):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(context)

    time.sleep(3)

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, _context_refresh_button)))
    context_refresh_button = driver.find_element(By.XPATH, _context_refresh_button)
    context_refresh_button.click()

    time.sleep(3)
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "bot-row")))

    input_element = driver.find_element(By.XPATH, _input_element)
    input_element.send_keys(prompt + Keys.RETURN)
    time.sleep(1)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "bot-row")))

    response = ""
    while response != driver.find_element(By.CLASS_NAME, "bot-row").text or response == "":
        response = driver.find_element(By.CLASS_NAME, "bot-row").text
        time.sleep(0.7)

    # delete context file
    os.remove(file_path)
    time.sleep(1)

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, _context_refresh_button)))
    context_refresh_button = driver.find_element(By.XPATH, _context_refresh_button)
    context_refresh_button.click()
    time.sleep(1)

    increment_counters(len(prompt), len(response))

    return response


def close_chat():
    driver.quit()
