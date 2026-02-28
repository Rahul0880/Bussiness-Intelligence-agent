from normalization import force_numeric


# -----------------------------
# Revenue Snapshot
# -----------------------------
def revenue_snapshot(df):

    value_col = [c for c in df.columns if "value" in c.lower()][0]
    values = force_numeric(df[value_col])

    total_value = float(values.sum())
    total_deals = int(len(df))
    avg_value = total_value / total_deals if total_deals else 0

    return {
        "summary": f"Overall pipeline value is ₹{total_value:,.2f} across {total_deals} deals. Average deal value is ₹{avg_value:,.2f}.",
        "data": {
            "Total Pipeline Value": total_value,
            "Total Deals": total_deals,
            "Average Deal Value": avg_value
        }
    }


# -----------------------------
# Pipeline Health
# -----------------------------
def pipeline_health(df):

    status_col = [c for c in df.columns if "status" in c.lower()][0]
    distribution = df[status_col].fillna("Unknown").value_counts().to_dict()

    most_common = max(distribution, key=distribution.get)

    return {
        "summary": f"Pipeline is primarily in '{most_common}' status. Distribution across statuses shown below.",
        "data": distribution
    }


# -----------------------------
# Sector Performance
# -----------------------------
def sector_performance(df):

    sector_col = [c for c in df.columns if "sector" in c.lower()][0]
    value_col = [c for c in df.columns if "value" in c.lower()][0]

    temp = df.copy()
    temp["clean_value"] = force_numeric(temp[value_col])

    result = (
        temp.groupby(sector_col)["clean_value"]
        .sum()
        .sort_values(ascending=False)
        .to_dict()
    )

    top_sector = next(iter(result)) if result else "N/A"

    return {
        "summary": f"Top performing sector is '{top_sector}'. Detailed sector-wise revenue below.",
        "data": result
    }


# -----------------------------
# Receivables Analysis
# -----------------------------
def receivables_analysis(df):

    recv_cols = [c for c in df.columns if "receivable" in c.lower()]

    if not recv_cols:
        return {
            "summary": "No receivable data available.",
            "data": {}
        }

    values = force_numeric(df[recv_cols[0]])
    total = float(values.sum())
    avg = float(values.mean())

    return {
        "summary": f"Total outstanding receivables are ₹{total:,.2f}. Average receivable per deal is ₹{avg:,.2f}.",
        "data": {
            "Outstanding Receivables": total,
            "Average Receivable": avg
        }
    }


# -----------------------------
# Billing vs Collection Gap
# -----------------------------
def billing_collection_gap(df):

    billed_cols = [c for c in df.columns if "billed" in c.lower()]
    collected_cols = [c for c in df.columns if "collected" in c.lower()]

    if not billed_cols or not collected_cols:
        return {
            "summary": "Billing or collection data missing.",
            "data": {}
        }

    billed = force_numeric(df[billed_cols[0]]).sum()
    collected = force_numeric(df[collected_cols[0]]).sum()
    gap = float(billed - collected)

    return {
        "summary": f"Total billed amount is ₹{billed:,.2f}, collected amount is ₹{collected:,.2f}. Collection gap is ₹{gap:,.2f}.",
        "data": {
            "Total Billed": float(billed),
            "Total Collected": float(collected),
            "Collection Gap": gap
        }
    }


# -----------------------------
# Data Quality Report
# -----------------------------
def data_quality_report(df):

    rows = int(df.shape[0])
    cols = int(df.shape[1])
    missing = int(df.isna().sum().sum())

    return {
        "summary": f"Dataset contains {rows} rows and {cols} columns with {missing} missing values.",
        "data": {
            "Rows": rows,
            "Columns": cols,
            "Missing Values": missing
        }
    }
