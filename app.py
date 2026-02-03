import streamlit as st
import pandas as pd
import json
import ollama

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Business Dashboard", layout="wide")
st.title("📊 AI Business Dashboard (Gemma 3 – Business Analyst)")

# ---------------- HELPERS ----------------
def preprocess_data(df):
    summary = {
        "rows": len(df),
        "columns": list(df.columns),
        "numeric": df.select_dtypes(include="number").columns.tolist(),
        "categorical": df.select_dtypes(exclude="number").columns.tolist(),
        "missing": df.isnull().sum().to_dict()
    }
    return summary

import re

def safe_json_parse(text):
    if not text or text.strip() == "":
        return None

    try:
        return json.loads(text)
    except:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            return None

    return None
def calculate_kpi(kpi_name, df):
    name = kpi_name.lower()
    numeric_cols = df.select_dtypes(include="number").columns

    # Total Revenue
    if "revenue" in name or "sales" in name:
        for col in numeric_cols:
            if any(x in col.lower() for x in ["revenue", "sales", "amount"]):
                return f"{df[col].sum():,.0f}"
        return "N/A"

    # Average Order Value
    if "average" in name or "order value" in name:
        return "N/A"

    # Conversion / Retention
    if any(x in name for x in ["conversion", "retention", "rate"]):
        return "N/A"

    return "N/A"


def gemma_business_analysis(profile, df):
    sample = df.head(5).to_dict()

    prompt = f"""
You are a senior business analyst and BI consultant.

Dataset profile:
Rows: {profile['rows']}
Columns: {profile['columns']}
Numeric columns: {profile['numeric']}
Categorical columns: {profile['categorical']}
Missing values: {profile['missing']}

Sample data:
{sample}

Tasks:
1. Identify business domain
2. List 4–6 important KPIs
3. Recommend charts for a dashboard
4. Write clear business insights

Return STRICT JSON in this format:
{{
  "domain": "",
  "kpis": ["", ""],
  "charts": [
    {{"type": "bar", "x": "", "y": ""}},
    {{"type": "line", "x": "", "y": ""}}
  ],
  "insights": ["", ""]
}}
"""

    response = ollama.chat(
        model="gemma3:4b",
        messages=[{"role": "user", "content": prompt}]
    )

    raw_output = response["message"]["content"]
    parsed = safe_json_parse(raw_output)

    if parsed is None:
        return {
        "domain": "Unknown",
        "kpis": [],
        "charts": [],
        "insights": ["AI could not generate structured output. Showing default dashboard."]
    }

    return parsed



def render_charts(charts, df):
    rendered = 0

    for chart in charts:
        x = chart.get("x")
        y = chart.get("y")

        if x not in df.columns or y not in df.columns:
            continue

        if chart["type"] == "bar":
            st.bar_chart(df.groupby(x)[y].sum())
            rendered += 1

        elif chart["type"] == "line":
            st.line_chart(df.groupby(x)[y].sum())
            rendered += 1

    return rendered


# ---------------- UI ----------------
uploaded_file = st.file_uploader("📁 Upload your business CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding="latin-1")


    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    profile = preprocess_data(df)

    with st.expander("📌 Dataset Summary"):
        st.json(profile)

    if st.button("🚀 Generate Business Dashboard"):
        with st.spinner("Gemma is analyzing your business data..."):
            result = gemma_business_analysis(profile, df)

        # ---------- BUSINESS DOMAIN ----------
        st.subheader("🏢 Business Domain")
        st.write(result["domain"])

        # ---------- KPIs ----------
        st.markdown("## 📈 Key Business KPIs")

        kpis = result["kpis"]
        rows = [kpis[i:i+3] for i in range(0, len(kpis), 3)]

        for row in rows:
            cols = st.columns(len(row))
            for i, kpi in enumerate(row):
                value = calculate_kpi(kpi, df)
                cols[i].metric(kpi, value)


        # ---------- DASHBOARD ----------
        st.subheader("📊 Dashboard Visuals")

        charts_rendered = 0

        if result["charts"]:
            charts_rendered = render_charts(result["charts"], df)

# fallback charts
        if charts_rendered < 2:
            numeric_cols = df.select_dtypes(include="number").columns
            cat_cols = df.select_dtypes(exclude="number").columns

            if len(cat_cols) > 0 and len(numeric_cols) > 0:
                st.bar_chart(df.groupby(cat_cols[0])[numeric_cols[0]].sum())

            if len(numeric_cols) > 1:
                st.line_chart(df[numeric_cols])



        # ---------- INSIGHTS ----------
        st.subheader("🧠 Business Insights")
        for insight in result["insights"]:
            st.write("•", insight)
