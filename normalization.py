import pandas as pd
import re


def force_numeric(series):

    return (
        series.astype(str)
        .str.replace(r"[₹, ]", "", regex=True)
        .replace(["None", "nan", "-", "", "NA", "N/A"], "0")
        .astype(float)
    )


def normalize_status(value):

    if not value:
        return "Unknown"

    v = str(value).strip().lower()

    if "complete" in v or "done" in v:
        return "Completed"
    if "progress" in v:
        return "In Progress"
    if "hold" in v:
        return "On Hold"
    if "cancel" in v:
        return "Cancelled"

    return value


def normalize_sector(value):

    if not value:
        return "Unknown"

    v = str(value).lower()

    if "oil" in v or "gas" in v or "energy" in v:
        return "Energy"
    if "infra" in v:
        return "Infrastructure"
    if "gov" in v:
        return "Government"

    return value.strip()


def normalize_board(board_json):

    items = board_json["data"]["boards"][0]["items_page"]["items"]

    rows = []

    for item in items:

        row = {"item_name": item["name"]}

        for col in item["column_values"]:

            title = col["column"]["title"]
            text = col["text"]

            if text in ["", None]:
                text = None

            if any(x in title.lower() for x in ["amount", "value", "receivable"]):
                row[title] = text

            elif "status" in title.lower():
                row[title] = normalize_status(text)

            elif "sector" in title.lower():
                row[title] = normalize_sector(text)

            else:
                row[title] = text

        rows.append(row)

    df = pd.DataFrame(rows)

    # Convert numeric columns safely
    for col in df.columns:
        if any(x in col.lower() for x in ["amount", "value", "receivable"]):
            df[col] = force_numeric(df[col])

    return df