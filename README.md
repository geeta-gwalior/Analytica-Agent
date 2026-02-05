 <h1>Analytica-Agent: Privacy-First Pharma AI Dashboard</h1>

Powered by Gemma 3 & Agentic AutoML

 <b>Overview</b>

Analytica-Agent is an enterprise-grade Business Intelligence (BI) tool designed specifically for the Pharmaceutical industry. Built with a Privacy-First mindset, it leverages the power of Gemma 3 to perform deep data analysis locally, ensuring sensitive clinical and sales data never leaves the premises.

 <b>Key Features</b>

Zero-Cloud Analysis: Fully local execution using Ollama and Gemma 3.

Agentic Domain Discovery: Automatically identifies business domains (Clinical, Sales, Supply Chain).

Dynamic KPI Generation: AI-driven metrics and chart recommendations based on data schema.

Privacy-Compliant: Designed for HIPAA and GDPR sensitive environments.

 Future Scope: Agentic AutoML

We are currently integrating an AutoML Engine where the agent doesn't just analyse data but also:

Model Selection: Automatically chooses between Regression, Classification, or Clustering based on feature distribution.

Autonomous Training: Triggers local scikit-learn pipelines without user intervention.

Self-Correction: Refines hyperparameters based on local accuracy benchmarks.

 <b>Learn with the Codelab</b>

I have authored a detailed, step-by-step Codelab for this project.
👉 View the Pharma AI Codelab (Note: If hosting on GitHub Pages, provide the full URL here)

 Quick Start

# Clone the repository
git clone [https://github.com/geeta-gwalior/Analytica-Agent.git](https://github.com/geeta-gwalior/Analytica-Agent.git)

# Install dependencies
pip install streamlit pandas ollama

# Pull Gemma 3
ollama pull gemma3:4b

# Run the dashboard
streamlit run app.py


👩‍💻 Author

Geeta Kakrani Google Developer Expert (AI) 22+ Years of Experience in Tech Leadership & AI Research.

This project is part of my research into making Generative AI accessible and secure for highly regulated industries.
