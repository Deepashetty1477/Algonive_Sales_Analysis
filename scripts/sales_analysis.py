# ============================================
# SALES DATA ANALYSIS - BASIC VERSION
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1️⃣ Load Dataset
df = pd.read_csv("data/retail_sales_dataset.csv")
print("✅ Dataset Loaded Successfully!\n")

# 2️⃣ View Basic Info
print("First 5 Rows:")
print(df.head(), "\n")

print("Dataset Info:")
print(df.info(), "\n")

# 3️⃣ Clean Data
df.drop_duplicates(inplace=True)
df['Date'] = pd.to_datetime(df['Date'])  # Convert Date column
print("✅ Data Cleaned!\n")

# 4️⃣ Check for Missing Values
print("Missing Values:")
print(df.isnull().sum(), "\n")

# 5️⃣ Basic Analysis
print("Basic Statistics:")
print(df.describe(), "\n")

# 6️⃣ Visualization: Total Sales Over Time
plt.figure(figsize=(10,6))
df.groupby('Date')['Total Amount'].sum().plot(title="Total Sales Over Time", color='green')
plt.xlabel("Date")
plt.ylabel("Total Sales (₹)")
plt.tight_layout()
plt.show()

# 7️⃣ Sales by Product Category
plt.figure(figsize=(8,5))
sns.barplot(x='Product Category', y='Total Amount', data=df, estimator=sum, palette='Set2')
plt.title("Sales by Product Category")
plt.tight_layout()
plt.show()

# 8️⃣ Gender-wise Total Spending
plt.figure(figsize=(6,4))
sns.barplot(x='Gender', y='Total Amount', data=df, estimator=sum, palette='pastel')
plt.title("Sales by Gender")
plt.tight_layout()
plt.show()

# ============================================
# 🔮 SALES FORECASTING USING PROPHET
# ============================================

from prophet import Prophet

# Prepare data for Prophet
# Prophet expects columns named 'ds' (date) and 'y' (value)
forecast_df = df[['Date', 'Total Amount']].rename(columns={'Date': 'ds', 'Total Amount': 'y'})

# Initialize and train the model
model = Prophet()
model.fit(forecast_df)

# Create future dates for prediction (next 30 days)
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# Plot forecast
model.plot(forecast)
plt.title("Sales Forecast for Next 30 Days")
plt.show()

# Optional: Save forecast results
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv("outputs/sales_forecast.csv", index=False)
print("✅ Forecast saved to outputs/sales_forecast.csv")

