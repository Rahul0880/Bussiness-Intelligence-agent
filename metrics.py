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

    return (
        f"The current pipeline stands at ₹{total_value:,.2f} across "
        f"{total_deals} deals, with an average deal size of "
        f"₹{avg_value:,.2f}. This represents your total revenue exposure."
    )


# -----------------------------
# Pipeline Health
# -----------------------------
def pipeline_health(df):

    status_col = [c for c in df.columns if "status" in c.lower()][0]
    distribution = df[status_col].fillna("Unknown").value_counts().to_dict()

    most_common = max(distribution, key=distribution.get)

    return (
        f"The pipeline is primarily concentrated in '{most_common}' status. "
        f"Status distribution is as follows: {distribution}."
    )


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

    if not result:
        return "No sector-level revenue data available."

    top_sector = next(iter(result))
    top_value = result[top_sector]

    return (
        f"The '{top_sector}' sector currently leads with ₹{top_value:,.2f} "
        f"in total value. Full sector breakdown: {result}."
    )


# -----------------------------
# Receivables Analysis
# -----------------------------
def receivables_analysis(df):

    recv_cols = [c for c in df.columns if "receivable" in c.lower()]

    if not recv_cols:
        return "Receivable data is not available in the dataset."

    values = force_numeric(df[recv_cols[0]])
    total = float(values.sum())
    avg = float(values.mean())

    return (
        f"Outstanding receivables total ₹{total:,.2f}, with an average "
        f"receivable per deal of ₹{avg:,.2f}. Monitoring collections "
        f"is advisable to maintain healthy cash flow."
    )


# -----------------------------
# Billing vs Collection Gap
# -----------------------------
def billing_collection_gap(df):

    billed_cols = [c for c in df.columns if "billed" in c.lower()]
    collected_cols = [c for c in df.columns if "collected" in c.lower()]

    if not billed_cols or not collected_cols:
        return "Billing or collection data is incomplete."

    billed = force_numeric(df[billed_cols[0]]).sum()
    collected = force_numeric(df[collected_cols[0]]).sum()
    gap = float(billed - collected)

    return (
        f"Total billed revenue stands at ₹{billed:,.2f}, while "
        f"collected revenue is ₹{collected:,.2f}, leaving a "
        f"collection gap of ₹{gap:,.2f}."
    )


# -----------------------------
# Data Quality Report
# -----------------------------
def data_quality_report(df):

    rows = int(df.shape[0])
    cols = int(df.shape[1])
    missing = int(df.isna().sum().sum())

    return (
        f"The dataset contains {rows} records across {cols} columns, "
        f"with {missing} missing values identified. Data completeness "
        f"should be reviewed before making high-stakes decisions."
    )
