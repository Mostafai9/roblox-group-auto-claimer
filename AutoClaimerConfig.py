import undetected_chromedriver as uc
from selenium_stealth import stealth
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from fake_useragent import UserAgent
import os
import asyncio
import requests

useragent = UserAgent()
current_path = os.getcwd()
chrome_driver_path = current_path + "/capsolver"


async def type_in_textbox(driver, textbox_xpath, input_text):
    try:
        textbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, textbox_xpath)))
        textbox.clear()
        textbox.send_keys(input_text)
    except TimeoutException as te:
        print("Timeout waiting for textbox:", te)
    except Exception as e:
        print("Error typing in textbox:", e)


async def click_element(driver, element_xpath):
    try:
        element = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, element_xpath)))
        element.click()
    except TimeoutException:
        await asyncio.sleep(0.5)
        if element_xpath in ["/html/body/div[5]/div[1]/div[2]/div/div/button[2]",
                             "/html/body/div[3]/main/div[2]/div[1]/div/div/div[4]/div/div[1]/div[2]/div[3]/button",
                             "/html/body/div[3]/main/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/div[3]/button"]:
            return
        await click_element(driver, element_xpath)
    except Exception as e:
        print("Error clicking element:", e)


async def element_exists(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
        return True
    except NoSuchElementException:
        return False


async def get_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'user-agent={useragent}')
    chrome_options.add_argument(
        "--load-extension={0}".format(chrome_driver_path))

    driver = uc.Chrome(executable_path=current_path, options=chrome_options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    return driver


async def CheckCaptcha(driver):
    if await element_exists(driver, "/html/body/div[20]/div[2]/div") or await element_exists(driver, "/html/body/div[20]/div[2]/div/div"):
        while True:
            if await element_exists(driver, "/html/body/div[20]/div[2]/div") or await element_exists(driver, "/html/body/div[20]/div[2]/div/div"):
                print("Captcha Exists Still")
                await asyncio.sleep(0.5)
            else:
                print("No Captcha Continuing")
                break


async def Login(driver):
    driver.get("https://roblox.com/login")
    await type_in_textbox(
        driver, "/html/body/div[3]/main/div[2]/div/div/div/div[1]/div/div/form/div[1]/input", "username") #replace "username" with ur username for example "MostafaAuto"
    await type_in_textbox(
        driver, "/html/body/div[3]/main/div[2]/div/div/div/div[1]/div/div/form/div[2]/input", "password") #replace "password" with ur password for example "1234"
    await click_element(
        driver, "/html/body/div[5]/div[1]/div[2]/div/div/button[2]")
    await click_element(
        driver, "/html/body/div[3]/main/div[2]/div/div/div[1]/div[1]/div/div/form/button")
    await CheckCaptcha(driver)


async def VisitWebsite(driver, url):
    driver.get(url)


async def JoinNClaimGroup(driver, url, ctx):
    driver.get(url)
    await asyncio.sleep(0)
    await click_element(
        driver, "/html/body/div[3]/main/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/div[2]/div[3]/div/button")
    await asyncio.sleep(0.1)
    await CheckCaptcha(driver)
    await asyncio.sleep(0.3)
    await CheckCaptcha(driver)
    await asyncio.sleep(0.5)
    await CheckCaptcha(driver)
    await click_element(
        driver, "/html/body/div[3]/main/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/div[3]/button")
    await asyncio.sleep(0)
    await CheckCaptcha(driver)

    
    claim_button_xpath = "/html/body/div[3]/main/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div/div/ul/li[1]/button"

    await click_element(driver, claim_button_xpath)

    
    webhook_url = "webhook here bc im cool"
    
    
    message_content = "Group claimed successfully" # edit this to whatever u want idc

    payload = {
        "content": message_content
    }

    headers = {
        "Content-Type": "application/json"
    }

    
    response = requests.post(webhook_url, json=payload, headers=headers)

    if response.status_code != 204:
        print(f"Failed to send message via webhook Status code: {response.status_code}")
    else:
        print("Group Claimed successfully Message sent via webhook")