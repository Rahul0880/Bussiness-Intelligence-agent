# Founder BI Agent
## AI-Powered Business Intelligence Agent for monday.com

---

## Overview

Founder BI Agent is an AI-powered Business Intelligence assistant that answers founder and executive-level business questions using **live monday.com board data**.

The system connects directly to monday.com through the GraphQL API, retrieves data at query time (no caching), normalizes inconsistent business datasets, and generates analytical insights across **Deals** and **Work Orders** boards.

Users can ask natural language questions such as:

- How is our pipeline looking?
- What is our revenue exposure?
- Which sector performs best?
- Do we have receivables risk?

---

## Live Demo

Hosted Prototype:  
<RENDER_APP_URL>

---

## monday.com Boards Used

Deals Board:  
[<DEALS_BOARD_LINK>](https://rahulnimbai018s-team.monday.com/boards/5026905032)

Work Orders Board:  
[<WORK_ORDERS_BOARD_LINK>](https://rahulnimbai018s-team.monday.com/boards/5026905024)

---

## Features

### Live monday.com Integration
- GraphQL API integration
- Data fetched live for every query
- No preloading or caching

### Data Resilience
- Handles messy CSV imports
- Normalizes currency values, missing fields, statuses, and sector names
- Graceful handling of null and inconsistent data

### Founder-Level Business Intelligence
Supports analytics including:
- Revenue exposure analysis
- Pipeline health monitoring
- Sector performance comparison
- Receivables risk analysis
- Billing vs collection gap
- Data quality reporting

### AI Agent with Tool Calling
- MCP-style tool orchestration
- LLM-assisted tool selection (Groq LLaMA 3)
- Deterministic fallback router for reliability
- Visible execution trace for transparency

### Conversational Interface
- Built using Streamlit
- Zero setup required for evaluation

---

## System Architecture

User Query  
→ Streamlit Interface  
→ Founder Agent  
→ Live monday.com API Calls  
→ Data Normalization  
→ BI Tool Execution  
→ Insight + Tool Trace

---

## Technology Stack

Frontend: Streamlit  
Backend: Python  
Data Processing: Pandas  
API Integration: monday.com GraphQL API  
AI Routing: Groq (LLaMA 3)  
Environment Management: python-dotenv  
Deployment: Render

---

