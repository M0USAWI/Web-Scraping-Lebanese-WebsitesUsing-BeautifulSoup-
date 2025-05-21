from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

driver = webdriver.Chrome() 

electronics_data = []

for page in range(1, 3):
    url = f"https://youneselectric.com/collections/audio-1?page={page}"
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    products = soup.find_all("div", class_="product-item__info")
    print(f"Page {page}: Found {len(products)} Electronics")

    for product in products:
        title_tag = product.find("a", class_="product-item__title text--strong link")
        price_tag = product.find("span", class_="price price--highlight")

        title = title_tag.get_text(strip=True) if title_tag else "Unknown"
        if price_tag:
            price_match = re.search(r'(\d+[\.,]?\d*)', price_tag.get_text())
            price = f"${price_match.group(1)}" if price_match else "Unknown"
        else:
            price = "Unknown"

        link = "https://youneselectric.com" + title_tag["href"] if title_tag else None

        size_match = re.search(r'(\d{2,3})\s*[-"]?\s*(inch|")', title, re.IGNORECASE)
        size = size_match.group(1) if size_match else None
        smart = "Smart" if "smart" in title.lower() else "Not Smart"
        resolution = "4K" if "4k" in title.lower() else ("FHD" if "fhd" in title.lower() else "HD")
        display = (
            "QLED" if "qled" in title.lower() else
            "OLED" if "oled" in title.lower() else
            "LCD" if "lcd" in title.lower() else
            "LED"
        )

        electronics_data.append({
            "Brand": title,
            "Size": size,
            "Smart": smart,
            "Display": display,
            "Resolution": resolution,
            "Price": price,
            "Link": link
        })

driver.quit()

df = pd.DataFrame(electronics_data)
df.drop_duplicates(inplace=True)
for x in df.index:
    if pd.isna(df.loc[x,"Size"]):
     df.drop(x,inplace=True)

df.to_csv("youneselectric.csv", index=False)

print("Saved", len(df), "Electronics to youneselectric.csv")