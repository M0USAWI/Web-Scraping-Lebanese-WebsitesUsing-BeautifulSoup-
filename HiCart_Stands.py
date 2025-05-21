from bs4 import BeautifulSoup
import pandas as pd
import re

stands_data = []

with open("C:/Users/hasan/Desktop/web scraping/bracketshicart.html", "r", encoding="utf-8") as files:
    soup = BeautifulSoup(files, "html.parser")

products = soup.find_all("div", class_="product-details")
print("Found", len(products), "stands")

for product in products:
    title_tag = product.find("h2", class_="product-name")
    a_tag = product.find("a", href=True)

    regular_price_tag = product.find("span", class_="regular-price")
    if regular_price_tag:
        price_tag = regular_price_tag.find("span", class_="price")
        sale_status = "No Sale"
    else:
        special_price_tag = product.find("p", class_="special-price")
        if special_price_tag:
            price_tag = special_price_tag.find("span", class_="price")
            sale_status = "Sale"

    if title_tag and price_tag and a_tag:
        title = title_tag.get_text(strip=True)
        price = price_tag.get_text(strip=True).replace("$", "")
        link = a_tag["href"]

        if link.startswith("https"):
            stands_data.append({
                "title": title,
                "price": price,
                "sale": sale_status,
                "link": link
            })

df = pd.DataFrame(stands_data)
df.to_csv("brackets.csv", index=False)
print("Saved", len(df), "rows to brackets.csv")