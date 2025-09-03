# load excel file and scraping the wiki articles and storing them as txt file in data folder for each wiki
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import os

def load_excel(excel_file):
  df = pd.read_excel(excel_file)
  if "url" not in df.columns:
    raise ValueError("Excel file must have a column named 'url'")
  else:
    urls = df['url'].tolist()
  return urls

def scrape_wiki(urls):
  for url in urls:
    r = requests.get(url, headers = {"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "lxml")

    content_div = soup.find("div", {"id": "mw-content-text"})
    if content_div:
      paragraphs = content_div.find_all("p")
    else:
      return

    clean_text = []
    for p in paragraphs:
      text = p.get_text()
      text = re.sub(r"\[\d+\]"," ",text)
      clean_text.append(text.strip())
    article_text = "\n".join(clean_text)

    title = soup.find("title")
    file_name = title.get_text().replace(" - Wikipedia","")+".txt"
    output_file = os.path.join("data/raw/", file_name)
    with open(output_file, "w", encoding="utf-8") as file:
      file.write(article_text)
    print(f"Saved: {file_name}")

