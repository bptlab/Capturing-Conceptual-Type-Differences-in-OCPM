# Order Management

Link: [https://www.ocel-standard.org/event-logs/simulations/order-management/](https://www.ocel-standard.org/event-logs/simulations/order-management/)

## Resource Discovery

### Final Resource Score per Object Type with Individual Metrics

| Object Type | Extended Object Lifetime Score | Divergent Behavior Score | Unstructured Individual Behavior Score | Final Score |
| --- | --- | --- | --- | --- |
| products | 0.95 | 1.0 | 1.0 | 0.98 |
| customers | 0.82 | 1.0 | 1.0 | 0.94 |
| employees | 0.91 | 1.0 | 0.84 | 0.92 |
| items | 0.04 | 0.0 | 0.46 | 0.17 |
| orders | 0.03 | 0.0 | 0.31 | 0.11 |
| packages | 0.0 | 0.0 | 0.31 | 0.11 |

### Expected Resource Types

- `products`: Represent the categories of items in the process. Are involved in events whenever an item of the respective type is involved.
- `customers`: Repeatedly place and confirm orders.
- `employees`: Employees of the organization.

## Role Discovery

### Discovered Roles Per Resource Type

employees:

- ['send package']
- ['create package', 'item out of stock', 'pick item', 'reorder item']
- ['failed delivery', 'package delivered']
- ['confirm order']

The roles are in line with the `role` attribute of employees. Attribute values differentiates Sales (can execute "confirm order"), Shipment (can execute "send package", "failed delivery", and "package delivered"), and Warehousing (can execute "send package", "create package", "item out of stock", "pick item", and "reorder item").

No additional roles were discovered for resource types customers and products.

## Average Execution Time for 10 Runs

5.590 seconds




# Logistics

Link: [https://www.ocel-standard.org/event-logs/simulations/logistics/](https://www.ocel-standard.org/event-logs/simulations/logistics/)

## Resource Discovery

### Final Resource Score per Object Type with Individual Metrics

| Object Type | Extended Object Lifetime Score | Divergent Behavior Score | Unstructured Individual Behavior Score | Final Score |
| --- | --- | --- | --- | --- |
| Forklift | 0.99 | 1.0 | 0.94 | 0.98 |
| Truck | 0.99 | 1.0 | 0.75 | 0.91 |
| Vehicle | 0.05 | 0.75 | 0.56 | 0.45 |
| Transport Document | 0.03 | 0.4 | 0.32 | 0.25 |
| Customer Order | 0.01 | 0.0 | 0.25 | 0.09 |
| Container | 0.03 | 0.1 | 0.12 | 0.08 |
| Handling Unit | 0.0 | 0.0 | 0.25 | 0.08 |

### Expected Resource Types

- ``Forklift``: Machines that repeatedly execute specific tasks.
- ``Truck``: Machines that repeatedly deliver containers.

Note: Vehicles and Containers are not expected resource types since each instance only occurs for a single process instance. 


## Role Discovery

### Discovered Roles Per Resource Type

No additional roles were discovered for resource types Forklift and Truck.

## Average Execution Time for 10 Runs

7.336 seconds




# Hinge Production

[https://www.ocel-standard.org/event-logs/simulations/hinge/](https://www.ocel-standard.org/event-logs/simulations/hinge/)

## Resource Discovery

### Final Resource Score per Object Type with Individual Metrics

| Object Type | Extended Object Lifetime Score | Divergent Behavior Score | Unstructured Individual Behavior Score | Final Score |
| --- | --- | --- | --- | --- |
| Machine | 0.97 | 1.0 | 0.93 | 0.97 |
| Workstation | 0.98 | 1.0 | 0.88 | 0.95 |
| Worker | 0.99 | 0.67 | 1.0 | 0.88 |
| SteelCoil | 0.07 | 1.0 | 1.0 | 0.69 |
| Facility | 0.95 | 0.0 | 1.0 | 0.65 |
| Hinge | 0.0 | 0.0 | 0.25 | 0.08 |
| FemalePart | 0.02 | 0.0 | 0.22 | 0.08 |
| MalePart | 0.02 | 0.0 | 0.22 | 0.08 |
| SteelSheet | 0.0 | 0.0 | 0.22 | 0.08 |
| FormedPart | 0.03 | 0.0 | 0.19 | 0.07 |
| HingePack | 0.0 | 0.0 | 0.0 | 0.0 |
| SteelPin | 0.0 | 0.0 | 0.0 | 0.0 |

### Expected Resource Types

- ``Machine``: Machines that repeatedly execute specific tasks.
- ``Workstation``: Facilities where several tasks can be performed.
- ``Worker``: Employee performing several steps in the process, mostly quality assurance.
- ``SteelCoil``: Coils of steel that are cut into several sheets that later form the hinges. Thus involved in several hinge productions.
- ``Facility``: Environment in which the process takes place.

## Role Discovery

### Discovered Roles Per Resource Type

Machine:
- ['SplitSteelSheet']
- ['PackHinges']
- ['HeatSteelSheet']
- ['FormSteelSheet']
- ['CuttFemalePart', 'CuttMalePart']
- ['CoatPart']
- ['AssembleHinge']

The discovered roles are in line with the log description where seven kinds of machines are distinguished: splitters, oven, former, coater, laser cutter, assembler, and packer.

Workstation:
- ['AssembleHinge', 'PackHinges']
- ['CheckFemalePart', 'CheckMalePart', 'CuttFemalePart', 'CuttMalePart']
- ['CoatPart', 'FormSteelSheet', 'HeatSteelSheet', 'SplitSteelSheet']

The discovered roles are in line with the log description where three kinds of workstations are distinguished: one for the steps from steel sheet splitting to coating, one for laser cutting and quality assurance, and one for assembling and packing.

No additional roles were discovered for resource types Facility, Worker, and SteelCoil. That is in line with the log since all three types are only involved in a single activity.

## Average Execution Time for 10 Runs

10.081 seconds




# P2P

[https://www.ocel-standard.org/event-logs/simulations/p2p/](https://www.ocel-standard.org/event-logs/simulations/p2p/)

## Resource Discovery

### Final Resource Score per Object Type with Individual Metrics

| Object Type | Extended Object Lifetime Score | Divergent Behavior Score | Unstructured Individual Behavior Score | Final Score |
| --- | --- | --- | --- | --- |
| invoice receipt | 0.01 | 0.67 | 0.67 | 0.45 |
| quotation | 0.01 | 0.67 | 0.56 | 0.41 |
| payment | 0.0 | 0.0 | 1.0 | 0.33 |
| goods receipt | 0.01 | 0.25 | 0.63 | 0.29 |
| purchase_order | 0.02 | 0.25 | 0.38 | 0.21 |
| purchase_requisition | 0.01 | 0.0 | 0.25 | 0.09 |
| material | 0.0 | 0.0 | 0.22 | 0.08 |

### Expected Resource Types

No resource types are expected in this log. All involved object types are only processed a single time.

## Role Discovery

### Discovered Roles Per Resource Type

No Resources were discovered.

## Average Execution Time for 10 Runs

14.842 seconds




# LRM Hiring

[https://zenodo.org/records/13879980](https://zenodo.org/records/13879980)

## Resource Discovery

### Final Resource Score per Object Type with Individual Metrics

| Object Type | Extended Object Lifetime Score | Divergent Behavior Score | Unstructured Individual Behavior Score | Final Score |
| --- | --- | --- | --- | --- |
| Interviewer | 0.92 | 1.0 | 0.5 | 0.81 |
| HiringManager | 0.97 | 1.0 | 0.44 | 0.8 |
| Recruiter | 1.0 | 1.0 | 0.38 | 0.79 |
| Assessment | 0.16 | 1.0 | 0.33 | 0.5 |
| JobRequisition | 0.97 | 0.25 | 0.25 | 0.49 |
| Candidate | 0.0 | 0.0 | 0.05 | 0.02 |

### Expected Resource Types

- ``Interviewer``: HR employees that perform the assessments for each job requisition.
- ``HiringManager``: HR employees that perform the assessments for each job requisition.
- ``Recruiter``: HR employees that perform the assessments for each job requisition.

## Role Discovery

### Discovered Roles Per Resource Type

No additional roles were discovered for resource types HiringManager, Interviewer, and Recruiter.

## Average Execution Time for 10 Runs

3.617 seconds




# LRM Hospital

[https://zenodo.org/records/13879980](https://zenodo.org/records/13879980)

## Resource Discovery

### Final Resource Score per Object Type with Individual Metrics

| Object Type | Extended Object Lifetime Score | Divergent Behavior Score | Unstructured Individual Behavior Score | Final Score |
| --- | --- | --- | --- | --- |
| InsuranceCompany | 0.94 | 1.0 | 1.0 | 0.98 |
| Physician | 0.87 | 1.0 | 1.0 | 0.96 |
| Room | 0.58 | 1.0 | 1.0 | 0.86 |
| Bed | 0.44 | 1.0 | 1.0 | 0.81 |
| DiagnosticEquipment | 0.43 | 1.0 | 1.0 | 0.81 |
| LabTechnician | 0.43 | 1.0 | 1.0 | 0.81 |
| Nurse | 0.58 | 1.0 | 0.5 | 0.69 |
| Patient | 0.04 | 0.0 | 0.1 | 0.05 |

### Expected Resource Types

- ``InsuranceCompany``: Involved in the insurance verification of every patient.
- ``Physician``: Employees of the hospital with respective tasks.
- ``LabTechnician``: Employees of the hospital with respective tasks.
- ``Nurse``: Employees of the hospital with respective tasks.
- ``Room``: Facilities that are repeatedly used in the process.
- ``Bed``: Facilities that are repeatedly used in the process.
- ``DiagnosticEquipment``: Tools that are repeatedly used in the process.

Note: Patient is not expected as a resource type since they are only involved in one instance each.

## Role Discovery

### Discovered Roles Per Resource Type

Physician:

- ['Pre-Admission Consultation']
- ['Diagnostic Test Order']

The log description does not state any distinction for physician role. However, we could detect that "Diagnsotic Test Order" is not performed by every physician.

## Average Execution Time for 10 Runs

2.967 seconds


# LRM O2C

[https://zenodo.org/records/13879980](https://zenodo.org/records/13879980)

## Resource Discovery

### Final Resource Score per Object Type with Individual Metrics

| Object Type | Extended Object Lifetime Score | Divergent Behavior Score | Unstructured Individual Behavior Score | Final Score |
| --- | --- | --- | --- | --- |
| Product | 0.79 | 1.0 | 0.33 | 0.71 |
| Customer | 0.32 | 1.0 | 0.23 | 0.52 |
| Payment | 0.0 | 0.0 | 0.25 | 0.08 |
| Shipment | 0.0 | 0.0 | 0.25 | 0.08 |
| Return | 0.0 | 0.0 | 0.22 | 0.07 |
| Invoice | 0.0 | 0.0 | 0.14 | 0.05 |
| Order | 0.0 | 0.0 | 0.09 | 0.03 |
| CreditNote | 0.0 | 0.0 | 0.0 | 0.0 |
| Dispute | 0.0 | 0.0 | 0.0 | 0.0 |

### Expected Resource Types

- ``Product``: Represent the categories of items in the process.
- ``Customer``: Repeatedly place orders and are involved in their processing.

## Role Discovery

### Discovered Roles Per Resource Type

No additional roles were discovered for resource types Product and Supplier.

## Average Execution Time for 10 Runs

5.644 seconds



# LRM P2P

[https://zenodo.org/records/13879980](https://zenodo.org/records/13879980)

## Resource Discovery

### Final Resource Score per Object Type with Individual Metrics

| Object Type | Extended Object Lifetime Score | Divergent Behavior Score | Unstructured Individual Behavior Score | Final Score |
| --- | --- | --- | --- | --- |
| Supplier | 0.9 | 1.0 | 0.75 | 0.88 |
| Payment | 0.01 | 1.0 | 1.0 | 0.67 |
| Invoice | 0.31 | 0.75 | 0.69 | 0.58 |
| Purchase Order | 0.28 | 0.75 | 0.42 | 0.48 |
| Goods Receipt | 0.11 | 0.67 | 0.67 | 0.48 |
| Purchase Requisition | 0.0 | 0.2 | 0.48 | 0.23 |

### Expected Resource Types

- ``Supplier``: Repeatedly receive purchase orders and get paid for them.

## Role Discovery

### Discovered Roles Per Resource Type

No additional roles were discovered for resource types Payment and Supplier.

## Average Execution Time for 10 Runs

1.661 seconds
