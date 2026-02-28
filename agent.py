# ==============================
# Founder BI Agent - Final Version
# ==============================

import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

from monday_client import fetch_deals_live, fetch_work_live
from normalization import normalize_board
from metrics import (
    revenue_snapshot,
    pipeline_health,
    sector_performance,
    receivables_analysis,
    billing_collection_gap,
    data_quality_report
)

# ------------------------------
# Load Environment Variables
# ------------------------------
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# ------------------------------
# LLM Tool Selection (Groq)
# ------------------------------
def llm_choose_tool(query):

    prompt = f"""
You are a founder-level business intelligence agent.

Available tools:
- revenue_snapshot
- pipeline_health
- sector_performance
- receivables_analysis
- billing_collection_gap
- data_quality_report

Choose ONLY the best tool for the following query.
Return ONLY the tool name.

Query: {query}
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()


# ------------------------------
# Deterministic Fallback Router
# ------------------------------
def fallback_router(query):

    q = query.lower()

    if "revenue" in q or "exposure" in q or "value" in q:
        return "revenue_snapshot"

    if "pipeline" in q or "health" in q:
        return "pipeline_health"

    if "sector" in q:
        return "sector_performance"

    if "receivable" in q or "outstanding" in q:
        return "receivables_analysis"

    if "billing" in q or "collection" in q:
        return "billing_collection_gap"

    if "data quality" in q or "missing" in q:
        return "data_quality_report"

    return "pipeline_health"


# ------------------------------
# Main Founder Agent
# ------------------------------
def founder_agent(query):

    trace = []

    trace.append("User query received")

    # LIVE API FETCH (NO CACHING)
    timestamp = datetime.now().strftime('%H:%M:%S')
    trace.append(f"Live API fetch at {timestamp}")

    try:
        deals = normalize_board(fetch_deals_live())
        work = normalize_board(fetch_work_live())
        combined = pd.concat([deals, work], ignore_index=True)

        trace.append("Data normalization completed")

    except Exception as e:
        return {"error": f"Data fetch failed: {str(e)}"}, trace

    # TOOL SELECTION
    try:
        tool = llm_choose_tool(query)
        trace.append(f"LLM selected tool: {tool}")

    except Exception:
        tool = fallback_router(query)
        trace.append(f"Fallback router selected tool: {tool}")

    # TOOL EXECUTION
    tool_map = {
        "revenue_snapshot": revenue_snapshot,
        "pipeline_health": pipeline_health,
        "sector_performance": sector_performance,
        "receivables_analysis": receivables_analysis,
        "billing_collection_gap": billing_collection_gap,
        "data_quality_report": data_quality_report,
    }

    if tool in tool_map:
        try:
            result = tool_map[tool](combined)
            trace.append("Tool executed successfully")
        except Exception as e:
            result = {"error": f"Tool execution failed: {str(e)}"}
            trace.append("Tool execution error")

    else:
        result = {"message": "Unable to determine appropriate analysis"}
        trace.append("Tool mapping failed")

    return result, trace