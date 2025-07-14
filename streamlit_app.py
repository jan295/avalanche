import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

session = st.connection("snowflake").session()

st.title("Customer Sentiment and Delivery Analysis")

# Data loading functions
@st.cache_data
def load_reviews():
    query_reviews = """
    SELECT *,
        SNOWFLAKE.CORTEX.SENTIMENT(CUSTOMER_REVIEW) AS SENTIMENT_SCORE
    FROM PARSED_REVIEWS
    """
    return session.sql(query_reviews).to_pandas()

@st.cache_data
def load_shipping():
    query_shipping = "SELECT * FROM SHIPPING_LOGS"
    return session.sql(query_shipping).to_pandas()

# Load data
df_reviews = load_reviews()
df_shipping = load_shipping()

# Filter by product selection
products = df_reviews["PRODUCT"].unique().tolist()
selected_products = st.multiselect("Filter by Product:", products, default=products)

# Filtered Reviews
filtered_reviews = df_reviews[df_reviews["PRODUCT"].isin(selected_products)]

# Combined Data (Filtered)
combined_df = filtered_reviews.merge(df_shipping, on="ORDER_ID", how="inner")

# Display combined dataset
st.header("Combined Reviews & Shipping Data")
st.dataframe(combined_df)

# Average sentiment by product
st.header("Average Sentiment by Product")
avg_sentiment_product = combined_df.groupby("PRODUCT")["SENTIMENT_SCORE"].mean().sort_values()

fig1, ax1 = plt.subplots(figsize=(8,5))
avg_sentiment_product.plot(kind="barh", color="skyblue", ax=ax1)
ax1.set_xlabel("Sentiment Score")
ax1.set_ylabel("Product")
st.pyplot(fig1)

# Average sentiment by delivery status
st.header("Average Sentiment by Delivery Status")
avg_sentiment_status = combined_df.groupby("STATUS")["SENTIMENT_SCORE"].mean().sort_values()

fig2, ax2 = plt.subplots(figsize=(8,5))
avg_sentiment_status.plot(kind="barh", color="slateblue", ax=ax2)
ax2.set_xlabel("Sentiment Score")
ax2.set_ylabel("Delivery Status")
st.pyplot(fig2)

# Option to save data to Snowflake
if st.button("Save Combined Data to Snowflake"):
    session.write_pandas(combined_df, "COMBINED_REVIEWS_SHIPPING", auto_create_table=True, overwrite=True)
    st.success("Combined data successfully saved to Snowflake!")
