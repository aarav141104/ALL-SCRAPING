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

# df = pd.DataFrame(columns=["Sr No.", "Agent Name", "Certificate No."])
url = "https://rerait.telangana.gov.in/SearchList/Search"
options = Options()
# options.add_argument("--headless")
page_sources = []
driver = webdriver.Chrome(
    service=Service(executable_path="./chromedriver"), options=options
)
driver.implicitly_wait(45)
driver.get(url)
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
registered_agent_element = driver.find_element(
    By.XPATH, "//input[contains(@id,'Agent') and contains(@name,'Type')]"
)
registered_agent_element.click()
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
page_sources.append(driver.page_source)
counter = 1
while True:
    try:
        if counter == 366:
            break
        next_button = driver.find_element(
            By.XPATH,
            "//button[contains(text(),'Next') and contains(@class,'btn') and contains(@class,'btn-success')]",
        )
        next_button.click()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        page_sources.append(driver.page_source)
        counter += 1
        logging.info(f"Done with {counter} pages")
    except:
        logging.info("No Next Button found")
        break

with open("telengana_page_sources.pkl", "wb") as file:
    pickle.dump(page_sources, file)
