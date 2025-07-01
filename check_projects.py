import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# ─── Load credentials ────────────────────────────────────────────────────────────
load_dotenv()  # loads from .env if present
USERNAME = os.getenv("DA_USER")
PASSWORD = os.getenv("DA_PASS")
if not USERNAME or not PASSWORD:
    raise RuntimeError("Missing DA_USER or DA_PASS environment variables")
# ──────────────────────────────────────────────────────────────────────────────────

LOGIN_URL            = "https://example.com/login"
PROJECTS_URL         = "https://example.com/dashboard/projects"
USERNAME_FIELD       = "input[name='username']"
PASSWORD_FIELD       = "input[name='password']"
SUBMIT_BUTTON        = "button[type='submit']"
PROJECT_ROW_SELECTOR = "table#projects-list tbody tr"

def login_and_get_driver():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        options=opts
    )
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, USERNAME_FIELD)))
    driver.find_element(By.CSS_SELECTOR, USERNAME_FIELD).send_keys(USERNAME)
    driver.find_element(By.CSS_SELECTOR, PASSWORD_FIELD).send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, SUBMIT_BUTTON).click()
    wait.until(EC.url_contains("dashboard"))
    return driver

def count_projects(html):
    soup = BeautifulSoup(html, "html.parser")
    return len(soup.select(PROJECT_ROW_SELECTOR))

def main():
    driver = login_and_get_driver()
    try:
        driver.get(PROJECTS_URL)
        # wait for table to appear
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, PROJECT_ROW_SELECTOR))
        )
        count = count_projects(driver.page_source)
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        if count > 1:
            print(f"[{ts}] You have {count} real projects!")
        else:
            print(f"[{ts}] Only the ‘Welcome’ row ({count} rows).")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
