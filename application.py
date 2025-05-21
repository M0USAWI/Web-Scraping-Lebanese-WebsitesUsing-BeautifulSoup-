import pandas as pd

choice = input("Would you like to check our TVs or other Electronics? (TV/Electronics): ").strip().lower()

if choice == "tv":
    df_hamdan = pd.read_csv("hamdan_tvs.csv")
    df_kstore = pd.read_csv("kaystore_tvs.csv")
    df_younes = pd.read_csv("youneselectric.csv")

    df = pd.concat([df_hamdan, df_kstore, df_younes], ignore_index=True)

    df["Price"] = pd.to_numeric(df["Price"].replace('[\$,]', '', regex=True), errors='coerce')
    df = df.dropna(subset=["Price"])

    if input("Would you like to enter a specific price range? (yes/no): ").strip().lower() == "yes":
        try:
            min_price = float(input("Enter minimum price: "))
            max_price = float(input("Enter maximum price: "))
            df = df[(df["Price"] >= min_price) & (df["Price"] <= max_price)]
        except ValueError:
            print("Invalid price input. Skipping price filter.")

    if input("Would you like to filter by TV inch? (yes/no): ").strip().lower() == "yes":
        try:
            min_size = int(input("Enter minimum size (in inches): "))
            max_size = int(input("Enter maximum size (in inches): "))
            df["Size"] = pd.to_numeric(df["Size"], errors='coerce')
            df = df.dropna(subset=["Size"])
            df = df[(df["Size"] >= min_size) & (df["Size"] <= max_size)]
        except ValueError:
            print("Invalid size input. Skipping size filter.")

    if input("Would you like to filter by display type (LCD, LED, OLED, QLED)? (yes/no): ").strip().lower() == "yes":
        display_type = input("Enter display type: ").strip().upper()
        valid_types = ["LED", "LCD", "QLED", "OLED"]
        if display_type in valid_types:
            df = df[df["Display"].str.upper() == display_type]
        else:
            print("Invalid display type. Showing all types.")

    if df.empty:
        print("\nNo TVs match your filters.")
    else:
        print(f"\nFound {len(df)} TVs matching your filters:\n")
        print(df.to_string())

if input("\nWould you like to check TV brackets? (yes/no): ").strip().lower() == "yes":
    df_brackets = pd.read_csv("brackets.csv")
    df_brackets["price"] = pd.to_numeric(df_brackets["price"].replace('[\$,]', '', regex=True), errors='coerce')
    df_brackets = df_brackets.dropna(subset=["price"])

    if input("Would you like to enter a budget for brackets? (yes/no): ").strip().lower() == "yes":
        try:
            min_b_price = float(input("Enter minimum bracket price: "))
            max_b_price = float(input("Enter maximum bracket price: "))
            df_brackets = df_brackets[(df_brackets["price"] >= min_b_price) & (df_brackets["price"] <= max_b_price)]
        except ValueError:
            print("Invalid price input. Showing all brackets.")

    if df_brackets.empty:
        print("\nNo brackets match your criteria.")
    else:
        print("\nAvailable TV Brackets:\n")
        print(df_brackets.to_string())

if input("\nWould you like to check TV units? (yes/no): ").strip().lower() == "yes":
    df_units = pd.read_csv("tvunit.csv")
    df_units["price"] = pd.to_numeric(df_units["price"].replace('[\$,]', '', regex=True), errors='coerce')
    df_units = df_units.dropna(subset=["price"])

    if input("Would you like to enter a budget for TV units? (yes/no): ").strip().lower() == "yes":
        try:
            min_u_price = float(input("Enter minimum TV unit price: "))
            max_u_price = float(input("Enter maximum TV unit price: "))
            df_units = df_units[(df_units["price"] >= min_u_price) & (df_units["price"] <= max_u_price)]
        except ValueError:
            print("Invalid price input. Showing all TV units.")

    if df_units.empty:
        print("\nNo TV units match your criteria.")
    else:
        print("\nAvailable TV Units:\n")
        print(df_units.to_string())

if input("\nWould you like to search for another electronic item? (yes/no): ").strip().lower() == "yes":
    df_electronics = pd.read_csv("hamdan_electronics.csv")
    item_name = input("Enter the name of the item you want to search for: ").strip().lower()
    filtered_items = df_electronics[df_electronics["Item"].str.lower().str.contains(item_name)]

    if input("Would you like to filter by budget? (yes/no): ").strip().lower() == "yes":
        try:
            min_e_price = float(input("Enter minimum price: "))
            max_e_price = float(input("Enter maximum price: "))
            filtered_items["Price"] = pd.to_numeric(filtered_items["Price"].replace('[\$,]', '', regex=True), errors='coerce')
            filtered_items = filtered_items[(filtered_items["Price"] >= min_e_price) & (filtered_items["Price"] <= max_e_price)]
        except ValueError:
            print("Invalid price input. Showing all matching items.")

    if filtered_items.empty:
        print(f"\nNo items found matching '{item_name}' with the specified criteria.")
    else:
        print(f"\nItems matching '{item_name}':\n")
        print(filtered_items.to_string())

print("\nThank you for visiting our store!")