Analytica Agent

Analytica Agent is a privacy-first GenAI tool that automatically converts CSV files into dashboards using local open LLMs.
It runs entirely on the user’s system, making it suitable for organisations working with sensitive data.

Overview

Many teams want quick insights from data but cannot send files to cloud-based LLMs due to privacy, compliance, or security constraints.
Analytica Agent addresses this by performing analysis and dashboard generation locally.

A user uploads a CSV file, and the system:

understands the data structure

identifies useful metrics and aggregations

generates a dashboard automatically

The entire flow runs on-prem without any external API calls.

Design Approach

Analytica Agent is built using Ollama and Gemma (open LLMs).
An agent layer interprets the dataset and decides how to analyse it before generating visual outputs.

There is no dependency on paid APIs or cloud inference.
Accuracy is prioritised over speed.

Performance depends on local hardware.
The current development environment uses 8GB RAM and 128GB storage, which results in slower execution but stable and correct outputs.

AutoML Direction (In Progress)

The project is evolving towards an AutoML-style workflow.
Current and planned capabilities include:

automatic column type detection

feature understanding and grouping

suggested metrics and aggregations

adaptive analysis based on dataset patterns

These capabilities are under active development.

Technology Stack

Python

Ollama

Gemma (open LLM)

Pandas for data processing

Visualisation libraries for dashboards

Agent-based orchestration logic

Intended Use Cases

Pharma and healthcare analytics

Enterprises handling regulated or sensitive data

Internal reporting tools

Offline or air-gapped environments

Teams exploring privacy-first GenAI systems

Project Status

Core CSV to dashboard flow is implemented.
Local LLM integration is stable.
AutoML capabilities and performance optimisations are ongoing.

Contributions

This project is actively being developed.
Feedback and contributions are welcome.

https://medium.com/google-developer-experts/personal-ai-in-pharma-keeping-your-data-private-with-zero-compromise-using-google-gemma-58ee9ce938a8
