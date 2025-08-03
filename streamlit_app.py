import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

session = st.connection("snowflake").session()

st.title("Customer Sentiment and Delivery Analysis")

# Data loading functions
@st.cache_data
def load_data():
    query_reviews = """
    SELECT
        *
    FROM
        REVIEWS_WITH_SENTIMENT
    """
    return session.sql(query_reviews).to_pandas()

# Load data
df = load_data()

# Filter by product selection
products = df["PRODUCT"].unique().tolist()
selected_products = st.multiselect("Filter by Product:", products, default=products)

# Filtered Reviews
filtered_reviews = df[df["PRODUCT"].isin(selected_products)]

# Display combined dataset
st.header("Combined Reviews & Shipping Data")
st.dataframe(df)

# Average sentiment by product
st.header("Average Sentiment by Product")
avg_sentiment_product = df.groupby("PRODUCT")["SENTIMENT_SCORE"].mean().sort_values()

fig1, ax1 = plt.subplots(figsize=(8,5))
avg_sentiment_product.plot(kind="barh", color="skyblue", ax=ax1)
ax1.set_xlabel("Sentiment Score")
ax1.set_ylabel("Product")
st.pyplot(fig1)

# Average sentiment by delivery status
st.header("Average Sentiment by Delivery Status")
avg_sentiment_status = df.groupby("STATUS")["SENTIMENT_SCORE"].mean().sort_values()

fig2, ax2 = plt.subplots(figsize=(8,5))
avg_sentiment_status.plot(kind="barh", color="slateblue", ax=ax2)
ax2.set_xlabel("Sentiment Score")
ax2.set_ylabel("Delivery Status")
st.pyplot(fig2)
