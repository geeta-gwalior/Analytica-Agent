summary: Building a Privacy-First Pharma AI Dashboard with Gemma 3 and AutoML scope.
id: pharma-ai-gemma-dashboard
categories: AI, Gemma, Pharma
tags: expert
status: Published
authors: Geeta Kakrani
feedback link: https://github.com/geeta-gwalior/Analytica-Agent

# Building a Privacy-First Pharma AI Dashboard with Gemma 3
... baaki aapka content yahan se shuru hoga ...

# ***Codelab: Building a Privacy-First Pharma AI Dashboard with Gemma 3***

***Author:** Geeta Kakrani (Google Developer Expert, AI)*

***Category:** Generative AI / Healthcare / Business Intelligence*

***Last Updated:** February 2026*

## ***\. Overview***

*In the pharmaceutical industry, data privacy is a non-negotiable priority. Sending sensitive clinical trials, drug formulations, or patient records to public cloud-based AI models can pose significant security and regulatory risks (HIPAA, GDPR).*

*In this codelab, you will build a **"Zero-Compromise" AI Business Dashboard**. This advanced version uses **Gemma 3** not just as a chatbot, but as a **Structured Data Analyst** that identifies business domains, recommends KPIs, and suggests visualizations—all while keeping data strictly local.*

### ***What you will learn:***

* *Setting up Gemma 3 on a local machine.*  
* *Building an automated Business Intelligence (BI) dashboard using Streamlit.*  
* *Implementing structured JSON output parsing from an LLM.*  
* *Dynamically rendering charts based on AI recommendations.*

## ***\. Prerequisites***

*To follow this tutorial, you will need the following:*

* ***Python 3.9+** installed on your system.*  
* ***Ollama:** For running LLMs locally ([download at ollama.com](https://ollama.com)).*  
* *Basic knowledge of Python, Pandas, and Streamlit.*

## ***3\. Setting Up the Local AI Engine***

*We are using Gemma 3 because it is a lightweight, high-performance model optimized for reasoning and structured output tasks.*

### ***Step 1: Install Ollama***

*After installing Ollama, run the following command to download the model:*

*\# Pull the Gemma 3 4B model*

*ollama pull gemma3:4b*

### ***Step 2: Install Required Libraries***

*Install the libraries needed for data processing and the web interface:*

*pip install streamlit pandas ollama*

## ***4\. Implementation: The Advanced Dashboard***

*Create a file named `app.py`. We will implement this in three logical layers: Data Preprocessing, AI Analysis (JSON-based), and Dynamic UI Rendering.*

### ***Step 1: Data Preprocessing & Helper Functions***

*Before sending data to the AI, we need to summarise it so the model understands the schema without reading thousands of rows.*

* *`preprocess_data`: Extracts column names, types, and missing value counts.*  
* *`safe_json_parse`: Since LLMs sometimes add conversational text around JSON, this uses Regular Expressions to find and extract the valid JSON block.*  
* *`calculate_kpi`: A mapping function that calculates actual totals from the dataframe based on the names suggested by the AI.*

### ***Step 2: The AI Analysis Engine***

*This function constructs a prompt containing the "Profile" of the dataset. Notice the instruction **"Return STRICT JSON"**. This is crucial because it allows our Python code to use the AI's "thoughts" to build actual UI components.*

### ***Step 3: UI Layer***

*Using Streamlit, we create a file uploader. Once a file is uploaded, the AI analyzes the metadata, and the dashboard dynamically builds metrics and charts.*

### ***The Full Code***

*Paste the following code into your `app.py`:*

*import streamlit as st*

*import pandas as pd*

*import json*

*import ollama*

*import re*

*\# \---------------- CONFIG & UI \----------------*

*st.set\_page\_config(page\_title="AI Pharma Business Dashboard", layout="wide")*

*st.title("📊 Pharma Business Dashboard (Gemma 3 – AI Analyst)")*

*\# \---------------- HELPERS: Data & Parsing \----------------*

*def preprocess\_data(df):*

    *""" Summarises dataset structure for the LLM."""*

    *return {*

        *"rows": len(df),*

        *"columns": list(df.columns),*

        *"numeric": df.select\_dtypes(include="number").columns.tolist(),*

        *"categorical": df.select\_dtypes(exclude="number").columns.tolist(),*

        *"missing": df.isnull().sum().to\_dict()*

    *}*

*def safe\_json\_parse(text):*

    *"""Safely extracts and parses JSON from LLM response."""*

    *if not text or text.strip() \== "": return None*

    *try:*

        *return json.loads(text)*

    *except:*

        *match \= re.search(r"\\{.\*\\}", text, re.DOTALL)*

        *if match:*

            *try: return json.loads(match.group())*

            *except: return None*

    *return None*

*def calculate\_kpi(kpi\_name, df):*

    *"""Logic to map AI suggested KPIs to actual data values."""*

    *name \= kpi\_name.lower()*

    *numeric\_cols \= df.select\_dtypes(include="number").columns*

    *if any(x in name for x in \["revenue", "sales", "amount"\]):*

        *for col in numeric\_cols:*

            *if any(x in col.lower() for x in \["revenue", "sales", "amount"\]):*

                *return f"${df\[col\].sum():,.0f}"*

    *return "N/A"*

*\# \---------------- AI ANALYSIS ENGINE \----------------*

*def gemma\_business\_analysis(profile, df):*

    *sample \= df.head(5).to\_dict()*

    *prompt \= f"""*

*You are a senior pharma business analyst.* 

*Dataset profile: {profile}*

*Sample data: {sample}*

*Tasks:*

*1\. Identify business domain (e.g., Clinical Trials, Sales, Supply Chain)*

*2\. List 4–6 important KPIs*

*3\. Recommend charts (bar or line)*

*4\. Write clear business insights*

*Return STRICT JSON:*

*{{*

  *"domain": "",*

  *"kpis": \["", ""\],*

  *"charts": \[{{"type": "bar", "x": "", "y": ""}}\],*

  *"insights": \["", ""\]*

*}}*

*"""*

    *response \= ollama.chat(model="gemma3:4b", messages=\[{"role": "user", "content": prompt}\])*

    *parsed \= safe\_json\_parse(response\["message"\]\["content"\])*

    *return parsed if parsed else {"domain": "Unknown", "kpis": \[\], "charts": \[\], "insights": \["Parsing Error"\]}*

*\# \---------------- DYNAMIC UI RENDERING \----------------*

*uploaded\_file \= st.file\_uploader("📁 Upload your Pharma/Business CSV file", type=\["csv"\])*

*if uploaded\_file:*

    *df \= pd.read\_csv(uploaded\_file, encoding="latin-1")*

    *st.subheader("🔍 Data Preview")*

    *st.dataframe(df.head())*

    

    *profile \= preprocess\_data(df)*

    *if st.button(" Generate AI Insights"):*

        *with st.spinner("Gemma 3 is analyzing your data locally..."):*

            *result \= gemma\_business\_analysis(profile, df)*

        *st.subheader(f" Domain: {result\['domain'\]}")*

        

        *\# Display KPIs*

        *st.markdown("\#\# 📈 Key Metrics")*

        *k\_cols \= st.columns(len(result\["kpis"\]\[:4\]))*

        *for i, kpi in enumerate(result\["kpis"\]\[:4\]):*

            *val \= calculate\_kpi(kpi, df)*

            *k\_cols\[i\].metric(kpi, val)*

        *\# Render AI-Recommended Charts*

        *st.subheader("📊 Visual Analytics")*

        *for chart in result\["charts"\]:*

            *x, y \= chart.get("x"), chart.get("y")*

            *if x in df.columns and y in df.columns:*

                *if chart\["type"\] \== "bar": st.bar\_chart(df.groupby(x)\[y\].sum())*

                *else: st.line\_chart(df.groupby(x)\[y\].sum())*

        *st.subheader("🧠 Strategic Insights")*

        *for insight in result\["insights"\]:*

            *st.write(f"• {insight}")*

## ***5\. Key Innovations in this Codelab***

* ***Structured Reasoning:** Instead of plain text, the model generates JSON, allowing the code to programmatically build the UI.*  
* ***Zero-Data Leakage:** Even the data summarization and metadata analysis happen within your local `ollama` instance.*  
* ***Dynamic BI:** The dashboard adapts to any CSV—whether it's clinical trial results or pharma supply chain logs.*

## ***6\. Running the Application***

*Launch your private dashboard by running:*

*streamlit run app.py*

## ***7\. Conclusion***

*By integrating Gemma 3 as a structured analyst, you've moved beyond simple chat interfaces into **Agentic BI**. For Pharma consultants, this provides a "ready-to-deploy" framework that respects data sovereignty while delivering high-level executive insights.*

***Next Steps:***

* ***Persistence:** Connect this to a local database instead of CSV uploads.*  
* ***Advanced Logic:** Refine the `calculate_kpi` function to handle complex Pharma-specific formulas like "Drug Efficacy Ratio."*

## ***8\. Future Roadmap: Agentic AutoML Integration***

*The true power of this project lies in its future scalability. We are moving towards an **Agentic AutoML** framework where:*

1. ***Automated Model Selection:** Instead of human-defined models, the agent will analyze the dataset's distribution and automatically select the best machine learning algorithm (e.g., Random Forest vs. XGBoost for clinical outcome prediction).*  
2. ***Self-Correction:** If the model's accuracy is below a threshold, the Agent will perform hyperparameter tuning locally without user intervention.*  
3. ***Cross-Model Reasoning:** Integrating Gemini via API for high-level strategy (Public data) while keeping Gemma 3 local for sensitive computations (Hybrid AI).*

*Developed by Geeta Kakrani | Google Developer Expert (AI)*

