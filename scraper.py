import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

url = sys.argv[1]
if not url.startswith("http"):
    url = "https://" + url

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)
driver.get(url)

time.sleep(3)   

soup = BeautifulSoup(driver.page_source, "html.parser")

driver.quit()

print(f"PAGE TITLE WITHOUT ANY HTML TAG:{soup.title.text} \n")
print()

print("PAGE BODY TEXT:")
Sentence_Body = (soup.get_text()).split()
print(Sentence_Body)
print()
print()
print()

print("ALL THE URLS THAT THE PAGE POINTS TO: \n")

for link in soup.find_all("a"):
    href = link.get("href")

    if href:
        full_url = urljoin(url, href)
        print(full_url)
