import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

st.title("Silver Price Calculator & Sales Analysis")

st.header("Silver Price Calculator")
unit = st.radio("Unit:", ["Grams", "Kilograms"])
weight = st.number_input("Weight:", min_value=0.0, step=1.0)
price = st.number_input("Price per gram (INR):", min_value=0.0, step=1.0)
rate = st.number_input("INR to USD Rate:", value=83.0, step=1.0)

weight_g = weight * 1000 if unit == "Kilograms" else weight
total = weight_g * price
st.markdown(f"#### **Total Cost: ₹{total:.2f} | ${total/rate:.2f}**")

st.header("Historical Analysis")
filter_opt = st.selectbox("Price Range:", 
    ["All", "< 20,000", "20,000-30,000", "> 30,000"])

df = pd.read_csv('historical_silver_price.csv')

data = df.copy()
if filter_opt == "< 20,000":
    data = data[data['Silver_Price_INR_per_kg'] < 20000]
elif filter_opt == "20,000-30,000":
    data = data[(data['Silver_Price_INR_per_kg'] >= 20000) & (data['Silver_Price_INR_per_kg'] <= 30000)]
elif filter_opt == "> 30,000":
    data = data[data['Silver_Price_INR_per_kg'] > 30000]

plt.figure(figsize=(12, 5))
plt.plot(data['Silver_Price_INR_per_kg'], linewidth=2, color='silver')
plt.xlabel("Time Period")
plt.ylabel("Price (INR/kg)")
plt.title(f"Silver Prices - {filter_opt}")
plt.grid(alpha=0.3)
st.pyplot(plt)

# Question 2

state_df = pd.read_csv('state_wise_silver_purchased_kg.csv')

st.header("State-wise Silver Sales Analysis")

st.subheader("India State-wise Silver Purchases Map")
india_states = gpd.read_file('ne_10m_admin_1_states_provinces.zip')

# Keep only states belonging to India (Natural Earth uses the 'admin' column for country)
if 'admin' in india_states.columns:
    india_states = india_states[india_states['admin'].str.lower() == 'india']

# Helper to match state names case-insensitively
def _get_purchase(name):
    if pd.isna(name):
        return 0.0
    match = state_df[state_df['State'].str.lower() == str(name).lower()]
    return float(match['Silver_Purchased_kg'].values[0]) if len(match) > 0 else 0.0

india_states['Silver_Purchased_kg'] = india_states['name'].apply(_get_purchase)

fig, ax = plt.subplots(figsize=(14, 10))
india_states.plot(column='Silver_Purchased_kg', ax=ax, legend=True,
                  cmap='Greens', edgecolor='black', linewidth=0.5)
ax.set_title('State-wise Silver Purchases (kg)', fontsize=14, fontweight='bold')

# Zoom to the India bounds so the full world is not shown
minx, miny, maxx, maxy = india_states.total_bounds
ax.set_xlim(minx, maxx)
ax.set_ylim(miny, maxy)

ax.axis('off')
st.pyplot(fig)

top5 = state_df.nlargest(5, 'Silver_Purchased_kg')
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(top5['State'], top5['Silver_Purchased_kg'], color='steelblue')
ax.set_xlabel('Silver Purchased (kg)')
ax.set_title('Top 5 States - Silver Purchases')
st.pyplot(fig)

st.subheader("Monthly Silver Price Trends (January)")
jan_data = df[df['Month'] == 'Jan']
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(jan_data['Year'], jan_data['Silver_Price_INR_per_kg'], marker='o', linewidth=2, color='darkblue')
ax.set_xlabel('Year')
ax.set_ylabel('Price (INR/kg)')
ax.set_title('January Silver Price Trends Over Years')
ax.grid(alpha=0.3)
st.pyplot(fig)
