from normalization import force_numeric


def revenue_snapshot(df):

    value_col = [c for c in df.columns if "value" in c.lower()][0]
    values = force_numeric(df[value_col])

    return {
        "Total Pipeline Value": float(values.sum()),
        "Total Deals": int(len(df))
    }


def pipeline_health(df):

    status_col = [c for c in df.columns if "status" in c.lower()][0]
    return df[status_col].fillna("Unknown").value_counts().to_dict()


def sector_performance(df):

    sector_col = [c for c in df.columns if "sector" in c.lower()][0]
    value_col = [c for c in df.columns if "value" in c.lower()][0]

    temp = df.copy()
    temp["clean_value"] = force_numeric(temp[value_col])

    return (
        temp.groupby(sector_col)["clean_value"]
        .sum()
        .sort_values(ascending=False)
        .to_dict()
    )


def receivables_analysis(df):

    recv_cols = [c for c in df.columns if "receivable" in c.lower()]

    if not recv_cols:
        return {"message": "No receivable data found"}

    values = force_numeric(df[recv_cols[0]])

    return {
        "Outstanding Receivables": float(values.sum()),
        "Average Receivable": float(values.mean())
    }


def billing_collection_gap(df):

    billed_cols = [c for c in df.columns if "billed" in c.lower()]
    collected_cols = [c for c in df.columns if "collected" in c.lower()]

    if not billed_cols or not collected_cols:
        return {"message": "Billing/collection data missing"}

    billed = force_numeric(df[billed_cols[0]]).sum()
    collected = force_numeric(df[collected_cols[0]]).sum()

    return {
        "Total Billed": float(billed),
        "Total Collected": float(collected),
        "Collection Gap": float(billed - collected)
    }


def data_quality_report(df):

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "missing_values": int(df.isna().sum().sum())
    }