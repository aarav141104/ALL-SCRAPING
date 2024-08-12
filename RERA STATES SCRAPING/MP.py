from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
import pickle
import pandas as pd


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("scraping.log"), logging.StreamHandler()],
)

url = "https://www.rera.mp.gov.in/agents/"
options = Options()
page_sources = []
driver = webdriver.Chrome(
    service=Service(executable_path="./chromedriver"), options=options
)
driver.implicitly_wait(45)
driver.get(url)
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
page_sources.append(driver.page_source)
counter = 1
while True:
    if counter == 142:
        break
    next_element = driver.find_element(By.XPATH, "//a[contains(text(),'Next')]")
    next_element.click()
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    page_sources.append(driver.page_source)
    counter += 1

with open("mp.pkl", "wb") as file:
    pickle.dump(page_sources, file)
