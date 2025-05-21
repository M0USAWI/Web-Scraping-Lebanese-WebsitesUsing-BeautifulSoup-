import requests
from bs4 import BeautifulSoup
import pandas as pd

electronics_data = []

for page in range(1, 11):
    url = f"https://hamdanelectronics.com/61-electronics?page={page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("div", class_="laberProduct-container")
    print(f"Page {page}: Found {len(products)} Electronics")

    for product in products:
        title_tag = product.find("h2", class_="productName")
        price_tag = product.find("span", class_="price")
        link_tag = product.find("a", href=True)

        title = title_tag.text.strip() if title_tag else "Unknown"
        price = price_tag.text.strip().replace(",", "").replace("$", "") if price_tag else "Unavailable"
        link = link_tag["href"] if link_tag else None
        brand = title.split()[0]

        electronics_data.append({
            "Brand": brand,
            "Item": title,
            "Price": price,
            "Link": link
        })

df = pd.DataFrame(electronics_data)

df.drop_duplicates(inplace=True)

df.to_csv("hamdan_electronics.csv", index=False)

print("Saved", len(df), "Electronics to hamdan_electronics.csv")