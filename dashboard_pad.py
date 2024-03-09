import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_payments_df(payments_df):
    count_payments = payments_df.groupby(by="payment_type").order_id.nunique().sort_values(ascending=False)
    count_payments_df = count_payments.reset_index().rename(columns={"order_id":"payments_count"})
    return count_payments_df

def create_sellers_df(sellers_df):
    count_sellers = sellers_df.groupby(by="seller_city").seller_id.nunique().sort_values(ascending=False)
    count_sellers_df = count_sellers.reset_index().rename(columns={"seller_id":"sellers_count"})
    return count_sellers_df

def create_reviews_df(reviews_df):
    count_reviews = reviews_df.groupby(by="review_score").order_id.nunique().sort_values(ascending=False)
    count_reviews_df = count_reviews.reset_index().rename(columns={"order_id":"reviews_count"})
    return count_reviews_df

all_df = pd.read_csv("all_data.csv", low_memory=False)

datetime_columns = ["review_creation_date", "review_answer_timestamp"]
all_df.sort_values(by="review_creation_date", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["review_creation_date"].min()
max_date = all_df["review_creation_date"].max()

with st.sidebar:
    st.image("https://github.com/salmajeir/ecommerce/raw/main/logo baju.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["review_creation_date"] >= str(start_date)) & 
                (all_df["review_creation_date"] <= str(end_date))]

st.header('Brazilian E-Commerce Public Dataset by Olist')

count_payments_df = create_payments_df(main_df)
st.subheader('Number of Customer by Payment Types')
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="payments_count",y="payment_type",data=count_payments_df.sort_values(by="payments_count",ascending=False),palette="viridis")
plt.title("Number of Customer by Payment Types", loc="center", fontsize=15)
plt.xlabel("Count Customer", fontsize=14)
plt.ylabel("Payment Types", fontsize=14)
st.pyplot(fig)

count_sellers_df = create_sellers_df(main_df)
st.subheader('Number of Customer by Each City')
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="sellers_count",y="seller_city",data=count_sellers_df.sort_values(by="sellers_count",ascending=False).head(10),palette="viridis")
plt.title("Number of Customer for Each City", loc="center", fontsize=15)
plt.xlabel("Count Seller", fontsize=14)
plt.ylabel("Seller City", fontsize=14)
st.pyplot(fig)

count_reviews_df = create_reviews_df(main_df)
st.subheader('Number of Reviews by Score')
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="review_score",y="reviews_count",data=count_reviews_df.sort_values(by="reviews_count",ascending=False).head(10),palette="viridis")
plt.title("Number of Reviews by Score", loc="center", fontsize=15)
plt.xlabel("Score", fontsize=14)
plt.ylabel("Number of Reviews", fontsize=14)
st.pyplot(fig)
