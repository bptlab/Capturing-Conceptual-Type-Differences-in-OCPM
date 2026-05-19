"""
Metric: Divergence of Event Types per Object Type
Computes the ratio of divergent event types per object type over the total event types linked to that object type.
"""

from collections import defaultdict
import pandas as pd


def _get_object_id_to_type(ocel, cache=None):
    if cache is not None:
        return cache.get("object_id_to_type", {})
    objects_df = getattr(ocel, "objects", pd.DataFrame())
    if objects_df.empty:
        return {}
    return objects_df.set_index("ocel:oid")["ocel:type"].to_dict()


def compute_divergent_event_types_per_object_type(ocel, cache=None):
    """
    Return a DataFrame with one boolean per (event_type, object_type).

    The value is True if there exists at least one object of the object type
    that participates in two events of the event type whose object sets differ.

    Args:
        ocel: PM4Py OCEL object loaded with pm4py.read_ocel2_xml
    
    Returns:
        pd.DataFrame with columns: event_type, object_type, boolean_different_object_sets
    """
    object_id_to_type = _get_object_id_to_type(ocel, cache)
    relations_df = cache["relations_df"] if cache else getattr(ocel, "relations", pd.DataFrame())

    if not object_id_to_type or relations_df.empty:
        return pd.DataFrame(columns=["event_type", "object_type", "boolean_different_object_sets"])

    event_types = set()
    object_type_to_object_ids = defaultdict(set)
    signatures_by_event_object = defaultdict(set)

    for (_, event_type), event_rows in relations_df.groupby(["ocel:eid", "ocel:activity"], sort=False):
        event_types.add(event_type)
        related_object_ids = set(event_rows["ocel:oid"].dropna().astype(str))

        if not related_object_ids:
            continue

        object_set_signature = frozenset(related_object_ids)
        for object_id in related_object_ids:
            object_type = object_id_to_type.get(object_id)
            if object_type:
                object_type_to_object_ids[object_type].add(object_id)
                signatures_by_event_object[(event_type, object_type, object_id)].add(
                    object_set_signature
                )

    true_pairs = {
        (event_type, object_type)
        for (event_type, object_type, _), signatures in signatures_by_event_object.items()
        if len(signatures) > 1
    }

    rows = []
    for event_type in event_types:
        for object_type in object_type_to_object_ids:
            rows.append({
                "event_type": event_type,
                "object_type": object_type,
                "boolean_different_object_sets": (event_type, object_type) in true_pairs,
            })

    df = pd.DataFrame(rows).sort_values(["event_type", "object_type"])
    return df


def compute_event_types_per_object_type(ocel, cache=None):
    """
    Return a DataFrame mapping each object type to the list of event types
    that at least one object of that type interacts with.

    Args:
        ocel: PM4Py OCEL object loaded with pm4py.read_ocel2_xml
    
    Returns:
        pd.DataFrame with columns: object_type, event_types
    """
    object_id_to_type = _get_object_id_to_type(ocel, cache)
    relations_df = getattr(ocel, "relations", pd.DataFrame())

    if not object_id_to_type or relations_df.empty:
        return pd.DataFrame(columns=["object_type", "event_types"])

    object_type_to_event_types = defaultdict(set)

    if cache and "merged_relations_objects" in cache:
        merged = cache["merged_relations_objects"][["ocel:oid", "ocel:activity", "ocel:type"]].copy()
    else:
        merged = relations_df[["ocel:oid", "ocel:activity"]].merge(
            getattr(ocel, "objects", pd.DataFrame())[["ocel:oid", "ocel:type"]],
            on="ocel:oid",
            how="inner",
        )

    for object_type, group in merged.groupby("ocel:type"):
        object_type_to_event_types[object_type].update(group["ocel:activity"].dropna().astype(str).tolist())

    if not object_type_to_event_types:
        return pd.DataFrame(columns=["object_type", "event_types"])

    df = pd.DataFrame({
        "object_type": list(object_type_to_event_types.keys()),
        "event_types": [sorted(event_types) for event_types in object_type_to_event_types.values()],
    }).sort_values("object_type")
    return df


def compute_divergence_score(ocel, cache=None):
    df_boolean = compute_divergent_event_types_per_object_type(ocel, cache=cache)
    df_event_types = compute_event_types_per_object_type(ocel, cache=cache)

    true_counts = (
        df_boolean[df_boolean["boolean_different_object_sets"]]
        .groupby("object_type")
        .size()
        .rename("true_event_type_count")
    )

    df = df_event_types.copy()
    df["event_type_count"] = df["event_types"].apply(len)
    df = df.merge(true_counts, on="object_type", how="left").fillna({"true_event_type_count": 0})
    df["divergence_score"] = 0.0
    nonzero_mask = df["event_type_count"] > 0
    df.loc[nonzero_mask, "divergence_score"] = (
        df.loc[nonzero_mask, "true_event_type_count"]
        / df.loc[nonzero_mask, "event_type_count"]
    )
    df = df.sort_values("divergence_score", ascending=False)

    # print("\n=== Metric: Divergence ===")
    # print(df[["object_type", "true_event_type_count", "event_type_count", "divergence_score"]].to_string(index=False))
    return df
