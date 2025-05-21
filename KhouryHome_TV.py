from bs4 import BeautifulSoup
import pandas as pd
import re

with open("C:/Users/hasan/Desktop/web scraping/kaystore.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

products = soup.find_all("div", class_="box-text box-text-products")
print("Found", len(products), "TVs")

tv_data = []

for box in products:
    title_link = box.select_one("p.name.product-title a")
    price_tag = box.find("span", class_="woocommerce-Price-amount")

    if not title_link:
        continue

    title = title_link.text.strip()
    raw_price = price_tag.find("bdi").text.strip() if price_tag and price_tag.find("bdi") else None
    link = title_link['href']

    brand = title.split()[0]
    size_match = re.search(r'(\d{2,3})\s*(inch|")', title, re.IGNORECASE)
    size = size_match.group(1) if size_match else None
    smart = "Smart" if "smart" in title.lower() else "Not Smart"
    resolution = "4K" if "4k" in title.lower() else ("FHD" if "fhd" in title.lower() else "HD")

    if "qled" in title.lower():
        display = "QLED"
    elif "oled" in title.lower():
        display = "OLED"
    elif "lcd" in title.lower():
        display = "LCD"
    else:
        display = "LED"

    tv_data.append({
        "Brand": brand,
        "Size": size,
        "Smart": smart,
        "Display": display,
        "Resolution": resolution,
        "Price": raw_price,
        "Link": link
    })

df = pd.DataFrame(tv_data)
df.to_csv("kaystore_tvs.csv", index=False)
print("Saved", len(tv_data), "TVs to kaystore_tvs.csv")