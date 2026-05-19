from pathlib import Path
import time
import pm4py
import pandas as pd
from metric_lifetime import compute_lifetime_metric
from metric_dfg_node_degree import compute_average_node_degree_per_object_type
from metric_divergence import compute_divergence_score
from role_discovery import discover_roles_from_resources
from ocel_cache import build_ocel_cache
from write_transformed_log import add_is_resource_and_discovered_roles_and_export

WRITE_TRANSFORMED_LOG = True

log_names = [
    "order-management_resource_discovered.xml",
    "logistics.xml",
    "hinge-production.xml",
    "LRM-hiring.xml",
    "LRM-hospital.xml",
    "LRM-o2c.xml",
    "LRM-p2p.xml",
    "p2p.xml",
]


def run_resource_discovery():
    script_start_time = time.perf_counter()

    input_file = Path(__file__).parent.parent / "event_logs" / log_names[1]

    ocel = pm4py.read_ocel2_xml(str(input_file))
    print(f"Loaded OCEL log: {input_file.name}")

    # Build reusable OCEL cache once to avoid repeated preprocessing in each metric.
    cache = build_ocel_cache(ocel)

    df_lifetime = compute_lifetime_metric(ocel, cache=cache)

    df_divergence_score = compute_divergence_score(ocel, cache=cache)

    df_average_node_degree = compute_average_node_degree_per_object_type(ocel, cache=cache)

    df_final = (
        df_lifetime
        .merge(df_divergence_score[["object_type", "divergence_score"]], on="object_type", how="outer")
        .merge(df_average_node_degree, on="object_type", how="outer")
        .fillna(0)
    )

    df_final["final_resource_score"] = (
        + df_final["average_node_degree"]
        + df_final["normalized_lifetime_score"]
        + df_final["divergence_score"]
    ) / 3

    metric_columns = [
        "object_type",
        "normalized_lifetime_score",
        "divergence_score",
        "average_node_degree",
        "final_resource_score"
    ]

    df_final_display = df_final[metric_columns].sort_values(
        "final_resource_score", ascending=False
    )

    print("\n\n=== Final Resource Score per Object Type with Individual Metrics ===")
    print(df_final_display.to_string(index=False))

    # Extract resource types with final_resource_score > 0.6
    high_score_resources = df_final[df_final["final_resource_score"] > 0.6]["object_type"].tolist()

    print(f"\n=== High-Score Resource Types (score > 0.6) ===")
    print(f"Resources: {high_score_resources}")

    # Run role discovery for each resource type individually
    print(f"\n{'='*60}")
    print("=== Role Discovery Per Resource Type ===")
    print(f"{'='*60}")

    discovered_roles = {}

    for resource_type in high_score_resources:
        print(f"\n--- Discovering roles for resource type: {resource_type} ---")
        discovered_roles[resource_type] = discover_roles_from_resources(ocel, [resource_type], cache=cache)
        print()

    if WRITE_TRANSFORMED_LOG:
        output_file = input_file.with_name(f"{input_file.stem}_resource_discovered.xml")
        add_is_resource_and_discovered_roles_and_export(ocel, high_score_resources, discovered_roles, output_file)
        print(f"\nWrote annotated OCEL log to: {output_file}")

    total_duration_seconds = time.perf_counter() - script_start_time
    print(f"\nTotal execution time: {total_duration_seconds:.3f} seconds")


run_resource_discovery()
