# Capturing-Conceptual-Type-Differences-in-OCPM

Repository accompanying the paper titled: "Object or Resource? Capturing Conceptual Type Differences in Object-Centric Process Mining"

## Results

The experiment results are shown in folder `experiment results`. For each event log, the following aspects are included:

- A table including the three measurement scores and the final score per object type in the log.
- A list of expected resource types based on the information in the log description.
- A list of discovered roles for each resource type.
- The average execution time across 10 runs.

## Tool setup

To set up the tool, the following steps are required:

1. Set up a virtual Python environment and install the requirements from the `requirements.txt`, e.g., using `pip install -r requirements.txt` in the current directory.
2. Download an OCEL 2.0 log, e.g., from the [OCEL standard website](https://www.ocel-standard.org/event-logs/overview/), and place it in the `event_logs` directory.
3. Update the ``log_name`` in `src/resource_discovery.py`.
4. (Optional): If you want to update the log with the discovered resources and roles, set the `` flag to true.
5. Run the script using `python sry/resource_discovery.py`.
