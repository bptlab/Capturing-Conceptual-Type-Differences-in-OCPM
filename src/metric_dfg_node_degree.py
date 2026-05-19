"""
Metric: Average Node Degree per Object Type DFG
Computes the average node degree for the typed DFG of each object type. If the DFG is disconnected, computes the average node degree per component and averages those.
"""

import pm4py
import pandas as pd


def _get_object_types(ocel):
    objects_df = getattr(ocel, "objects", pd.DataFrame())
    if objects_df.empty:
        return []
    return sorted(objects_df["ocel:type"].dropna().astype(str).unique().tolist())


def discover_typed_dfgs_per_object_type(ocel, cache=None):
    objects_df = cache["objects_df"] if cache else getattr(ocel, "objects", pd.DataFrame())
    object_types = cache["object_types"] if cache else _get_object_types(ocel)
    object_counts = {}

    if not objects_df.empty:
        object_counts = objects_df["ocel:type"].value_counts(dropna=True).astype(int).to_dict()

    results = {}
    for object_type in object_types:
        flattened_log = pm4py.ocel_flattening(ocel, object_type)
        typed_dfg = pm4py.discover_dfg_typed(flattened_log)
        results[object_type] = typed_dfg

    return results, object_counts


def _build_average_node_degree_dataframe(results):
    rows = []

    for object_type, result in results.items():
        graph = getattr(result, "graph", {}) or {}
        edges = list(graph)
        number_of_edges = len(edges)

        # collect all nodes referenced by edges
        nodes = set()
        for edge in edges:
            if isinstance(edge, tuple) and len(edge) == 2:
                nodes.update(edge)

        number_of_nodes = len(nodes)

        # If the graph is disconnected, compute the metric per connected component
        # and average the per-component metrics. Connectivity is considered
        # undirected for component detection.
        average_node_degree = 0.0
        if number_of_nodes:
            # build undirected adjacency
            from collections import defaultdict, deque

            adj = defaultdict(set)
            for edge in edges:
                if isinstance(edge, tuple) and len(edge) == 2:
                    u, v = edge
                    adj[u].add(v)
                    adj[v].add(u)

            # find connected components
            visited = set()
            components = []
            for n in nodes:
                if n in visited:
                    continue
                comp = set()
                dq = deque([n])
                while dq:
                    cur = dq.popleft()
                    if cur in visited:
                        continue
                    visited.add(cur)
                    comp.add(cur)
                    for nb in adj.get(cur, ()):  # neighbors
                        if nb not in visited:
                            dq.append(nb)
                components.append(comp)

            if len(components) <= 1:
                average_node_degree = number_of_edges / (number_of_nodes * number_of_nodes)
            else:
                comp_avgs = []
                for comp in components:
                    comp_nodes = len(comp)
                    comp_edges = sum(1 for (u, v) in edges if u in comp and v in comp)
                    comp_avg = (comp_edges / (comp_nodes * comp_nodes)) if comp_nodes else 0.0
                    comp_avgs.append(comp_avg)
                average_node_degree = sum(comp_avgs) / len(comp_avgs)

        rows.append(
            {
                "object_type": object_type,
                "number_of_nodes": number_of_nodes,
                "number_of_edges": number_of_edges,
                "average_node_degree": average_node_degree,
            }
        )

    return pd.DataFrame(rows).sort_values("average_node_degree", ascending=False)


def compute_average_node_degree_per_object_type(ocel, cache=None):
    results, _ = discover_typed_dfgs_per_object_type(ocel, cache=cache)
    return _build_average_node_degree_dataframe(results)


# def main():
#     from pathlib import Path

#     input_ocel = Path(__file__).parent.parent / "Event Logs" / "Logistics_original.xml"
#     # print(f"Loading OCEL: {input_ocel.name}")
#     ocel = pm4py.read_ocel2_xml(str(input_ocel))
#     df_average_node_degree = compute_average_node_degree_per_object_type(ocel)
#     # print("\n=== Average Node Degree per Object Type ===")
#     # print(df_average_node_degree.to_string(index=False))


# if __name__ == "__main__":
#     main()
