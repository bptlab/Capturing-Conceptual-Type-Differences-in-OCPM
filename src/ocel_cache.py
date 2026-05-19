"""
Shared OCEL preprocessing cache.

Build once in the main pipeline and pass to metric functions to avoid repeated
DataFrame normalization, joins, and dictionary construction.
"""

import pandas as pd


def build_ocel_cache(ocel):
    """Precompute normalized OCEL structures reused by multiple metrics."""
    objects_df_raw = getattr(ocel, "objects", pd.DataFrame())
    relations_df_raw = getattr(ocel, "relations", pd.DataFrame())

    if objects_df_raw.empty:
        objects_df = pd.DataFrame(columns=["ocel:oid", "ocel:type"])
    else:
        objects_df = objects_df_raw.loc[:, ["ocel:oid", "ocel:type"]].dropna().copy()
        objects_df["ocel:oid"] = objects_df["ocel:oid"].astype(str)
        objects_df["ocel:type"] = objects_df["ocel:type"].astype(str).str.strip()

    relations_cols = [col for col in ["ocel:eid", "ocel:oid", "ocel:activity", "ocel:timestamp"] if col in relations_df_raw.columns]
    if relations_df_raw.empty or not relations_cols:
        relations_df = pd.DataFrame(columns=["ocel:eid", "ocel:oid", "ocel:activity", "ocel:timestamp"])
    else:
        relations_df = relations_df_raw.loc[:, relations_cols].copy()
        if "ocel:oid" in relations_df.columns:
            relations_df["ocel:oid"] = relations_df["ocel:oid"].astype(str)
        if "ocel:activity" in relations_df.columns:
            relations_df["ocel:activity"] = relations_df["ocel:activity"].astype(str)
        if "ocel:eid" in relations_df.columns:
            relations_df["ocel:eid"] = relations_df["ocel:eid"].astype(str)
        if "ocel:timestamp" in relations_df.columns:
            relations_df["ocel:timestamp"] = pd.to_datetime(relations_df["ocel:timestamp"], errors="coerce", utc=True)

    object_id_to_type = objects_df.set_index("ocel:oid")["ocel:type"].to_dict() if not objects_df.empty else {}
    object_types = sorted(objects_df["ocel:type"].unique().tolist()) if not objects_df.empty else []

    merged_rel_obj = pd.DataFrame(columns=["ocel:eid", "ocel:activity", "ocel:oid", "ocel:type", "ocel:timestamp"])
    if not relations_df.empty and not objects_df.empty and "ocel:oid" in relations_df.columns:
        merged_rel_obj = relations_df.merge(objects_df, on="ocel:oid", how="left")

    return {
        "objects_df": objects_df,
        "relations_df": relations_df,
        "object_id_to_type": object_id_to_type,
        "object_types": object_types,
        "merged_relations_objects": merged_rel_obj,
    }
