from bs4 import BeautifulSoup
import pandas as pd
import re

tvunit_data = []

files = [
    "C:/Users/hasan/Desktop/web scraping/testtest1.html",
    "C:/Users/hasan/Desktop/web scraping/testtest2.html"
]

for file_path in files:
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        products = soup.find_all("div", class_="product-details")
        print(f"Found {len(products)} TV Units in {file_path}")

        for product in products:
            title_tag = product.find("h2", class_="product-name")
            a_tag = product.find("a", href=True)

            sale_status = "No Sale"
            price_tag = None

            regular_price_tag = product.find("span", class_="regular-price")
            if regular_price_tag:
                price_tag = regular_price_tag.find("span", class_="price")
            else:
                special_price_tag = product.find("p", class_="special-price")
                if special_price_tag:
                    price_tag = special_price_tag.find("span", class_="price")
                    sale_status = "Sale"

            if title_tag and price_tag and a_tag:
                title = title_tag.get_text(strip=True)
                price = price_tag.get_text(strip=True).replace("$", "").strip()
                link = a_tag["href"]

                if link.startswith("https"):
                    tvunit_data.append({
                        "title": title,
                        "price": price,
                        "Sale": sale_status,
                        "link": link
                    })

df = pd.DataFrame(tvunit_data)
df.to_csv("tvunit.csv", index=False)
print(f"Saved {len(df)} rows to tvunit.csv")