from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import matplotlib.pyplot as plt
import os

# ================= CONFIGURATION =================
DATA_PATH = "data/retail_sales_dataset.csv"      # Your dataset
IMG_PATH = "dashboard/dashboard_screenshot1.png" # One of your screenshots
OUTPUT_PDF = "Sales_Analysis_Report.pdf"         # Output report file
# =================================================

# Create PDF file
pdf = SimpleDocTemplate(OUTPUT_PDF, pagesize=A4)
styles = getSampleStyleSheet()
content = []

# Title
content.append(Paragraph("Sales Analysis Report", styles["Title"]))
content.append(Spacer(1, 20))

# ================= DATA ANALYSIS =================
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)

    # Convert Date column to datetime and extract month
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month_name()

    # Basic summary statistics
    total_sales = df["Total Amount"].sum()
    avg_sales = df["Total Amount"].mean()
    top_category = df["Product Category"].value_counts().idxmax()

    # Add summary details
    summary = f"""
    <b>Total Sales:</b> ₹{total_sales:,.2f}<br/>
    <b>Average Sales:</b> ₹{avg_sales:,.2f}<br/>
    <b>Top Product Category:</b> {top_category}
    """
    content.append(Paragraph(summary, styles["Normal"]))
    content.append(Spacer(1, 20))

    # ================= SALES CHART =================
    plt.figure(figsize=(8, 4))
    df.groupby("Month")["Total Amount"].sum().plot(kind="bar", color="skyblue")
    plt.title("Total Sales by Month")
    plt.xlabel("Month")
    plt.ylabel("Total Sales (₹)")
    plt.tight_layout()
    chart_path = "sales_chart.png"
    plt.savefig(chart_path)
    plt.close()

    # Add chart image to report
    if os.path.exists(chart_path):
        content.append(Image(chart_path, width=400, height=250))
        content.append(Spacer(1, 20))
else:
    content.append(Paragraph("Dataset not found. Please check the path.", styles["Normal"]))

# ================= DASHBOARD IMAGE =================
# Add dashboard screenshot
if os.path.exists(IMG_PATH):
    content.append(Paragraph("Dashboard Screenshot", styles["Heading2"]))
    content.append(Image(IMG_PATH, width=400, height=250))
else:
    content.append(Paragraph("Dashboard screenshot not found.", styles["Normal"]))

# ================= SAVE PDF =================
pdf.build(content)

print("✅ Report generated successfully: ", OUTPUT_PDF)
