"""
Metric: Average Object Type Lifetime
Computes average lifetime per object type normalized over the log duration.
"""

import pandas as pd


def compute_lifetime_metric(ocel, cache=None):
    """
    Compute average lifetime per object type.

    Args:
        ocel: PM4Py OCEL object loaded with pm4py.read_ocel2_xml
    
    Returns:
        pd.DataFrame with columns: object_type, Average lifetime in days, 
                                   normalized_lifetime_score
    """
    objects_df = cache["objects_df"] if cache else getattr(ocel, "objects", pd.DataFrame())
    relations_df = cache["relations_df"] if cache else getattr(ocel, "relations", pd.DataFrame())

    if objects_df.empty or relations_df.empty:
        return pd.DataFrame(
            columns=["object_type", "Average lifetime in days", "normalized_lifetime_score"]
        )

    object_id_to_type = cache["object_id_to_type"] if cache else objects_df.set_index("ocel:oid")["ocel:type"].to_dict()
    relations = relations_df[["ocel:oid", "ocel:timestamp"]].copy()
    if not pd.api.types.is_datetime64_any_dtype(relations["ocel:timestamp"]):
        relations["ocel:timestamp"] = pd.to_datetime(relations["ocel:timestamp"], errors="coerce", utc=True)
    relations = relations.dropna(subset=["ocel:timestamp"])

    if relations.empty:
        return pd.DataFrame(
            columns=["object_type", "Average lifetime in days", "normalized_lifetime_score"]
        )

    min_event_time = relations["ocel:timestamp"].min()
    max_event_time = relations["ocel:timestamp"].max()

    grouped = relations.groupby("ocel:oid")["ocel:timestamp"].agg(["min", "max", "count"])
    if grouped.empty:
        return pd.DataFrame(
            columns=["object_type", "Average lifetime in days", "normalized_lifetime_score"]
        )
    # For objects with only 1 event, set lifetime to 0; for multiple events, compute the difference
    grouped["lifetime_days"] = (grouped["max"] - grouped["min"]).dt.total_seconds() / (60 * 60 * 24)
    grouped.loc[grouped["count"] == 1, "lifetime_days"] = 0
    grouped["object_type"] = grouped.index.map(object_id_to_type)
    grouped = grouped.dropna(subset=["object_type"])

    avg_lifetime_by_type = (
        grouped.groupby("object_type")["lifetime_days"].mean().to_dict()
    )

    log_life = (max_event_time - min_event_time).total_seconds() / (60 * 60 * 24)
    if avg_lifetime_by_type:
        norm_life = {
            ot: avg_life / log_life
            for ot, avg_life in avg_lifetime_by_type.items()
        }
    else:
        norm_life = {}

    if not avg_lifetime_by_type:
        return pd.DataFrame(
            columns=["object_type", "Average lifetime in days", "normalized_lifetime_score"]
        )

    df_lifetime = pd.DataFrame({
        "object_type": list(avg_lifetime_by_type.keys()),
        "Average lifetime in days": list(avg_lifetime_by_type.values()),
        "normalized_lifetime_score": [norm_life[ot] for ot in avg_lifetime_by_type.keys()]
    }).sort_values("normalized_lifetime_score", ascending=False)

    # print("\n=== Metric: Average Object Type Lifetime ===")
    # print(f"Total log duration: {log_life:.2f} days")
    # print(df_lifetime.to_string(index=False))
    
    return df_lifetime
