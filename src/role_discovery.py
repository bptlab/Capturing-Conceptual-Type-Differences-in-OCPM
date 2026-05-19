"""
Role Discovery from Event-Resource Interactions.

For each event type, identifies which resources it interacts with.
Then discovers roles as distinct sets of resources that occur across event types.
"""

from collections import defaultdict
import pandas as pd


def discover_roles_from_resources(ocel, resource_types, cache=None):
    """
    Discover roles based on distinct event-resource interaction patterns.
    
    Algorithm:
    1. For each event type, identify which resources it interacts with.
    2. Group event types by their resource set.
    3. Each distinct resource set becomes a role.
    4. Print the discovered roles and their activities.
    
    Args:
        ocel: PM4Py OCEL object
        resource_types: List of resource types to consider
    
    Returns:
        dict: Mapping of role_id -> {resources: set, event_types: set}
    """
    if not resource_types:
        print("\n=== Role Discovery ===")
        print("No resource types provided. No roles discovered.")
        return {}
    
    relations_df = (cache["relations_df"] if cache else getattr(ocel, "relations", pd.DataFrame())).copy()
    objects_df = (cache["objects_df"] if cache else getattr(ocel, "objects", pd.DataFrame())).copy()

    if relations_df.empty or objects_df.empty:
        print("\n=== Role Discovery ===")
        print("Empty relations or objects DataFrame. No roles discovered.")
        return {}

    # Normalize resource types to a set of str for fast membership tests
    resource_types_set = {str(rt).strip() for rt in resource_types}

    # Reuse merged relations+objects when available in cache.
    if cache and "merged_relations_objects" in cache and not cache["merged_relations_objects"].empty:
        merged = cache["merged_relations_objects"][["ocel:oid", "ocel:activity", "ocel:type"]].dropna(subset=["ocel:oid", "ocel:activity"]).copy()
    else:
        relations_df = relations_df.loc[:, ["ocel:oid", "ocel:activity"]].dropna()
        relations_df["ocel:oid"] = relations_df["ocel:oid"].astype(str)
        relations_df["ocel:activity"] = relations_df["ocel:activity"].astype(str)

        objects_df = objects_df.loc[:, ["ocel:oid", "ocel:type"]].dropna()
        objects_df["ocel:oid"] = objects_df["ocel:oid"].astype(str)
        objects_df["ocel:type"] = objects_df["ocel:type"].astype(str).str.strip()

        merged = relations_df.merge(objects_df, on="ocel:oid", how="left")

    # Keep only relations where the object type is one of the resource types
    merged = merged[merged["ocel:type"].isin(resource_types_set)]

    if merged.empty:
        print("\n=== Role Discovery ===")
        print("No event interactions with the provided resource types. No roles discovered.")
        return {}

    # Also compute and print which individual object IDs (resources) each
    # event type interacts with (useful for debugging / inspection).
    grouped_ids = merged.groupby("ocel:activity")["ocel:oid"].agg(lambda s: set(s.dropna().astype(str)))
    event_type_to_object_ids = {str(event): ids for event, ids in grouped_ids.items()}

    # Optional debug print: only when discovering roles for Physician.
    if len(resource_types_set) == 1 and "physician" in {rt.lower() for rt in resource_types_set}:
        # print("\n=== Individual Resources per Activity (Physician) ===")
        for activity in sorted(event_type_to_object_ids):
            obj_ids = sorted(event_type_to_object_ids[activity])
            # print(f"Activity: {activity} -> Individual Resources: {obj_ids}")

    # Group event types by the exact set of individual resource IDs they interact with
    object_set_to_event_types = defaultdict(set)

    for event_type, obj_ids in event_type_to_object_ids.items():
        # Skip empty object id sets
        if not obj_ids:
            continue
        signature = frozenset(obj_ids)
        object_set_to_event_types[signature].add(event_type)

    # Build roles: each distinct object-id set is one role
    roles = {}
    for role_id, (obj_signature, event_types) in enumerate(sorted(
        object_set_to_event_types.items(),
        key=lambda x: (len(x[0]), sorted(x[0])),
        reverse=True
    )):
        roles[role_id] = {
            "object_ids": set(obj_signature),
            "event_types": event_types
        }
    
    # Print results
    if not roles:
        print("No roles discovered.")
        pass
    else:
        for role_id, role_info in roles.items():
            event_types = sorted(role_info["event_types"])
            print(f"\nRole {role_id}:")
            print(f"  Activities ({len(event_types)}): {event_types}")
    
    return roles
