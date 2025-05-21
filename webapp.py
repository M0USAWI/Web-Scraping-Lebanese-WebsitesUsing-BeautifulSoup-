import streamlit as st
import pandas as pd

st.title("Electronics & TV Store")

choice = st.radio("What would you like to check?", ["TVs", "Electronics"])

if choice == "TVs":
    df1 = pd.read_csv("hamdan_tvs.csv")
    df2 = pd.read_csv("kaystore_tvs.csv")
    df3 = pd.read_csv("youneselectric.csv")
    df = pd.concat([df1, df2, df3], ignore_index=True)
    df["Price"] = pd.to_numeric(df["Price"].replace('[\$,]', '', regex=True), errors='coerce')
    df = df.dropna(subset=["Price"])

    min_price, max_price = st.slider("Select TV Price Range", 0, int(df["Price"].max()), (0, int(df["Price"].max())))
    df = df[(df["Price"] >= min_price) & (df["Price"] <= max_price)]

    if st.checkbox("Filter by TV Size"):
        min_size, max_size = st.slider("Select Size Range (inches)", 0, 100, (0, 100))
        df["Size"] = pd.to_numeric(df["Size"], errors='coerce')
        df = df.dropna(subset=["Size"])
        df = df[(df["Size"] >= min_size) & (df["Size"] <= max_size)]

    if st.checkbox("Filter by Display Type"):
        display_type = st.selectbox("Select Display Type", ["Any", "LED", "LCD", "OLED", "QLED"])
        if display_type != "Any":
            df = df[df["Display"].str.upper() == display_type]

    st.subheader("Matching TVs:")
    st.dataframe(df)

    if st.checkbox("Would you like to check TV Brackets?"):
        df_brackets = pd.read_csv("brackets.csv")
        df_brackets["price"] = pd.to_numeric(df_brackets["price"].replace('[\$,]', '', regex=True), errors='coerce')
        df_brackets = df_brackets.dropna(subset=["price"])

        min_b_price, max_b_price = st.slider("Select Bracket Price Range", 0, int(df_brackets["price"].max()), (0, int(df_brackets["price"].max())))
        df_brackets = df_brackets[(df_brackets["price"] >= min_b_price) & (df_brackets["price"] <= max_b_price)]

        st.subheader("Available Brackets:")
        st.dataframe(df_brackets)

    if st.checkbox("Would you like to check TV Units?"):
        df_units = pd.read_csv("tvunit.csv")
        df_units["price"] = pd.to_numeric(df_units["price"].replace('[\$,]', '', regex=True), errors='coerce')
        df_units = df_units.dropna(subset=["price"])

        min_u_price, max_u_price = st.slider("Select TV Unit Price Range", 0, int(df_units["price"].max()), (0, int(df_units["price"].max())))
        df_units = df_units[(df_units["price"] >= min_u_price) & (df_units["price"] <= max_u_price)]

        st.subheader("Available TV Units:")
        st.dataframe(df_units)

elif choice == "Electronics":
    df_electronics = pd.read_csv("hamdan_electronics.csv")
    search_item = st.text_input("Enter the item name you want to search for:")

    if search_item:
        filtered_items = df_electronics[df_electronics["Item"].str.lower().str.contains(search_item.lower())]

        if st.checkbox("Would you like to filter this item by price?"):
            filtered_items["Price"] = pd.to_numeric(filtered_items["Price"].replace('[\$,]', '', regex=True), errors='coerce')
            filtered_items = filtered_items.dropna(subset=["Price"])

            min_e_price, max_e_price = st.slider("Select Item Price Range", 0, int(filtered_items["Price"].max()), (0, int(filtered_items["Price"].max())))
            filtered_items = filtered_items[(filtered_items["Price"] >= min_e_price) & (filtered_items["Price"] <= max_e_price)]

        st.subheader("Matching Electronics:")
        st.dataframe(filtered_items)

st.success("Thank you for visiting our store!")