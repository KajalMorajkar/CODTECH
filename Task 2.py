
"""
covid_report.py
Automated COVID-19 Data Report
--------------------------------
- Fetches live COVID-19 data from a public API (no key)
- Creates a bar chart for cases, recoveries, and deaths
- Generates a professional PDF report automatically
"""

import requests
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
from datetime import datetime

# ---------------- FETCH COVID DATA ----------------
def fetch_covid_data(country):
    """Fetch COVID data for a given country (no API key needed)."""
    url = f"https://disease.sh/v3/covid-19/countries/{country}?strict=true"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()

    covid_info = {
        "Country": data["country"],
        "Total Cases": data["cases"],
        "Recovered": data["recovered"],
        "Deaths": data["deaths"],
        "Active Cases": data["active"],
        "Today's Cases": data["todayCases"],
        "Today's Deaths": data["todayDeaths"],
        "Today's Recovered": data["todayRecovered"],
        "Last Updated": datetime.fromtimestamp(data["updated"] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
    }
    return covid_info

# ---------------- CREATE CHART ----------------
def create_chart(covid_info):
    """Create a bar chart comparing Cases, Recovered, and Deaths."""
    categories = ["Total Cases", "Recovered", "Deaths"]
    values = [covid_info["Total Cases"], covid_info["Recovered"], covid_info["Deaths"]]

    plt.figure(figsize=(7, 5))
    plt.bar(categories, values, color=["orange", "green", "red"])
    plt.title(f"COVID-19 Summary - {covid_info['Country']}")
    plt.ylabel("Number of People")
    plt.tight_layout()
    chart_path = "covid_chart.png"
    plt.savefig(chart_path, dpi=150)
    plt.close()
    print(f"✅ Chart saved as {chart_path}")
    return chart_path

# ---------------- PDF REPORT ----------------
def generate_pdf_report(covid_info, chart_path):
    pdf = FPDF()
    pdf.add_page()

    # Function to clean Unicode text (replace unsupported characters)
    def clean(text):
        return str(text).encode("latin-1", "replace").decode("latin-1")

    # Title
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, clean(f"COVID-19 Report - {covid_info['Country']}"), ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, clean(f"Generated on: {covid_info['Last Updated']}"), ln=True, align="C")
    pdf.ln(10)

    # Insert chart
    if os.path.exists(chart_path):
        pdf.image(chart_path, x=15, w=180)
        pdf.ln(10)

    # Table Header
    pdf.set_font("Arial", "B", 12)
    pdf.cell(70, 8, clean("Metric"), border=1, align="C")
    pdf.cell(60, 8, clean("Value"), border=1, align="C")
    pdf.ln()

    # Table Data
    pdf.set_font("Arial", "", 12)
    for key, val in covid_info.items():
        if key not in ["Country", "Last Updated"]:
            pdf.cell(70, 8, clean(key), border=1)
            pdf.cell(60, 8, clean(val), border=1, align="C")
            pdf.ln()

    pdf.output("covid_report.pdf")
    print("✅ PDF report saved as covid_report.pdf")

# ---------------- MAIN FUNCTION ----------------
def main():
    country = "India"  # You can change to any other country
    print(f"Fetching COVID-19 data for {country}...")
    try:
        covid_info = fetch_covid_data(country)
    except Exception as e:
        print("❌ Error fetching data:", e)
        return

    chart_path = create_chart(covid_info)
    generate_pdf_report(covid_info, chart_path)
    print("🎉 Report generation completed successfully!")

if __name__ == "__main__":
    main()
