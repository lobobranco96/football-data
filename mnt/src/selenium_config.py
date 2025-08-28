from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def selenium_webdriver():
  """
  Inicializa o driver do Selenium com Chromium em modo headless.

  Returns:
      webdriver.Chrome: instância configurada do driver.
  """
  chrome_options = Options()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  service = Service("/usr/local/share/chrome/chromedriver")
  return webdriver.Chrome(service=service, options=chrome_options)
