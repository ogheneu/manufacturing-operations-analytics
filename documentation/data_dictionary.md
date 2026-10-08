# Data Dictionary

## Production
- production_id: unique production run identifier
- date: production date
- shift_id: S1 Morning, S2 Afternoon, S3 Night
- line_id: production line
- machine_id: machine identifier
- product_id: manufactured product
- operator_id: assigned operator
- planned_minutes: scheduled production time
- downtime_minutes: lost production time
- units_produced: total units produced
- good_units: non-defective units
- defective_units: defective units
- ideal_cycle_seconds: theoretical best cycle time
- actual_cycle_seconds: observed cycle time

## Downtime
- downtime_reason: reason for downtime
- planned_flag: whether the downtime was planned

## Maintenance
- maintenance_type: Preventive, Corrective, or Emergency
- failure_flag: 1 for failure-related maintenance, 0 otherwise
