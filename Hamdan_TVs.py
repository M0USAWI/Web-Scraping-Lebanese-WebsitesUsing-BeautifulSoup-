import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

tv_data = []

for page in range(1, 4):
    url = f"https://hamdanelectronics.com/155-tvs?page={page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.find_all("div", class_="laberProduct-container")
    print(f"Page {page}: Found {len(products)} TVs")

    for product in products:
        title_tag = product.find("h2", class_="productName")
        price_tag = product.find("span", class_="price")
        link_tag = product.find("a", href=True)

        title = title_tag.text.strip() if title_tag else "Unknown"
        price = price_tag.text.strip().replace(",", "").replace("$", "") if price_tag else "Unavailable"
        link = link_tag["href"] if link_tag else None

        brand = title.split()[0]
        size_match = re.search(r'(\d{2,3})\s*(inch|")', title, re.IGNORECASE)
        size = size_match.group(1) if size_match else None
        smart = "Smart" if "smart" in title.lower() else "Not Smart"
        resolution = "4K" if "4k" in title.lower() else "FHD" if "fhd" in title.lower() else ("UHD" if "uhd" in title.lower() else "HD")
        display = "QLED" if "qled" in title.lower() else ("OLED" if "oled" in title.lower() else ("LCD" if "lcd" in title.lower() else "LED"))

        tv_data.append({
            "Brand": brand,
            "Size": size,
            "Smart": smart,
            "Display": display,
            "Resolution": resolution,
            "Price": price,
            "Link": link
        })

df = pd.DataFrame(tv_data)
df.drop_duplicates(inplace=True)
df.to_csv("hamdan_tvs.csv", index=False)
print("Saved", len(df), "TVs to hamdan_tvs.csv")
print(len(df))
